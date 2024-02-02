from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import HORIZONTAL, VERTICAL, ttk, StringVar
from tkinter import filedialog
import Download
from ch341_wrapper import *
import sys

from icon32 import icon32
import base64
import io

import zipfile

version = "1.0.2"


def getFirmwareFromCRC(crc_table):
    firmware_list = {
        "hdzero_freestyle_v1 @ 1.0.0": {
            "pageNum": 187,
            "read_crc": "0x2c7871ad",
        },
        "hdzero_race_v1 @ 1.0.0": {
            "pageNum": 183,
            "read_crc": "0xed18964a",
        },
        "hdzero_race_v2 @ 1.0.0": {
            "pageNum": 183,
            "read_crc": "0xf88dc480",
        },
        "hdzero_whoop @ 1.0.0": {
            "pageNum": 172,
            "read_crc": "0xa9649ace",
        },
        "hdzero_whoop_lite @ 1.0.0": {
            "pageNum": 182,
            "read_crc": "0xaeed4934",
        },
        "hdzero_freestyle_v1 @ 1.1.0": {
            "pageNum": 188,
            "read_crc": "0xa36937e4",
        },
        "hdzero_race_v1 @ 1.1.0": {
            "pageNum": 184,
            "read_crc": "0xb3c0e07a",
        },
        "hdzero_race_v2 @ 1.1.0": {
            "pageNum": 184,
            "read_crc": "0x153f831e",
        },
        "hdzero_whoop @ 1.1.0": {
            "pageNum": 172,
            "read_crc": "0x98ba4b29",
        },
        "hdzero_whoop_lite @ 1.1.0": {
            "pageNum": 183,
            "read_crc": "0x30758bc7",
        },
        "hdzero_freestyle_v1 @ 1.2.0": {
            "pageNum": 195,
            "read_crc": "0xc31a3596",
        },
        "hdzero_race_v1 @ 1.2.0": {
            "pageNum": 191,
            "read_crc": "0x4b4d7aeb",
        },
        "hdzero_race_v2 @ 1.2.0": {
            "pageNum": 191,
            "read_crc": "0x5d6d7f88",
        },
        "hdzero_whoop @ 1.2.0": {
            "pageNum": 180,
            "read_crc": "0xa97b865d",
        },
        "hdzero_whoop_lite @ 1.2.0": {
            "pageNum": 190,
            "read_crc": "0x90957a34",
        },
        "foxeer_vtx @ 1.3.0": {
            "pageNum": 195,
            "read_crc": "0x47be5d3a",
        },
        "hdzero_freestyle_v1 @ 1.3.0": {
            "pageNum": 200,
            "read_crc": "0xdc45f45f",
        },
        "hdzero_race_v1 @ 1.3.0": {
            "pageNum": 195,
            "read_crc": "0x1c4220a0",
        },
        "hdzero_race_v2 @ 1.3.0": {
            "pageNum": 195,
            "read_crc": "0x1207d32d",
        },
        "hdzero_race_v3 @ 1.3.0": {
            "pageNum": 190,
            "read_crc": "0x0894030d",
        },
        "hdzero_whoop @ 1.3.0": {
            "pageNum": 184,
            "read_crc": "0xf2297c3f",
        },
        "hdzero_whoop_lite @ 1.3.0": {
            "pageNum": 195,
            "read_crc": "0x4a873a8b",
        },
        "foxeer_vtx @ 1.4.0": {
            "pageNum": 200,
            "read_crc": "0x2b758ebd",
        },
        "hdzero_freestyle_v1 @ 1.4.0": {
            "pageNum": 205,
            "read_crc": "0xdbb9c87f",
        },
        "hdzero_race_v1 @ 1.4.0": {
            "pageNum": 200,
            "read_crc": "0xa3ca64bd",
        },
        "hdzero_race_v2 @ 1.4.0": {
            "pageNum": 199,
            "read_crc": "0x40a5716b",
        },
        "hdzero_race_v3 @ 1.4.0": {
            "pageNum": 195,
            "read_crc": "0xa9925181",
        },
        "hdzero_whoop @ 1.4.0": {
            "pageNum": 189,
            "read_crc": "0x69bdd828",
        },
        "hdzero_whoop_lite @ 1.4.0": {
            "pageNum": 200,
            "read_crc": "0x785b02f5",
        },
        "foxeer_vtx @ 1.5.0": {
            "pageNum": 207,
            "read_crc": "0xed2133b3",
        },
        "hdzero_freestyle_v1 @ 1.5.0": {
            "pageNum": 212,
            "read_crc": "0xfad37aba",
        },
        "hdzero_freestyle_v2 @ 1.5.0": {
            "pageNum": 213,
            "read_crc": "0xfe479852",
        },
        "hdzero_race_v1 @ 1.5.0": {
            "pageNum": 207,
            "read_crc": "0xdfe1f8d4",
        },
        "hdzero_race_v2 @ 1.5.0": {
            "pageNum": 207,
            "read_crc": "0x602030a7",
        },
        "hdzero_race_v3 @ 1.5.0": {
            "pageNum": 201,
            "read_crc": "0xc31605fd",
        },
        "hdzero_whoop @ 1.5.0": {
            "pageNum": 197,
            "read_crc": "0x855da136",
        },
        "hdzero_whoop_lite @ 1.5.0": {
            "pageNum": 207,
            "read_crc": "0x7f1a74be",
        },
        "foxeer_vtx @ 1.5.0-CITA": {
            "pageNum": 195,
            "read_crc": "0x1b06017f",
        },
        "hdzero_race_v1 @ 1.5.0-CITA": {
            "pageNum": 195,
            "read_crc": "0x815fb9a6",
        },
        "hdzero_race_v2 @ 1.5.0-CITA": {
            "pageNum": 194,
            "read_crc": "0x9c95b6c1",
        },
        "hdzero_race_v3 @ 1.5.0-CITA": {
            "pageNum": 195,
            "read_crc": "0xe966412a",
        },
        "hdzero_whoop @ 1.5.0-CITA": {
            "pageNum": 195,
            "read_crc": "0x193c4a95",
        },
        "hdzero_whoop_lite @ 1.5.0-CITA": {
            "pageNum": 195,
            "read_crc": "0xc6162081",
        },
    }
    for firmware, metadata in firmware_list.items():
        if crc_table[metadata["pageNum"]] == metadata["read_crc"]:
            if firmware.endswith("CITA"):
                return firmware + "\nFirmware is valid"
            else:
                return firmware + "\nFirmware is NOT valid"
    else:
        return "Unknown firmware" + "\nFirmware is NOT valid"

