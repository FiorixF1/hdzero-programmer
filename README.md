
## Clone the repository or download the latest [release](https://github.com/FiorixF1/hdzero-programmer/releases).

#### Cloning
```
git clone https://github.com/FiorixF1/hdzero-programmer.git
cd hdzero-programmer
```

## Windows

#### Python Version

Windows 3.10.5 32-bit (but it should work also on 64 bit)

#### Create venv

#### Install package

```
.venv/Scripts/python.exe -m pip install Pillow pyserial esptool xmodem requests pyinstaller
```

#### Generate .exe

```
pyinstaller ./hdzero_programmer.py --onefile
```

## Linux

#### Install the ch341 kernel driver

```
unzip CH341PAR_LINUX.zip
cd CH341PAR_LINUX/driver
make -C /lib/modules/$(uname -r)/build M=$PWD modules
sudo make install
cd -
```

#### Apply ch341 driver permissions
- Note: something similar could potentially be performed with udev rules as well. On my machine it worked with
```
sudo nano /etc/udev/rules.d/99-ch34x-pis.rules
SUBSYSTEM=="usbmisc", KERNEL=="ch34x_pis*", MODE="0666"
```

- Plugin the hdzero-programmer dongle first (ID 1a86:5512 QinHeng Electronics CH341 in EPP/MEM/I2C mode, EPP/I2C adapter), then
```
# sometimes the device shows up as 0, 1, or some other number. Chmod all of them.
sudo chmod 777 /dev/ch34x_pis*
```

#### Install python pre-requisites
```
sudo apt-get install python3 python3-tk python3-pil.imagetk python3-wget
```

#### Connect programmer to hdzero vtx

#### Linux execute
```
python3 ./hdzero_programmer.py
```

#### Uninstalling the ch341 driver
- Note: Sometimes the driver will show up as `/dev/ch34x_pis1` or another number.  May need to uninstall, reboot, install.
```
cd ch341par_linux/driver
sudo make uninstall
```
