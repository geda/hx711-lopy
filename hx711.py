from machine import Pin

class HX711:
    def __init__(self, dout, pd_sck, gain=128):
        
        self.pSCK = Pin(pd_sck , mode=Pin.OUT)
        self.pOUT = Pin(dout, mode=Pin.IN, pull=Pin.PULL_DOWN)

        self.GAIN = 0
        self.OFFSET = 0
        self.SCALE = 1
        self.lastVal = 0
        self.allTrue = False
        
        self.set_gain(gain);
        

    def createBoolList(size=8):
        ret = []
        for i in range(8):
            ret.append(False)
        return ret
    
    def is_ready(self):
        return self.pOUT() == 0

    def set_gain(self, gain):
        if gain is 128:
            self.GAIN = 1
        elif gain is 64:
            self.GAIN = 3
        elif gain is 32:
            self.GAIN = 2

        self.pSCK.value(False)
        self.read()
        print('Gain setted')

    def read(self):
        
        dataBits = [self.createBoolList(), self.createBoolList(), self.createBoolList()]
        while not self.is_ready():
            pass
              
        for j in range(2, -1, -1):
            for i in range(7, -1, -1):
                self.pSCK.value(True)
                dataBits[j][i] = self.pOUT()
                self.pSCK.value(False)


        #set channel and gain factor for next reading
        for i in range(self.GAIN):
            self.pSCK.value(True)
            self.pSCK.value(False)
            

        #check for all 1
        if all(item == True for item in dataBits[0]):
            print('all true')
            self.allTrue=True
            return self.lastVal

        self.allTrue=False

        
        readbits = ""
        for j in range(2, -1, -1):
            for i in range(7, -1, -1):
                if dataBits[j][i] == True:
                    readbits= readbits +'1'
                else:
                    readbits= readbits+'0'

        self.lastVal = int(readbits, 2)
        
        if self.lastVal > 0x7fffff:
            self.lastVal -= 0x1000000

        return self.lastVal



    def read_average(self, times=3):
        sum = 0
        effectiveTimes = 0
        readed = 0
        for i in range(times):
            readed = self.read()
            if self.allTrue == False:
                sum += readed
                effectiveTimes+=1

        if effectiveTimes == 0:
            return 0
        return sum / effectiveTimes

    def get_value(self, times=3):
        return self.read_average(times) - self.OFFSET

    def get_units(self, times=3):
        return self.get_value(times) / self.SCALE

    def tare(self, times=15):
        sum = self.read_average(times)
        self.set_offset(sum)

    def set_scale(self, scale):
        self.SCALE = scale

    def set_offset(self, offset):
        self.OFFSET = offset

    def power_down(self):
        self.pSCK.value(False)
        self.pSCK.value(True)


    def power_up(self):
        self.pSCK.value(False)

