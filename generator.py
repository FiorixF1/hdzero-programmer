# Python 3.10 a 32 bit mi raccomando

import json
import zlib
import os

class Ch341:
    def __init__(self):
        self.iobuffer = [0 for i in range(65544)]
        self.fw_path = ""
        self.fw_full_size = 0
        self.pageNum = 0
        self.read_crc = []

ch341 = Ch341()

def get_expected_checksum(ch341):
    with open(ch341.fw_path, 'rb') as fw_file:
        fw_image_ff = fw_file.read()
        fw_image_00 = fw_image_ff
        if ch341.fw_full_size % 256 != 0:
            # The firmware image must reflect the memory content in Flash for correct CRC calculation.
            # Flash is written in blocks of 256 bytes each. Make the firmware image a multiple of 256 
            # by adding padding bytes (0xFF) at the end, as it happens in the real device.
            fw_image_ff += bytes([0xff])*(256 - ch341.fw_full_size%256)
            # However VTXs fresh from manifacturer have null bytes as padding instead of 0xFF,
            # so calculate two valid CRCs.
            fw_image_00 += bytes([0x00])*(256 - ch341.fw_full_size%256)
            
        ch341.pageNum = (ch341.fw_full_size + (1 << 8) - 1) >> 8
        ch341.read_crc = []
        ch341.read_crc.append(zlib.crc32(fw_image_ff) & 0xffffffff)
        ch341.read_crc.append(zlib.crc32(fw_image_00) & 0xffffffff)

vtx_list = ['foxeer_vtx',
            'hdzero_freestyle_v1',
            'hdzero_freestyle_v2',
            'hdzero_race_v1',
            'hdzero_race_v2',
            'hdzero_race_v3',
            'hdzero_whoop',
            'hdzero_whoop_lite',
            'hdzero_eco']

version_list = ['1.0.0',
                '1.1.0',
                '1.2.0',
                '1.3.0',
                '1.4.0',
                '1.5.0',
                '1.5.0-CITA',
                '1.6.0',
                '1.6.0-CITA']

firmware_list = dict()

for version in version_list:
    print(f"Version: {version}")
    for vtx in vtx_list:
        ch341.fw_path = f"~/HDZero/Firmware/{version}/{vtx}/HDZERO_TX.bin"
        try:
            ch341.fw_full_size = os.path.getsize(ch341.fw_path)
        except:
            continue
        get_expected_checksum(ch341)
        
        firmware = vtx + " @ " + version
        page_string = ch341.pageNum
        crc_strings = list(map(lambda crc: "0x"+hex(crc)[2:].rjust(8, '0'), ch341.read_crc))
        firmware_list[firmware] = (page_string, crc_strings)
        print("{}: {} - {} pages".format(vtx.ljust(20, ' '), crc_strings, page_string))
    print()

output_object = dict()
for firmware in firmware_list:
    output_object[firmware] = {
        "pageNum": firmware_list[firmware][0],
        "read_crc": firmware_list[firmware][1]
    }
with open("crc.json", "w") as output_file:
    output_data = json.dumps(output_object, indent=4)
    output_file.write(output_data)

