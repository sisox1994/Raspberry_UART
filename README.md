# Raspberry UART 



### 1. 列出所有  UART Port

```shell
$ dtoverlay -a | grep uart
```



### 2. 查看指定 UART Port 資訊

```shell
$ dtoverlay -h uart2
```

可以確認 此UART Port  Mapping 的 GPIO 腳位 ,  uart 2  預設 [ GPIO 0 -1 為 TX , RX]  [GPIO 2-3 CTS/RTS] 

```
Name:   uart2

Info:   Enable uart 2 on GPIOs 0-3. BCM2711 only.

Usage:  dtoverlay=uart2,<param>

Params: ctsrts                  Enable CTS/RTS on GPIOs 2-3 (default off)
```



### 3.配置開啟 UART2

```shell
$ sudo nano /boot/config.txt
```

檔尾加入

```
dtoverlay=uart2
```

重新開機($sudo reboot)後確認是否生效    PS. 預設只會有ttyAMA0 , 出現ttyAMA1表示成功開啟uart2

```shell
$ ls /dev/ttyAMA*
```

```
/dev/ttyAMA0  /dev/ttyAMA1
```



### 4. UART   ttyAMA   GPIO 配置關係表

```
uart0 ttyAMA0   TX:GPIO 14 (Pin8)    RX:GPIO 15 (Pin10)

uart2 ttyAMA1   TX: GPIO 0   (Pin27)    RX: GPIO 1  (Pin28)
uart3 ttyAMA2   TX: GPIO 4   (Pin7)     RX: GPIO 5  (Pin29)
uart4 ttyAMA3   TX: GPIO 8   (Pin24)    RX: GPIO 9  (Pin21)
uart5 ttyAMA4   TX: GPIO 12  (Pin32)    RX: GPIO 13 (Pin33)

```



```shell
直接在終端機測試 Uart2 輸出
$ echo haha > /dev/ttyAMA1
```



```shell
確認軟體版本
$ uname -a

確認硬體 Model  EX: [Raspberry Pi 4 Model B Rev 1.2]
$ cat /proc/device-tree/model

查看 Raspberry pi 硬體詳細資訊(含圖像化文字) GPIO,RAM size,Soc....
$ pinout

```



### 5. Python UART  - pyserial  



```python
# ========= 開啟 Serial port =======
# $ sudo raspi-config
# select [Interface Options]
# The serial login shell is disabled   /(N)
# The serial interface is enabled      /(Y)
# sudo reboot

# ======== 安裝 pyserial ===========
# $ python -m pip install pyserial

# ======== 修改 /boot/config.txt ==========
# $ sudo nano /boot/config.txt
# 如果沒有請加入下面這行至檔尾
# enable_uart=1  


import serial
import time
import threading

UART2 = serial.Serial("/dev/ttyAMA1",9600)

# 背景收資料 固定0.001秒 接收RX資料
def Background():
    # print("<Background ID>:", threading.get_ident())
    while True:
        r_data = UART2.read()
        time.sleep(0.001)
        print(r_data)


if __name__ == "__main__":

    # 建立背景 程序 (收RX Data 用)
    t1 = threading.Thread(target=Background)
    t1.setDaemon(True)
    t1.start()
    
    rawdata = bytearray(b'Hello UART\n')
 

    while True:        
        # Tx 發送 UART 資料   
        UART2.write(bytes(rawdata))
        time.sleep(0.3)
```

