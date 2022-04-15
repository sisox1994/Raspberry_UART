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