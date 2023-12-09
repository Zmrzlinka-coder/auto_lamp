from yeelight import *
import time
import schedule
import socket  
import sys
from urllib.parse import urlparse

dst="239.255.255.250"
msg = "\r\n".join(["M-SEARCH * HTTP/1.1", "HOST: 239.255.255.250:1982", 'MAN: "ssdp:discover"', "ST: wifi_bulb"])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  
s.settimeout(5)  
s.sendto(msg.encode(), ("239.255.255.250", 1982))

while True:  
    try:
        data, addr = s.recvfrom(32*1024)
    except socket.timeout:
        break
    capabilities = dict([x.strip("\r").split(": ") for x in data.decode().split("\n") if ":" in x])
    parsed_url = urlparse(capabilities["Location"])

    bulb_ip = parsed_url.hostname
    print(bulb_ip)



bulb=Bulb(bulb_ip[0])

def turnOnAt16():
    bulb.turn_on()
    bulb.set_brightness(100)
    bulb.set_color_temp(4100)

def turnOnAt21():
    bulb.turn_on()
    bulb.set_rgb(255,0,0)
    bulb.set_brightness(100)

def main():
    schedule.every().day.at('08:00').do(turnOnAt16)
    schedule.every().day.at('16:00').do(turnOnAt16)
    schedule.every().day.at('21:00').do(turnOnAt21)
    schedule.every().day.at('23:00').do(bulb.turn_off)
    while True:
        schedule.run_pending()
        time.sleep(10)

if __name__=='__main__':
    main()
    

