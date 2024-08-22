import ctypes
import zlib
import time
import sys
import os
from ctypes import create_string_buffer
import tkinter as tk
from tkinter import ttk
from global_var import *
from ctypes import *
import global_var
import subprocess



class windows_driver(object):
    def __init__(self):
        self.dll = None
        self.dll_name = "resource\\driver\\CH341DLL.DLL"
        self.iIndex = 0

    def load(self):
        try:
            self.dll = ctypes.WinDLL(self.dll_name)
        except:
            command = "resource\\driver\\SETUP.EXE \\S"
            print("Need to install ch341 driver")
            print("Installing ...")
            subprocess.run(command, shell=True, capture_output=True, text=True)
            print("done")
            time.sleep(1)
            try:
                self.dll = ctypes.WinDLL(self.dll_name)
            except:
                a = 1

    def open_device(self):
        return self.dll.CH341OpenDevice(self.iIndex)

    def close_device(self):
        self.dll.CH341CloseDevice(self.iIndex)

    def get_version(self):
        return self.dll.CH341GetVersion()

    def get_driver_version(self):
        return self.dll.CH341GetDrvVersion()

    def get_chip_version(self):
        return self.dll.CH341GetVerIC(self.iIndex)

    def set_stream(self, cs):
        if cs == True:
            self.dll.CH341SetStream(self.iIndex, 0x80)
        else:
            self.dll.CH341SetStream(self.iIndex, 0x81)

    def stream_spi4(self, command, ilength, iobuffer):
        self.dll.CH341StreamSPI4(
            self.iIndex, command, ilength, iobuffer)

    def set_output(self, a, b, c):
        self.dll.CH341SetOutput(self.iIndex, a, b, c)

    def read_I2C(self, addr_fpga_device, addr, iobuffer):
        self.dll.CH341ReadI2C(0, addr_fpga_device, addr, iobuffer)

    def write_I2C(self, addr_usb_write_fpga_device, addr, byte):
        self.dll.CH341WriteI2C(0, addr_usb_write_fpga_device, addr, byte)

    def set_delay_ms(self, ms):
        self.dll.CH341SetDelaymS(self.iIndex, ms)



class linux_driver(object):
    def __init__(self):
        self.dll = None
        self.dll_name = "./resource/driver/libch347.so"
        self.iIndex = 0

    def load(self):
        try:
            self.dll = cdll.LoadLibrary(self.dll_name)
        except:
            print("Please check ch341 driver")

    def open_device(self):
        self.iIndex = self.dll.CH34xOpenDevice("/dev/ch34x_pis0".encode())
        return self.iIndex

    def close_device(self):
        self.dll.CH34xCloseDevice(self.iIndex)

    def get_version(self):
        return self.dll.CH34xGetVersion()

    def get_driver_version(self):
        return self.dll.CH34xGetDrvVersion() 

    def get_chip_version(self):
        ver_str = create_string_buffer(1)
        self.dll.CH34x_GetChipVersion(self.iIndex, ver_str)
        return int.from_bytes(ver_str[0], byteorder='big')

    def set_stream(self, cs):
        if cs == True:
            self.dll.CH34xSetStream(self.iIndex, 0x80)
        else:
            self.dll.CH34xSetStream(self.iIndex, 0x81)

    def stream_spi4(self, command, ilength, iobuffer):
        self.dll.CH34xStreamSPI4(
            self.iIndex, command, ilength, iobuffer)

    def set_output(self, a, b, c):
        self.dll.CH34xSetOutput(self.iIndex, a, b, c)

    def read_I2C(self, addr_fpga_device, addr, iobuffer):
        # this function does not exist?
        self.dll.CH34xReadI2C(0, addr_fpga_device, addr, iobuffer)

    def write_I2C(self, addr_usb_write_fpga_device, addr, byte):
        # this function does not exist?
        self.dll.CH34xWriteI2C(0, addr_usb_write_fpga_device, addr, byte)

    def set_delay_ms(self, ms):
        self.dll.CH34xSetDelaymS(self.iIndex, ms)



