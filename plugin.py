#!/usr/bin/env python
"""
Midea heat pump. The Python plugin for Domoticz
Author: Kawiarz33
Requirements: 
    1.python module minimalmodbus -> http://minimalmodbus.readthedocs.io/en/master/
        (pi@raspberrypi:~$ sudo pip3 install minimalmodbus)
    2.Communication module Modbus USB to RS485 converter module
"""
"""
<plugin key="Midea" name="Midea heat pump" version="1.0.0" author="Kawiarz33">
    <params>
        <param field="SerialPort" label="Modbus Port" width="200px" required="true" default="/dev/ttyUSB0" />
        <param field="Mode1" label="Baud rate" width="40px" required="true" default="9600"  />
        <param field="Mode2" label="Device ID" width="40px" required="true" default="1" />
        <param field="Mode3" label="Reading Interval min." width="40px" required="true" default="1" />
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
            </options>
        </param>
    </params>
</plugin>

"""

import minimalmodbus
import serial
import Domoticz


class BasePlugin:
    def __init__(self):
        self.runInterval = 1
        self.rs485 = "" 
        return

    def onStart(self):
        self.rs485 = minimalmodbus.Instrument(Parameters["SerialPort"], int(Parameters["Mode2"]))
        self.rs485.serial.baudrate = Parameters["Mode1"]
        self.rs485.serial.bytesize = 8
        self.rs485.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.rs485.serial.stopbits = 1
        self.rs485.serial.timeout = 1
        self.rs485.debug = False

        self.rs485.mode = minimalmodbus.MODE_RTU
        devicecreated = []
        Domoticz.Log("Midea heat pump plugin start")
        self.runInterval = int(Parameters["Mode3"]) * 1 
        if 1 not in Devices:
            Domoticz.Device(Name="PC oper freq", Unit=1,TypeName="Hz",Used=0).Create()
        if 2 not in Devices:
            Domoticz.Device(Name="PC Water inlet temp", Unit=2,TypeName="Temperature",Used=0).Create()
        if 3 not in Devices:
            Domoticz.Device(Name="PC Water out temp", Unit=3,TypeName="Temperature",Used=0).Create()
        if 4 not in Devices:
            Domoticz.Device(Name="PC Fan", Unit=4,TypeName="rpm",Used=0).Create()
        if 5 not in Devices:
            Domoticz.Device(Name="Condenser temperature", Unit=5,TypeName="Temperature",Used=0).Create()
        if 6 not in Devices:
            Domoticz.Device(Name="Outdoor ambient temp", Unit=6,TypeName="Temperature",Used=0).Create()
        if 7 not in Devices:
            Domoticz.Device(Name="Compressor inlet temp", Unit=7,TypeName="Temperature",Used=0).Create()
        if 8 not in Devices:
            Domoticz.Device(Name="Compressor discharge temp", Unit=8,TypeName="Temperature",Used=0).Create()
        if 9 not in Devices:
            Domoticz.Device(Name="Outdoor unit current", Unit=9,TypeName="Current",Used=0).Create()
        if 10 not in Devices:
            Domoticz.Device(Name="curve T1S calculated value", Unit=10,TypeName="Temperature",Used=0).Create()
        if 11 not in Devices:
            Domoticz.Device(Name="Water flow", Unit=11,TypeName="m3/h",Used=0).Create()
        if 12 not in Devices:
            Domoticz.Device(Name="Heat Power", Unit=12,TypeName="Power",Used=0,Options=Options).Create()
       
    def onStop(self):
        Domoticz.Log("Midea heat pump plugin stop")

    def onHeartbeat(self):
        self.runInterval -=1;
        if self.runInterval <= 0:
            # Get data from Midea
            try:
                PC_Freq = self.rs485.read_register(100, functioncode=3, number_of_decimals=0)
                W_in_temp = self.rs485.read_register(104, functioncode=3, number_of_decimals=0)
                W_out_temp = self.rs485.read_register(105, functioncode=3, number_of_decimals=0)
                PC_Fan = self.rs485.read_register(102, functioncode=3, number_of_decimals=0)
                Cond_temp = self.rs485.read_register(106, functioncode=3, number_of_decimals=0)
                Amb_temp = self.rs485.read_register(107, functioncode=3, number_of_decimals=0)
                Comp_in_temp = self.rs485.read_register(109, functioncode=3, number_of_decimals=0)
                Comp_out_temp = self.rs485.read_register(108, functioncode=3, number_of_decimals=0)
                Comp_Current = self.rs485.read_register(118, functioncode=3, number_of_decimals=0)
                Curve_temp = self.rs485.read_register(137, functioncode=3, number_of_decimals=0)
                W_flow = self.rs485.read_register(138, functioncode=3, number_of_decimals=0)*100
                Heat_power = self.rs485.read_register(140, functioncode=3, number_of_decimals=0)*100
                
            except:
                Domoticz.Log("Connection problem");
            else:
                #Update devices
                Devices[1].Update(0,str(PC_Freq))
                Devices[2].Update(0,str(W_in_temp))
                Devices[3].Update(0,str(W_out_temp))
                Devices[4].Update(0,str(PC_Fan))
                Devices[5].Update(0,str(Cond_temp))
                Devices[6].Update(0,str(Amb_temp))
                Devices[7].Update(0,str(Comp_in_temp))
                Devices[8].Update(0,str(Comp_out_temp))
                Devices[9].Update(0,str(Comp_Current))
                Devices[10].Update(0,str(Curve_temp))
                Devices[11].Update(0,str(W_flow))
                Devices[12].Update(0,str(Heat_power))
                

            if Parameters["Mode6"] == 'Debug':
                Domoticz.Log("Midea heat pump Modbus Data")
                Domoticz.Log('PC oper freq: {0:d} Hz'.format(PC_Freq))
                Domoticz.Log('PC Water inlet temp: {0:d} C'.format(W_in_temp))
                Domoticz.Log('PC Water out temp: {0:d} C'.format(W_out_temp))
                Domoticz.Log('PC Fan: {0:d} rpm'.format(PC_Fan))
                Domoticz.Log('Condenser temperature: {0:d} C'.format(Cond_temp))
                Domoticz.Log('Outdoor ambient temp: {0:d} C'.format(Amb_temp))
                Domoticz.Log('Compressor inlet temp: {0:d} C'.format(Comp_in_temp))
                Domoticz.Log('Compressor discharge temp: {0:d} C'.format(Comp_out_temp))
                Domoticz.Log('Outdoor unit current: {0:d} A'.format(Comp_Current))
                Domoticz.Log('curve T1S calculated value: {0:d} C'.format(Curve_temp))
                Domoticz.Log('Water flow: {0:d} m3/h'.format(W_flow))
                Domoticz.Log('Heat Power: {0:d} W'.format(Heat_power))
                

            self.runInterval = int(Parameters["Mode3"]) * 6


global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
