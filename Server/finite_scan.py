from __future__ import print_function
from time import sleep
from sys import stdout, version_info
from math import sqrt
from daqhats import mcc172, OptionFlags, SourceType, HatIDs, HatError
from daqhats_utils import select_hat_device, enum_mask_to_string, \
chan_list_to_mask
import pandas as pd
import datetime
import os
metaData = {}

def mainFiniteScan(myDict):
    CURSOR_BACK_2 = '\x1b[2D'
    ERASE_TO_END_OF_LINE = '\x1b[0K'
    actScanRate = ""
    try:
        SAMPLERATE = int(myDict["SAMPLERATE"])
        SAMPLEDURATION = int(myDict["SAMPLEDURATION"])
        # SENS = int(myDict["SENSITIVITY"])
        SAMP = int(SAMPLEDURATION*SAMPLERATE)
        # sensitivity = SENS
        samples_per_channel = SAMP
        scan_rate = SAMPLERATE
        sensChn0 = int(myDict["SENSITIVITY0"])
        sensChn1 = int(myDict["SENSITIVITY1"])
    except:
        # sensitivity = 1000.0
        sensChn0 = 1000.0
        sensChn1 = 1000.9
        samples_per_channel = 50000
        scan_rate = 10240.0
    print("Sensitivity Channel 0: ", sensChn0)
    print("Sensitivity Channel 1: ", sensChn1)
    print("Samples Per Channel: ", samples_per_channel)
    print("Sampling frequency: ", scan_rate) 
    channels = [0, 1]
    channel_mask = chan_list_to_mask(channels)
    num_channels = len(channels)
    options = OptionFlags.DEFAULT
    try:
        address = select_hat_device(HatIDs.MCC_172)
        hat = mcc172(address)
        print('\nSelected MCC 172 HAT device at address', address)
        iepe_enable = 1
        for channel in channels:
            hat.iepe_config_write(channel, iepe_enable)
            if channel == 0:
                hat.a_in_sensitivity_write(channel, sensChn0)
            else:
                hat.a_in_sensitivity_write(channel, sensChn1)
        hat.a_in_clock_config_write(SourceType.LOCAL, scan_rate)
        synced = False
        while not synced:
            (_source_type, actual_scan_rate, synced) = hat.a_in_clock_config_read()
            if not synced:
                sleep(0.005)
        print('    IEPE power: ', end='')
        if iepe_enable == 1:
            print('on')
        else:
            print('off')
        print('    Channels: ', end='')
        print(', '.join([str(chan) for chan in channels]))
        print('    Sensitivity Channel 0: ', sensChn0)
        print('    Sensitivity Channel 1: ', sensChn1)
        print('    Requested scan rate: ', scan_rate)
        print('    Actual scan rate: ', actual_scan_rate)
        print('    Samples per channel', samples_per_channel)
        print('    Options: ', enum_mask_to_string(OptionFlags, options))
        actScanRate = str(actual_scan_rate)
        metaData['Channels'] = ', '.join([str(chan) for chan in channels])
        metaData['Sensitivity Channel 0'] = str(sensChn0)
        metaData['Sensitivity Channel 1'] = str(sensChn1)
        metaData['Requested scan rate'] = str(scan_rate)
        metaData['Actual scan rate'] = str(actual_scan_rate)
        metaData['Samples per channel'] = str(samples_per_channel)
        metaData['Start Time'] =  str(datetime.datetime.now())                               
        hat.a_in_scan_start(channel_mask, samples_per_channel, options)
        print('Starting scan ... Press Ctrl-C to stop\n')
        print('Samples Read    Scan Count', end='')
        for chan in channels:
            print('      Ch ', chan, ' RMS', sep='', end='')
        print('')
        try:
            read_and_display_data(hat, samples_per_channel, num_channels)
        except KeyboardInterrupt:
            print(CURSOR_BACK_2, ERASE_TO_END_OF_LINE, '\n')
            hat.a_in_scan_stop()
        hat.a_in_scan_cleanup()
    except (HatError, ValueError) as err:
        print('\n', err)
    return actScanRate, metaData
    
def calc_rms(data, channel, num_channels, num_samples_per_channel, lstChn0, lstChn1):
    print(data)
    lstChn0.extend(round(value,6) for value in data[::2])
    lstChn1.extend(round(value,6) for value in data[1::2])
    value = 0.0
    index = channel
    for _i in range(num_samples_per_channel):
        value += (data[index] * data[index]) / num_samples_per_channel
        index += num_channels
    return sqrt(value)
    
def read_and_display_data(hat, samples_per_channel, num_channels):
    lstChn0 = []
    lstChn1 = []
    total_samples_read = 0
    read_request_size = 1000
    timeout = 5.0
    while total_samples_read < samples_per_channel:
        read_result = hat.a_in_scan_read(read_request_size, timeout)
        if read_result.hardware_overrun:
            print('\n\nHardware overrun\n')
            break
        elif read_result.buffer_overrun:
            print('\n\nBuffer overrun\n')
            break
        samples_read_per_channel = int(len(read_result.data) / num_channels)
        total_samples_read += samples_read_per_channel
        # lstChn0 lstChn1 data
        
        # ==============================================================
        print('\r{:12}'.format(samples_read_per_channel),
              ' {:12}'.format(total_samples_read), end='')
        if samples_read_per_channel > 0:
            #for i in range(num_channels):
            for i in range(0,1):
                value = calc_rms(read_result.data, i, num_channels,
                                 samples_read_per_channel, lstChn0, lstChn1)
                print('{:14.5f}'.format(value), end='')
            stdout.flush()
        # ==============================================================
    print(metaData)
    metaData['End Time'] = str(datetime.datetime.now()) 
    print("\n Sesnsing Job Complete!")
    print('\n')
    df = pd.DataFrame({'Channel 0': lstChn0, 'Channel 1': lstChn1})
    print("Shape: ", df.shape)
    df.to_csv("./main.csv", index=False)
    with open ("./logFile.txt", "a") as file:
        file.write(str(metaData))
        file.write("\n")
    
if __name__ == '__main__':
    mainFiniteScan()