class ch341_class(object):

    def __init__(self):
        FW_5680SIZE = 65536
        FW_FPGASIZE = 2*1024*1024
        FW_8339SIZE = 10*1024*1024
        self.fw_5680_size = 0
        self.fw_5680_buf = create_string_buffer(FW_5680SIZE)
        self.fw_fpga_size = 0
        self.fw_fpga_buf = create_string_buffer(FW_FPGASIZE)
        self.fw_8339_size = 0
        self.fw_8339_buf = create_string_buffer(FW_8339SIZE)

        self.dll_object = None
        self.target = -1
        self.status = ch341_status.IDLE.value        # idle
        self.read_setting_flag = 1

        self.reconnect_vtx = 0

        # ------ monitor -------------
        self.addr_brightness = 0x22
        self.addr_contrast = 0x23
        self.addr_saturation = 0x24
        self.addr_backlight = 0x25
        self.addr_cell_count = 0x26
        self.addr_warning_cell_voltage = 0x27
        self.addr_osd = 0x28
        self.addr_fpga_device = 0x65  # 7bit address

        self.target_id = 0
        self.fw_path = ""

        self.written_len = 0
        self.to_write_len = 100

        self.monitor_connected = 0
        self.iolength = 6
        self.iobuffer = create_string_buffer(65544)
        self.rdbuffer = [0] * 256
        self.write_crc = 0
        self.read_crc = 0

        # --------- event vrx ------------------------
        self.WRITE_ENABLE = 0x06
        self.WRITE_DISABLE = 0x04
        self.READ_STATUS_REG1 = 0x05
        self.READ_STATUS_REG2 = 0x35
        self.READ_DATA = 0x03
        self.EWSR = 0x50
        self.FAST_READ = 0x0B
        self.PAGE_PROGRAM = 0x02  # Byte Prog Mode
        self.SECTOR_ERASE_4K = 0x20  # Erase 4 KByte of memory array
        self.BLOCK_ERASE_32K = 0x52  # Erase 32 KByte block of memory array
        self.BLOCK_ERASE_64K = 0xD8  # Erase 64 KByte block of memory array
        self.CHIP_ERASE = 0xC7  # Erase one chip flash
        self.SELECT_FPGA_5680 = 0x80
        self.FLASH_STATUS = 0x05  # read flash status
        self.FLASH_SET_5680 = 0xffff40ff
        self.FLASH_SET_FPGA = 0xffff80ff
        self.FLASH_BASE_ADDR = 0x00

        self.buffer_size = 2560
        self.write_buffer = create_string_buffer(self.buffer_size)

        if sys.platform.startswith('linux'):
            self.dll_object = linux_driver()
        else:
            self.dll_object = windows_driver()

        self.dll_object.load()

    def parse_monitor_fw(self, fw_path):
        try:
            with open(fw_path, "rb") as file:
                file.seek(2)
                self.fw_5680_size = int.from_bytes(
                    file.read(4), byteorder='little')
                self.fw_fpga_size = int.from_bytes(
                    file.read(4), byteorder='little')
                self.fw_8339_size = int.from_bytes(
                    file.read(4), byteorder='little')
                if self.fw_5680_size < 65536 and self.fw_fpga_size < 10000000 and self.fw_8339_size < 10000000:
                    self.fw_5680_buf = file.read(self.fw_5680_size)
                    self.fw_fpga_buf = file.read(self.fw_fpga_size)
                    self.fw_8339_buf = file.read(self.fw_8339_size)
                    return 1
                else:
                    return 0
        except:
            return 0

    def parse_event_vrx_fw(self, fw_path):
        try:
            with open(fw_path, "rb") as file:
                file_size = os.path.getsize(fw_path)
                head_size = file.read(8)
                self.fw_5680_size = int(head_size) - 2560
                self.fw_fpga_size = file_size - 8 - self.fw_5680_size
                if self.fw_5680_size < 65536 and self.fw_fpga_size < 10000000:
                    return 1
                else:
                    return 0
        except:
            return 0

    def ch341read_i2c(self, addr):
        self.dll_object.read_I2C(self.addr_fpga_device, addr, self.iobuffer)
        return int.from_bytes(self.iobuffer[0], byteorder='big')

    def read_setting(self):
        global_var.brightness = self.ch341read_i2c(self.addr_brightness)
        global_var.contrast = self.ch341read_i2c(self.addr_contrast)
        global_var.saturation = self.ch341read_i2c(self.addr_saturation)
        global_var.backlight = self.ch341read_i2c(self.addr_backlight)
        global_var.cell_count = self.ch341read_i2c(self.addr_cell_count)
        global_var.warning_cell_voltage = self.ch341read_i2c(
            self.addr_warning_cell_voltage)
        global_var.osd = self.ch341read_i2c(self.addr_osd)
        
        fpga_version = self.ch341read_i2c(0xff)
        print(f"cell:{global_var.cell_count:d} warning_cell:{global_var.warning_cell_voltage:d} fpga_version:0x{fpga_version:2x}")

    def set_stream(self, cs):
        self.dll_object.set_stream(cs)

    def stream_spi4(self):
        self.dll_object.stream_spi4(0x80, self.ilength, self.iobuffer)

    def flash_switch0(self):
        self.dll_object.set_output(0x03, 0x0000FF00, 0x4300)

    def flash_switch1(self):
        self.dll_object.set_output(0x03, 0x0000FF00, 0x8300)

    def flash_switch2(self):
        self.dll_object.set_output(0x03, 0x0000FF00, 0xc800)

    def flash_release(self):
        self.dll_object.set_output(0x03, 0x0000FF00, 0xc200)

    def flash_read_id(self):
        self.iobuffer[0] = 0x9f
        self.iobuffer[1] = 0x9f
        self.iobuffer[2] = 0x9f
        self.iobuffer[3] = 0x9f
        self.iobuffer[4] = 0x9f
        self.iobuffer[5] = 0x9f
        self.ilength = 6

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)

        return int.from_bytes(self.iobuffer[1], byteorder='big') * 256 * 256 \
            + int.from_bytes(self.iobuffer[2], byteorder='big') * 256 \
            + int.from_bytes(self.iobuffer[3], byteorder='big')

    def flash_write_enable(self):
        self.iobuffer[0] = 0x06
        self.ilength = 1

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)

    def flash_erase_block64(self):
        self.iobuffer[0] = 0xd8
        self.iobuffer[1] = 0
        self.iobuffer[2] = 0
        self.iobuffer[3] = 0
        self.ilength = 4

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)

    def flash_erase_block64_m(self, addr):
        self.iobuffer[0] = 0xd8
        self.iobuffer[1] = (addr >> 16) & 0xff
        self.iobuffer[2] = (addr >> 8) & 0xff
        self.iobuffer[3] = (addr >> 0) & 0xff
        self.ilength = 4

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)

    def flash_erase_section(self, addr):
        self.iobuffer[0] = 0x20
        self.iobuffer[1] = (addr >> 16) & 0x1f
        self.iobuffer[2] = (addr >> 8) & 0x1f
        self.iobuffer[3] = (addr >> 0) & 0x1f
        self.ilength = 4

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)

    def flash_write_disable(self):
        self.iobuffer[0] = 0x04
        self.ilength = 1

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)

    def flash_is_busy(self):
        self.iobuffer[0] = 0x05
        self.iobuffer[1] = 0x00
        self.ilength = 2

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)

        return (int.from_bytes(self.iobuffer[1], byteorder='little') & 1)

    def flash_erase_flash(self, block):
        self.flash_write_enable()
        self.flash_erase_block64_m(block)
        self.flash_wait_busy()
        self.flash_write_disable()

    def flash_wait_busy(self):
        while True:
            if self.flash_is_busy() == 0:
                return

    def flash_erase_vtx(self):
        self.flash_write_enable()
        self.flash_erase_block64()
        self.flash_wait_busy()
        self.flash_write_disable()

        self.flash_write_enable()
        self.flash_erase_section(65536)
        self.flash_wait_busy()
        self.flash_write_disable()

    def flash_write_page(self, base_address, length, fw):
        self.iobuffer[0] = 0x02
        self.iobuffer[1] = (base_address >> 16) & 0xff
        self.iobuffer[2] = (base_address >> 8) & 0xff
        self.iobuffer[3] = (base_address >> 0) & 0xff
        self.ilength = 4 + length

        for i in range(length):
            try:
                self.iobuffer[4+i] = fw[i]
            except:
                self.iobuffer[4+i] = 0xff

            self.write_crc += int.from_bytes(
                self.iobuffer[4 + i], byteorder='little')

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)

    def flash_read_page(self, base_address, length):
        self.iobuffer[0] = 0x03
        self.iobuffer[1] = (base_address >> 16) & 0xff
        self.iobuffer[2] = (base_address >> 8) & 0xff
        self.iobuffer[3] = (base_address >> 0) & 0xff
        self.ilength = 4 + length

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)

        for i in range(256):
            self.read_crc += int.from_bytes(
                self.iobuffer[4 + i], byteorder='little')

    def flash_read_file(self):
        self.read_crc = 0
        self.crc_table = dict()

        buffer = bytes()
        dump = open('dump.bin', 'wb')

        for page in range(256):
            baseAddress = page << 8

            self.iobuffer[0] = 0x03
            self.iobuffer[1] = (baseAddress >> 16) & 0xff
            self.iobuffer[2] = (baseAddress >> 8) & 0xff
            self.iobuffer[3] = baseAddress & 0xff
            self.iobuffer[4] = 0x00
            self.ilength = 260

            self.set_stream(0)
            self.stream_spi4()
            self.set_stream(1)

            for i in range(0, 256):
                self.read_crc += int.from_bytes(
                    self.iobuffer[4 + i], byteorder='big')
                self.read_crc &= 0xffff
                buffer += self.iobuffer[4 + i]
            self.crc_table[page+1] = "0x"+hex(zlib.crc32(buffer) & 0xffffffff)[2:].rjust(8, '0')

        dump.write(buffer)
        dump.close()

    def connect_vtx(self):
        if self.dll_object.open_device() < 0:
            return 0
        else:
            # needed on Linux
            if self.dll_object.get_chip_version() == 0:
                return 0

            self.flash_switch0()
            flash_id_0 = self.flash_read_id()
            self.flash_switch1()
            flash_id_1 = self.flash_read_id()
            self.flash_switch2()
            flash_id_2 = self.flash_read_id()
            if flash_id_0 == flash_id_1 and flash_id_1 == flash_id_2:
                if flash_id_0 == 0xEF4014 or flash_id_0 == 0x5E6014:
                    return 1

            return 0

    def flash_read_target_id(self):
        raddr = 0x10000
        self.iobuffer[0] = 0x03
        self.iobuffer[1] = (raddr >> 16) & 0xff
        self.iobuffer[2] = (raddr >> 8) & 0xff
        self.iobuffer[3] = raddr & 0xff
        self.iobuffer[4] = 0x00
        self.ilength = 16

        self.set_stream(0)
        self.stream_spi4()
        self.set_stream(1)

        return int.from_bytes(self.iobuffer[4], byteorder='big')

    def flash_write_target_id(self):
        self.flash_write_enable()
        self.flash_write_page(65536, 1, [self.target_id])
        self.flash_write_disable()
        self.flash_wait_busy()

    def flash_write_fw(self):
        size = os.path.getsize(self.fw_path)
        file = open(self.fw_path, "rb")
        fw = file.read()

        page_number = (size + (1 << 8) - 1) >> 8
        self.write_crc = 0
        self.read_crc = 0

        for page in range(page_number):
            base_address = page << 8
            self.flash_write_enable()
            self.flash_write_page(base_address, 256, fw[base_address:])
            self.flash_write_disable()
            self.flash_wait_busy()
            
            self.flash_read_page(base_address, 256)
            
            my_ch341.written_len += 256
        
        if self.write_crc == self.read_crc:
            return 1
        else:
            return 0

    def connect_monitor(self, sleep_sec):
        if self.dll_object.open_device() < 0:
            return 0
        else:
            # self.dll.CH341SetStream(0, 0x82)
            time.sleep(sleep_sec)
            self.flash_switch1()
            flash_id_2 = self.flash_read_id()
            if flash_id_2 == 0xEF4018:
                return 1
            else:
                return 0

    def fw_write_to_flash(self, fw_buf, fw_size):
        page_number = (fw_size + (1 << 8) - 1) >> 8
        for page in range(page_number):
            block = page << 8
            if (block & 0xffff) == 0:
                self.flash_erase_flash(block)

            base_address = page << 8
            self.flash_write_enable()
            self.flash_write_page(base_address, 256, fw_buf[base_address:])
            self.flash_write_disable()
            self.flash_wait_busy()
            my_ch341.written_len += 256
        """
        for page in range(page_number):
            base_address = page << 8
            self.flash_read_page(base_address, 256)
            
            for i in range(256):
                self.read_crc += int.from_bytes(self.rdbuffer[i], byteorder='little')
        """

    # ---------------- event_vrx --------------------------------
    def connect_event_vrx(self):
        if self.dll_object.open_device() < 0:
            return 0
        else:
            self.dll_object.set_stream(0)
            return 1

    def FlashChipErase(self):
        self.dll_object.set_stream(1)

        self.iobuffer[0] = self.WRITE_ENABLE
        self.dll_object.stream_spi4(
            self.SELECT_FPGA_5680, 1, self.iobuffer)

        self.iobuffer[0] = self.CHIP_ERASE
        self.dll_object.stream_spi4(
            self.SELECT_FPGA_5680, 1, self.iobuffer)

        self.iobuffer[0] = self.WRITE_DISABLE
        self.dll_object.stream_spi4(
            self.SELECT_FPGA_5680, 1, self.iobuffer)

    def data_cpy(self, dest, dst_off, src, src_off, length):
        for i in range(length):
            dest[dst_off+i] = src[src_off+i]

    def write_SPI(self, addr, data_buf, size):
        temp_write_buffer = create_string_buffer(int(PAGE_SIZE+HEAD_SIZE))
        self.dll_object.set_stream(1)

        page = 0
        while size > PAGE_SIZE:
            temp_write_buffer[0] = self.WRITE_ENABLE
            self.dll_object.stream_spi4(
                self.SELECT_FPGA_5680, 1, temp_write_buffer)

            temp_write_buffer[0] = self.PAGE_PROGRAM
            temp_write_buffer[1] = ((addr & 0xFF0000) >> 16)
            temp_write_buffer[2] = ((addr & 0x00FF00) >> 8)
            temp_write_buffer[3] = (addr & 0x0000FF)

            self.data_cpy(temp_write_buffer, HEAD_SIZE, data_buf,
                          (page * PAGE_SIZE), PAGE_SIZE)
            self.dll_object.stream_spi4(self.SELECT_FPGA_5680, int(
                PAGE_SIZE+HEAD_SIZE), temp_write_buffer)

            temp_write_buffer[0] = self.WRITE_DISABLE
            self.dll_object.stream_spi4(
                self.SELECT_FPGA_5680, 1, temp_write_buffer)
            self.dll_object.set_delay_ms(2)

            size -= PAGE_SIZE
            page += 1
            addr += PAGE_SIZE

        temp_write_buffer[0] = self.WRITE_ENABLE
        self.dll_object.stream_spi4(
            self.SELECT_FPGA_5680, 1, temp_write_buffer)

        temp_write_buffer[0] = self.PAGE_PROGRAM
        temp_write_buffer[1] = ((addr & 0xFF0000) >> 16)
        temp_write_buffer[2] = ((addr & 0x00FF00) >> 8)
        temp_write_buffer[3] = (addr & 0x0000FF)
        if size < PAGE_SIZE:
            self.data_cpy(temp_write_buffer, HEAD_SIZE,
                          data_buf, (page * PAGE_SIZE), size)
        else:
            self.data_cpy(temp_write_buffer, HEAD_SIZE, data_buf,
                          (page * PAGE_SIZE), PAGE_SIZE)

        self.dll_object.stream_spi4(self.SELECT_FPGA_5680, int(
            PAGE_SIZE+HEAD_SIZE), temp_write_buffer)

        temp_write_buffer[0] = self.WRITE_DISABLE
        self.dll_object.stream_spi4(
            self.SELECT_FPGA_5680, 1, temp_write_buffer)

    def write_event_vrx_fw_to_flash(self, path):
        file = open(path, "rb")
        file_size = os.path.getsize(path)   # file_size: 2383867
        head_size = file.read(8)
        file5680_size = int(head_size) - 2560    # 58581 = 64141 - 2560
        print("file: ", path)

        # erase 5680 flash
        my_ch341.written_len += 15 * PAGE_SIZE
        self.dll_object.set_output(0x03, 0xffffffff, self.FLASH_SET_5680)
        time.sleep(0.01)
        self.FlashChipErase()
        my_ch341.written_len += 15 * PAGE_SIZE
        time.sleep(1)

        # erase fpga flash
        self.dll_object.set_output(0x03, 0xffffffff, self.FLASH_SET_FPGA)
        time.sleep(0.01)
        self.FlashChipErase()
        my_ch341.written_len += 15 * PAGE_SIZE
        # time.sleep(65)  # Wait for all flash erase to be completed
        for i in range(65):
            time.sleep(1)
            my_ch341.written_len += 10 * PAGE_SIZE

        # write 5680 data to flash
        self.dll_object.set_output(0x03, 0xffffffff, self.FLASH_SET_5680)
        time.sleep(0.01)
        file.seek(8)

        page = 0
        while page * self.buffer_size < file5680_size:
            self.write_buffer = file.read(self.buffer_size)
            self.write_SPI(self.FLASH_BASE_ADDR + (page * self.buffer_size),
                           self.write_buffer, len(self.write_buffer))
            my_ch341.written_len += 15 * PAGE_SIZE
            time.sleep(0.1)
            page += 1

        # write 5680 last page data
        page -= 1
        self.write_buffer = file.read(
            file5680_size - (page * self.buffer_size))
        self.write_SPI(self.FLASH_BASE_ADDR + (page + 1) * self.buffer_size,
                       self.write_buffer, file5680_size - (page * self.buffer_size))
        time.sleep(1)
        my_ch341.written_len += 15 * PAGE_SIZE

        # write fpga data to flash
        self.dll_object.set_output(0x03, 0xffffffff, self.FLASH_SET_FPGA)
        page = 0
        while True:
            self.write_buffer = file.read(self.buffer_size)
            self.write_SPI(self.FLASH_BASE_ADDR + (page * self.buffer_size),
                           self.write_buffer, len(self.write_buffer))
            time.sleep(0.1)
            my_ch341.written_len += 9 * PAGE_SIZE

            page += 1
            if len(self.write_buffer) != self.buffer_size:
                break

        file.flush()
        file.close()
        self.dll_object.set_output(0x03, 0xffffffff, self.FLASH_SET_FPGA)


