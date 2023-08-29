import machine
import network
import time
import ssl
import socket
#import os

#print(machine.freq())

def connect_wifi(ssid, passwd):
    wlan = network.WLAN(network.STA_IF)

    wlan.active(True)
    print(wlan.scan())
    #wlan.disconnect()
    isconn = wlan.isconnected()
    print(isconn)
    if not isconn:
        wlan.connect(ssid,passwd)
        time.sleep(3)
    print(wlan.config('mac'))
    print(wlan.ifconfig())

def https_request(url, meth, body=None):
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 443)[0][-1]
    s = socket.socket()
    s.connect(addr)

    ssock = ssl.wrap_socket(s)
    outlen = 0
    if meth == "POST":
        out = bytes('%s\r\n\r\n' % (body), 'utf8')
        outlen = len(out)
        ssock.write(bytes('POST /%s HTTP/1.0\r\nHost: %s\r\nContent-Length: %s\r\n\r\n' % ( path, host, outlen), 'utf8'))
        ssock.write(bytes('%s\r\n\r\n' % (body), 'utf8'))
    if meth == "GET":
        ssock.write(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % ( path, host), 'utf8'))
    while True:
        data = ssock.read(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    ssock.close()
    s.close()

connect_wifi('SSID','PASSWD')

https_request('https://HOST/post', 'GET')
https_request('https://HOST/post', 'POST', 'post')


