## python version

windows 3.10.5 32-bit

## generate exe

```
pyinstaller ./hdzero_programmer.py --onefile
```

## Linux

### install library

```
sudo apt-get install python3-tk python3-pil.imagetk python3-wget
```

### Install driver

 execute only once

 `cd ./ch341par_linux/driver`

 `make`

 `sudo make install`

### connect your programmer tool to pc

### Modify device permission

`sudo chmod 777 /dev/ch34x_pis0`

### Run hdzero_programmer.py