class MyGUI:
    def __init__(self, master):
        self.master = master

        self.SelectedFirmwareString = ''
        self.target = 0
        self.targetNameString = tk.StringVar()

        self.ver_combobox = None
        self.target_combobox = None
        self.auto_btn = None
        self.prog_state = None
        self.vtx_state = None
        self.fw_state = None
        self.refresh_btn = None
        self.update_btn = None
        self.load_fw_online_btn = None
        self.load_fw_local_btn = None
        self.init_done = 0
        self.downloadCommand = 0
        self.ch341Command = 0

        self.updateCnt = 0

        self.ver_index_select = 0
        self.vtx_index_select = 0
        self.ver_name_select = ""
        self.vtx_name_select = ""

        self.create_root_window()
        self.create_version_combobox()
        self.switch_version_action()
        self.create_target_combobox()
        self.switch_target_action()
        self.create_refresh_btn()
        self.create_auto_detect_btn()
        self.create_load_firmnware_online_btn()
        self.create_load_firmnware_local_btn()
        self.create_update_button()
        self.create_fw_state()
        self.create_prog_state()
        self.create_vtx_state()
        self.create_progressbar()

    def create_root_window(self):
        titleString = "HDZero Programmer"+" v"+version+" CITA"
        windowX = 450
        windowY = 170
        offsetX = (self.master.winfo_screenwidth() - windowX)/2
        offsetY = (self.master.winfo_screenheight() - windowY)/2
        self.master.geometry('%dx%d+%d+%d' %
                             (windowX, windowY, offsetX, offsetY))
        self.master.resizable(False, False)
        self.master.title(titleString)
        self.master.configure(bg="#303030")

        icon_base64 = base64.b64decode(icon32)
        icon_bytes = io.BytesIO(icon_base64)
        icon = tk.PhotoImage(data=icon_bytes.getvalue())

        self.master.iconphoto(True, icon)

    def create_version_combobox(self):
        self.ver_combobox = ttk.Combobox(self.master, state='readonly')
        self.ver_combobox.anchor = 'NW'
        self.ver_combobox.place(width=200, height=24, x=20, y=20)

        self.ver_combobox['value'] = Download.version_list
        self.ver_combobox.current(0)

    def create_target_combobox(self):
        self.target_combobox = ttk.Combobox(self.master, state='readonly')
        self.target_combobox.anchor = 'NW'
        self.target_combobox.place(width=200, height=24, x=20, y=50)
        self.target_combobox['value'] = Download.vtx_name_list[0]
        self.target_combobox.current(0)

    def reset_fw_state(self):
        self.fw_state.config(text="FW:")
        self.fw_state.config(background="#a0a0a0")

    def auto_detect_btn_callback(event):
        global my_gui
        ch341.command = 1
        my_gui.ch341Command = 1
        my_gui.reset_fw_state()

    def create_auto_detect_btn(self):
        self.auto_btn = ttk.Button(
            self.master, text='Auto detect', command=self.auto_detect_btn_callback)
        self.auto_btn.anchor = 'NW'
        self.auto_btn.place(width=80, height=24, x=240, y=50)

    def refresh_btn_callback(event):
        global my_gui
        Download.downloadCommand = 1
        my_gui.downloadCommand = 1
        my_gui.vtx_index_select = 0
        my_gui.ver_index_select = 0
        # my_gui.refresh_btn.config(state=tk.DISABLED)
        # my_gui.load_fw_online_btn.config(state=tk.DISABLED)
        # my_gui.load_fw_local_btn.config(state=tk.DISABLED)
        # my_gui.ver_combobox.config(state=tk.DISABLED)
        # my_gui.target_combobox.config(state=tk.DISABLED)
        # my_gui.update_btn.config(state=tk.DISABLED)
        # my_gui.auto_btn.config(state=tk.DISABLED)

    def create_refresh_btn(self):
        self.refresh_btn = ttk.Button(
            self.master, text='Refresh', command=self.refresh_btn_callback)
        self.refresh_btn.anchor = 'NW'
        self.refresh_btn.place(width=80, height=24, x=240, y=20)

    def create_fw_state(self):
        self.fw_state = ttk.Label(
            self.master, text="FW:", border=1, relief='ridge')
        self.fw_state.anchor = 'NW'
        self.fw_state.place(width=74, height=20, x=300, y=140)
        self.fw_state.config(background="#a0a0a0")

    def create_vtx_state(self):
        self.vtx_state = ttk.Label(
            self.master, text="VTX", border=1, relief='ridge')
        self.vtx_state.anchor = 'NW'
        self.vtx_state.place(width=28, height=20, x=374, y=140)
        self.vtx_state.config(background="#a0a0a0")

    def create_prog_state(self):
        self.prog_state = ttk.Label(
            self.master, text="PROG", border=1, relief='ridge')
        self.prog_state.anchor = 'NW'
        self.prog_state.place(width=38, height=20, x=402, y=140)
        self.prog_state.config(background="#a0a0a0")

    def switch_version_callback(self, event):
        self.ver_index_select = self.ver_combobox.current()
        self.ver_name_select = self.ver_combobox['value'][self.ver_index_select]
        self.target_combobox['value'] = Download.vtx_name_list[self.ver_index_select]
        self.target_combobox.current(0)
        self.reset_fw_state()

    def switch_version_action(self):
        self.ver_combobox.bind("<<ComboboxSelected>>",
                               self.switch_version_callback)

    def switch_vtx_callback(self, event):
        self.vtx_index_select = self.target_combobox.current()
        self.vtx_name_select = self.target_combobox['value'][self.vtx_index_select]
        if self.vtx_index_select != 0 and self.vtx_index_select <= len(Download.vtx_id_list):
            ch341.vtx_id = Download.vtx_id_list[self.vtx_name_select]
        self.reset_fw_state()

    def switch_target_action(self):
        self.target_combobox.bind(
            "<<ComboboxSelected>>", self.switch_vtx_callback)

    def load_firmware_online_callback(event):
        global my_gui
        if my_gui.vtx_index_select != 0 and my_gui.ver_index_select != 0:
            Download.downloadLink = Download.firmware_link_list[
                my_gui.ver_name_select][my_gui.vtx_name_select]
            Download.localTemp = "./Data/Temp/fw.zip"
            Download.downloadCommand = 2
            my_gui.downloadCommand = 2
            my_gui.reset_fw_state()

            # my_gui.refresh_btn.config(state=tk.DISABLED)
            # my_gui.load_fw_online_btn.config(state=tk.DISABLED)
            # my_gui.load_fw_local_btn.config(state=tk.DISABLED)
            # my_gui.ver_combobox.config(state=tk.DISABLED)
            # my_gui.target_combobox.config(state=tk.DISABLED)
            # my_gui.update_btn.config(state=tk.DISABLED)
            # my_gui.auto_btn.config(state=tk.DISABLED)

        else:
            a = 1
            # print()
            # print("Version and VTX must be specified.")

    def create_load_firmnware_online_btn(self):
        self.load_fw_online_btn = ttk.Button(
            self.master, text='Load Firmware(Online)', command=self.load_firmware_online_callback)
        self.load_fw_online_btn.anchor = 'NW'
        self.load_fw_online_btn.place(width=150, height=24, x=20, y=100)
        # self.load_fw_online_btn.config(state=tk.DISABLED)

    def load_firmware_local_callback(event):
        global my_gui
        selected_file_path = filedialog.askopenfilename()
        try:
            if os.path.getsize(selected_file_path) <= 65536:
                ch341.fw_path = selected_file_path
                my_gui.fw_state.config(text="FW:Local")
                my_gui.fw_state.config(background="#42a459")
            else:
                # print()
                # print("local firmware error")
                my_gui.reset_fw_state()
        except:
            # print()
            # print("local firmware error")
            my_gui.reset_fw_state()

    def create_load_firmnware_local_btn(self):
        self.load_fw_local_btn = ttk.Button(
            self.master, text='Load Firmware(Local)', command=self.load_firmware_local_callback)
        self.load_fw_local_btn.anchor = 'NW'
        self.load_fw_local_btn.place(width=150, height=24, x=180, y=100)

    def update_callback(event):
        global my_gui
        ch341.command = 2
        my_gui.ch341Command = 2

    def create_update_button(self):
        self.update_btn = ttk.Button(
            self.master, text='Update', command=self.update_callback)
        self.update_btn.anchor = 'NW'
        self.update_btn.place(width=70, height=24, x=340, y=100)
        self.update_btn.config(state=tk.DISABLED)

    def create_progressbar(self):
        self.progressbar = ttk.Progressbar(self.master, mode='determinate')
        self.progressbar.anchor = 'NW'
        self.progressbar['value'] = 0
        self.progressbar.place(width=280, height=20, x=10, y=140)

    def ok_callback(self):
        self.window.destroy()
        self.window.grab_release()

    def create_window(self, string):
        windowX = 300
        windowY = 100
        offsetX = (self.master.winfo_screenwidth() - windowX)/2
        offsetY = (self.master.winfo_screenheight() - windowY)/2
        self.window = tk.Toplevel()
        self.window.geometry('%dx%d+%d+%d' %
                             (windowX, windowY, offsetX, offsetY))
        self.window.title(" ")
        label = tk.Label(self.window, text=string)
        label.pack(padx=10, pady=10)
        button = tk.Button(self.window, text="ok", command=self.ok_callback)
        button.pack(padx=10, pady=10)
        self.window.grab_set()
        self.window.resizable(False, False)

    def update_connection_state(self):
        # init download online info
        if self.updateCnt == 1:
            self.ver_combobox['value'] = Download.version_list
            self.ver_combobox.current(0)

            self.target_combobox['value'] = Download.vtx_name_list[0]
            self.target_combobox.current(0)

        # update ver_combobox status
        if self.downloadCommand != 0:
            self.ver_combobox.config(state=tk.DISABLED)
        elif self.ch341Command != 0:
            self.ver_combobox.config(state=tk.DISABLED)
        elif ch341.dev_connected == 1 and ch341.flash_connected == 1:
            self.ver_combobox.config(state="readonly")
        else:
            self.ver_combobox.config(state=tk.DISABLED)

        # update target_combobox status
        if self.downloadCommand != 0:
            self.target_combobox.config(state=tk.DISABLED)
        elif self.ch341Command != 0:
            self.target_combobox.config(state=tk.DISABLED)
        elif ch341.dev_connected == 1 and ch341.flash_connected == 1:
            self.target_combobox.config(state="readonly")
        else:
            self.target_combobox.config(state=tk.DISABLED)

        # update load_fw_online_btn status
        if self.downloadCommand != 0:
            self.load_fw_online_btn.config(state=tk.DISABLED)
        elif self.ch341Command != 0:
            self.load_fw_online_btn.config(state=tk.DISABLED)
        elif self.vtx_index_select != 0 and self.ver_index_select != 0:
            self.load_fw_online_btn.config(state=tk.NORMAL)
        else:
            self.load_fw_online_btn.config(state=tk.DISABLED)

        # update load_fw_local_btn status
        if self.downloadCommand != 0:
            self.load_fw_local_btn.config(state=tk.DISABLED)
        elif self.ch341Command != 0:
            self.load_fw_local_btn.config(state=tk.DISABLED)
        elif self.vtx_index_select != 0:
            self.load_fw_local_btn.config(state=tk.NORMAL)
        else:
            self.load_fw_local_btn.config(state=tk.DISABLED)

        # update refresh_btn status
        if self.downloadCommand != 0:
            self.refresh_btn.config(state=tk.DISABLED)
        elif self.ch341Command != 0:
            self.refresh_btn.config(state=tk.DISABLED)
        elif ch341.dev_connected == 1 and ch341.flash_connected == 1:
            self.refresh_btn.config(state=tk.NORMAL)
        else:
            self.refresh_btn.config(state=tk.DISABLED)

        # update auto_btn status
        if self.downloadCommand != 0:
            self.auto_btn.config(state=tk.DISABLED)
        elif self.ch341Command != 0:
            self.auto_btn.config(state=tk.DISABLED)
        elif ch341.dev_connected == 1 and ch341.flash_connected == 1:
            self.auto_btn.config(state=tk.NORMAL)
        else:
            self.auto_btn.config(state=tk.DISABLED)

        if self.ch341Command != 0 or self.downloadCommand != 0:
            self.update_btn.config(state=tk.DISABLED)

        if self.downloadCommand == 1 and Download.downloadCommand == 0:
            self.ver_combobox['value'] = Download.version_list
            self.ver_combobox.current(0)
            self.target_combobox['value'] = Download.vtx_name_list[0]
            self.target_combobox.current(0)
            self.downloadCommand = 0
            if Download.success == 1:
                self.create_window("Refresh success")
            else:
                self.create_window("Refresh failed")

        if ch341.dev_connected == 0:
            self.prog_state.config(background="#a0a0a0")
        elif ch341.dev_connected == 1:
            self.prog_state.config(background="#42a459")

        if ch341.flash_connected == 0:
            self.vtx_state.config(background="#a0a0a0")
        elif ch341.dev_connected == 1:
            self.vtx_state.config(background="#42a459")

        if ch341.flash_connected == 1 and ch341.dev_connected == 1:
            a = 1
        else:
            self.target_combobox.current(0)
            self.vtx_index_select = 0
            self.ver_index_select = 0
            self.ver_combobox.current(0)
            self.reset_fw_state()

        # check vtx id done
        if self.ch341Command == 1 and ch341.command == 0:
            j = 0
            for i in Download.vtx_id_list:
                if vtx_id_list[i] == ch341.vtx_id:
                    # print()
                    # print("Current vtx is", i)
                    for j in range(0, len(Download.vtx_name_list[self.ver_index_select])):
                        if self.target_combobox['value'][j] == i:
                            self.target_combobox.current(j)
                            self.vtx_name_select = i
                            self.vtx_index_select = j
            self.create_window(getFirmwareFromCRC(ch341.crc_table))
            self.ch341Command = 0
        elif self.ch341Command == 2:
            if ch341.command == 0:
                # update done
                self.progressbar['value'] = 100
                self.ch341Command = 0
                if ch341.success == 1:
                    self.create_window("Update success")
                else:
                    self.create_window("Update failed")
            else:
                self.progressbar['value'] = ch341.percent

        # download online firmware done
        if self.downloadCommand == 2 and Download.downloadCommand == 0:
            zfile = zipfile.ZipFile(Download.localTemp, 'r')
            for filename in zfile.namelist():
                data = zfile.read(filename)
                file = open("./Data/Temp/"+filename, 'w+b')
                file.write(data)
                file.close()
            ch341.fw_path = "./Data/Temp/"+filename
            self.fw_state.config(text="FW:Online")
            self.fw_state.config(background="#42a459")
            self.downloadCommand = 0
            if Download.success == 1:
                self.create_window("Load firmware(online) success")
            else:
                self.create_window("Load firmware(online) failed")

        # update update_btn status
        if self.ch341Command != 0 or self.downloadCommand != 0:
            self.update_btn.config(state=tk.DISABLED)
        elif self.ch341Command != 2:
            if self.fw_state.cget('text') == "FW:":
                self.update_btn.config(state=tk.DISABLED)
            else:
                self.update_btn.config(state=tk.NORMAL)

        if self.updateCnt < 10:
            self.updateCnt += 1
        self.master.after(100, self.update_connection_state)


def on_closing():
    global my_gui
    ch341.command = 255
    Download.downloadCommand = 255
    sys.exit()


def UI_mainloop():
    global my_gui
    root = tk.Tk()
    my_gui = MyGUI(root)
    my_gui.update_connection_state()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    my_gui.master.mainloop()
