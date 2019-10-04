import smbus2 
import bme280 
import pyfiap
import math
import datetime

'''
 Sonntag近似式を使って飽和水蒸気圧[Pa]を求めます
'''
def temp2svp( temp ):
  temp = temp+273.15
  a = -6096.9385 / temp
  b = 21.2409642
  c = -2.711193 / 100 * temp
  d = 1.673952 / 100000 * temp * temp
  e = 2.433502 * math.log(temp)
  return( math.exp( a + b + c + d + e ) )

def calc_vpd( temp, humi ):
  svp = temp2svp(temp)   # Saturated Vapour Pressure [Pa]
  vp  = svp * humi / 100 # Vapour Pressure [Pa]
  vpd = (svp-vp)/1000    # Vapour Pressure Dificit [kPa]
  return(vpd)

bus = smbus2.SMBus(1) 
bme280.load_calibration_params(bus, 0x76) 
data = bme280.sample(bus, 0x76)

temp = data.temperature
humi = data.humidity
vpd  = calc_vpd(temp, humi)
pres = data.pressure
'''
print("Temp[C]   : {:.2f}".format(temp))
print("Humi[%]   : {:.2f}".format(humi))
print("VPD[kPa]  : {:.4f}".format(vpd))
print("Pres[hPa] : {:.2f}".format(pres))

'''
today = datetime.datetime.now()
fiap = pyfiap.fiap.APP("http://iot.info.nara-k.ac.jp/axis2/services/FIAPStorage?wsdl")
fiap.write([['http://tomato.fukuoka.lab/bme280/temperature', "{:.2f}".format(temp), today],
            ['http://tomato.fukuoka.lab/bme280/humidity', "{:.2f}".format(humi), today],
            ['http://tomato.fukuoka.lab/bme280/VPD', "{:.4f}".format(vpd), today],
            ['http://tomato.fukuoka.lab/bme280/pressure', "{:.2f}".format(pres), today],])

