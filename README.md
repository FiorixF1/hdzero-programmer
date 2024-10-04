
## Clone the repository or download the latest [release](https://github.com/FiorixF1/hdzero-programmer/releases).

#### Cloning
```
git clone https://github.com/FiorixF1/hdzero-programmer.git
cd hdzero-programmer
```

## Windows

#### Python Version

windows 3.10.5 32-bit

#### Generate .exe

```
pyinstaller ./hdzero_programmer.py --onefile
```

## Linux

#### Install the ch341 kernel driver

```
unzip ch341par_linux_V1.4_20230524.zip
cd ch341par_linux/driver
make
sudo make install
cd -
```

#### Apply ch341 driver permissions
- Note: something similar could potentially be perform with udev rules as well.
- Plugin the hdzero-programmer dongle first (ID 1a86:5512 QinHeng Electronics CH341 in EPP/MEM/I2C mode, EPP/I2C adapter), then
```
sudo chmod 777 /dev/ch34x_pis0
```


#### Install python pre-requisites
```
sudo apt-get install python3 python3-tk python3-pil.imagetk python3-wget
```

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
