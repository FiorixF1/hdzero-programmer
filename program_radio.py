import serial
import serial.tools.list_ports
import time
import esptool
import sys
from xmodem import XMODEM


def flash_esp_api(port, baud, chip, flash_args):
    """Program an ESP-family target through esptool."""
    argv = ["--chip", chip, "--port", port, "--baud", str(baud), "write-flash"]
    for addr, path in flash_args:
        argv.extend((hex(addr), path))

    old_argv = sys.argv
    try:
        sys.argv = ["esptool.py"] + argv
        esptool.main()
        return True
    except (Exception, SystemExit) as exc:
        print(f"ESP flash failed on {port}: {exc}")
        return False
    finally:
        sys.argv = old_argv


class radio_class(object):
    def __init__(self):
        self.ser = None
        self.status = 0
        self.com = ""

    def find_word_in_string(self, value, word):
        if not isinstance(value, str):
            return 0
        return int(word in value.split())

    def _close_serial(self):
        """Close the currently held serial port, if any."""
        ser = self.ser
        self.ser = None
        if ser is not None:
            try:
                if ser.is_open:
                    ser.close()
            except Exception as exc:
                print(f"Radio serial close failed: {exc}")

    def close(self):
        self._close_serial()

    def serial_tx(self, value):
        self.ser.write(value.encode("utf-8"))

    def serial_rx(self, sleep_sec):
        time.sleep(sleep_sec)
        if self.ser is None:
            return ""
        chunks = []
        while self.ser.in_waiting:
            chunks.append(self.ser.read(self.ser.in_waiting))
        return b"".join(chunks).decode("utf-8", errors="replace")

    def getc(self, size, timeout=1):
        if self.ser is None:
            return None
        return self.ser.read(size)

    def putc(self, data, timeout=1):
        if self.ser is None:
            return 0
        return self.ser.write(data)

    def _search_port(self, description_token):
        # Do not leave a previous port open while changing operating modes.
        self._close_serial()
        for port_info in serial.tools.list_ports.comports():
            if description_token not in (port_info.description or ""):
                continue
            self.com = port_info.device or port_info.name
            time.sleep(0.25)
            try:
                self.ser = serial.Serial(self.com, 115200, timeout=2)
                return 1
            except (serial.SerialException, OSError) as exc:
                print(f"Unable to open radio port {self.com}: {exc}")
                self._close_serial()
        return 0

    def search_stm32_port(self):
        return self._search_port("STMicroelectronics")

    def search_elrs_port(self):
        return self._search_port("CH340")

    def unzip_radio_firmware(self, file_path, dest_folder):
        import zipfile
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(dest_folder)

    def radio_is_active(self):
        if self.search_stm32_port() == 0:
            return 0
        try:
            self.ser.write(b"ATPING\r\n")
            rx = self.serial_rx(1)
            return 1 if self.find_word_in_string(rx, "HDZero") else 2
        except Exception as exc:
            print(f"Radio detection failed: {exc}")
            return 0
        finally:
            self._close_serial()

    def program_stm32(self):
        # Ask the radio controller to reboot into its STM32 bootloader.
        if self.search_stm32_port() == 0:
            return False
        try:
            command = b"ATPROG\r\n"
            self.ser.write(command * 3)
            time.sleep(0.5)
        except Exception as exc:
            print(f"Unable to enter STM32 bootloader: {exc}")
            return False
        finally:
            self._close_serial()

        time.sleep(0.5)
        if self.search_stm32_port() == 0:
            return False

        try:
            time.sleep(0.2)
            self.ser.write(b"XXX" * 3)
            time.sleep(0.5)
            self.serial_rx(0)
            with open("resource/hdzero_radio_stm32.bin", "rb") as stream:
                modem = XMODEM(self.getc, self.putc)
                if not modem.send(stream):
                    print("XMODEM transfer of STM32 firmware failed")
                    return False
            self.ser.write(b"ccc" * 3)
            time.sleep(0.5)
            return True
        except Exception as exc:
            print(f"STM32 firmware update failed: {exc}")
            return False
        finally:
            self._close_serial()

    def _program_elrs(self, command, chip, flash_args):
        if self.search_stm32_port() == 0:
            return False
        try:
            self.ser.write((command + "\r\n").encode("ascii"))
            time.sleep(0.2)
        except Exception as exc:
            print(f"Unable to switch Radio to {chip} bootloader: {exc}")
            return False
        finally:
            self._close_serial()

        time.sleep(1)
        if self.search_elrs_port() == 0:
            return False
        # esptool opens the port itself; release our discovery handle first.
        port = self.com
        self._close_serial()
        return flash_esp_api(
            port=port,
            baud=460800,
            chip=chip,
            flash_args=flash_args,
        )

    def program_elrs_tx(self):
        return self._program_elrs(
            "ATPGTX",
            "esp32",
            [
                (0x1000, "resource/elrs_tx/bootloader.bin"),
                (0x8000, "resource/elrs_tx/partitions.bin"),
                (0xe000, "resource/elrs_tx/boot_app0.bin"),
                (0x10000, "resource/elrs_tx/firmware.bin"),
            ],
        )

    def program_elrs_backpack(self):
        return self._program_elrs(
            "ATPGBP",
            "esp32c3",
            [
                (0x0000, "resource/elrs_backpack/bootloader.bin"),
                (0x8000, "resource/elrs_backpack/partitions.bin"),
                (0xe000, "resource/elrs_backpack/boot_app0.bin"),
                (0x10000, "resource/elrs_backpack/firmware.bin"),
            ],
        )


my_radio = radio_class()
