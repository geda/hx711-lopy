from hx711_spi import *
from utime import ticks_ms, ticks_diff, sleep, sleep_ms
from machine import Pin
from onewire import DS18X20
from onewire import OneWire

#DS18B20 data line connected to pin P21
ow = OneWire(Pin('P21'))
temp = DS18X20(ow)


hx = HX711("P10", "P11", "P9")
#hx = HX711( "P10", "P11")
hx.OFFSET = -150000

data = [0 for _ in range(100)]

def get_median(hx, num=100):
    for _ in range(num):
        data[_] = hx.read()
    data.sort()
    return data[num // 2]

def run(loops = 100):
    temp.start_conversion()
    start = ticks_ms()
    hx.set_gain(128)
    sleep_ms(50)
    resulta = get_median(hx, loops)
    hx.set_gain(32)
    sleep_ms(50)
    resultb = get_median(hx, loops)
    t = temp.read_temp_async()
    print(resulta, resultb, t)

def run100(loops=100, delay = 1):
    for _ in range (loops):
        run(100)
        if delay:
            sleep(delay)

def minmax(loops=10000):
    middle = hx.read_average(1000)
    hx.filtered = middle
    middle -= hx.OFFSET
    cnt0003 = 0
    cnt001 = 0
    cnt003 = 0
    cnt010 = 0
    cnt030 = 0
    cnt100 = 0
    cntx = 0
    print ("Average", middle)
    for _ in range(loops):
        val = hx.read_lowpass() - hx.OFFSET
        if middle * (1 - 0.00003) < val < middle * (1 + 0.00003):
            cnt0003 += 1
        elif middle * (1 - 0.0001) < val < middle * (1 + 0.0001):
            cnt001 += 1
        elif middle * (1 - 0.0003) < val < middle * (1 + 0.0003):
            cnt003 += 1
        elif middle * (1 - 0.001) < val < middle * (1 + 0.001):
            cnt010 += 1
        elif middle * (1 - 0.003) < val < middle * (1 + 0.003):
            cnt030 += 1
        elif middle * (1 - 0.01) < val < middle * (1 + 0.01):
            cnt100 += 1
        else:
            cntx += 1
            print("Really out of band at %d: %d %x"  % (_, int(val), int(val)))

    print("+/- 0.003%% %f\n+/- 0.01%% %f\n+/- 0.03%% %f\n+/- .1%%   %f\n+/- .3%%   %f\n+/- 1%%  %f\nBeyond:  %f" %
          (cnt0003/loops, cnt001/loops, cnt003/loops, cnt010/loops, cnt030/loops, cnt100/loops, cntx/loops))


run()
#minmax(1000)