my_ch341 = ch341_class()


def ch341_thread_proc():
    while True:
        if my_ch341.status == ch341_status.STATUS_EXIT.value:
            sys.exit()

        if my_ch341.status == ch341_status.VTX_DISCONNECTED.value:  # connect vtx
            if my_ch341.connect_vtx() == 1:
                my_ch341.status = ch341_status.VTX_CONNECTED.value

        elif my_ch341.status == ch341_status.VTX_UPDATE.value:  # update vtx
            my_ch341.written_len = 0
            my_ch341.to_write_len = os.path.getsize(my_ch341.fw_path)

            if my_ch341.to_write_len == 0 or my_ch341.to_write_len >= 65536:  # check fw size
                my_ch341.status = ch341_status.VTX_FW_ERROR.value
            else:
                my_ch341.flash_erase_vtx()
                my_ch341.flash_write_target_id()
                if my_ch341.flash_write_fw() == 1:
                    my_ch341.status = ch341_status.VTX_UPDATEDONE.value
                else:
                    my_ch341.status = ch341_status.VTX_UPDATE_FAILED.value
                my_ch341.reconnect_vtx = 0
        elif my_ch341.status == ch341_status.VTX_RECONNECT.value:  # reconnect vtx
            if my_ch341.reconnect_vtx == 0:
                my_ch341.dll_object.close_device()
                if my_ch341.connect_vtx() == 0:
                    my_ch341.reconnect_vtx = 1
            elif my_ch341.reconnect_vtx == 1:
                my_ch341.dll_object.close_device()
                if my_ch341.connect_vtx() == 1:
                    my_ch341.reconnect_vtx = 0
                    my_ch341.status = ch341_status.VTX_RECONNECTDONE.value

        # -------- Monitor -----------------
        elif my_ch341.status == ch341_status.MONITOR_CHECK_ALIVE.value:  # check monitor is alive
            if my_ch341.connect_monitor(0.35) == 1:
                if my_ch341.monitor_connected == 0:
                    time.sleep(0.5)
                    my_ch341.read_setting()
                    my_ch341.monitor_connected = 1
            else:
                my_ch341.monitor_connected = 0

        elif my_ch341.status == ch341_status.MONITOR_UPDATE.value:  # update monitor
            # check fw size
            if my_ch341.parse_monitor_fw(my_ch341.fw_path) == 0:
                my_ch341.status = ch341_status.MONITOR_FW_ERROR.value
            else:
                my_ch341.flash_switch0()
                my_ch341.fw_write_to_flash(
                    my_ch341.fw_5680_buf, my_ch341.fw_5680_size)
                my_ch341.flash_switch1()
                my_ch341.fw_write_to_flash(
                    my_ch341.fw_fpga_buf, my_ch341.fw_fpga_size)
                my_ch341.flash_switch2()
                my_ch341.fw_write_to_flash(
                    my_ch341.fw_8339_buf, my_ch341.fw_8339_size)
                my_ch341.dll_object.close_device()
                my_ch341.flash_release()
                my_ch341.status = ch341_status.MONITOR_UPDATEDONE.value

        # ---------------------- event_vrx ------------------------------------
        elif my_ch341.status == ch341_status.EVENT_VRX_DISCONNECTED.value:  # connect event vrx
            if my_ch341.connect_event_vrx() == 1:
                my_ch341.status = ch341_status.EVENT_VRX_CONNECTED.value

        elif my_ch341.status == ch341_status.EVENT_VRX_UPDATE.value:  # update event_vrx
            file = open(my_ch341.fw_path, "rb")
            file_size = os.path.getsize(my_ch341.fw_path)
            head_size = file.read(8)
            try:
                file5680_size = int(head_size) - 2560
            except:
                file5680_size = 65536
                my_ch341.status = ch341_status.EVENT_VRX_FW_ERROR.value

            file.close()
            if file_size > 10000000 or file5680_size >= 65536:
                my_ch341.status = ch341_status.EVENT_VRX_FW_ERROR.value
            else:
                my_ch341.write_event_vrx_fw_to_flash(my_ch341.fw_path)
                my_ch341.status = ch341_status.EVENT_VRX_UPDATEDONE.value
        else:
            time.sleep(0.1)
