import pylibhackrf ,ctypes
import time
#import timeit 
import numpy as np
import copy

buf = list()
length = 0 
#center_freq = int(105e6)
#sample_rate = int(2.048e6)

hackrf = pylibhackrf.HackRf()


def setParameters(center_freq,sample_rate = int(2.048e6), lna = 16, vga = 20):
    center_freq = int(center_freq)
    sample_rate = int(sample_rate)
    hackrf.setup()
    hackrf.set_freq(center_freq)
    hackrf.set_sample_rate(sample_rate)
    hackrf.set_amp_enable(False)
    hackrf.set_lna_gain(lna)
    hackrf.set_vga_gain(vga)    
    #hackrf.set_baseband_filter_bandwidth(1 * 1000 * 1000) 
    dt = np.array([center_freq,sample_rate])
    return dt

def callback_fun(hackrf_transfer):
    global  buf,length
    length = hackrf_transfer.contents.valid_length
    #print(length)
    array_type = (ctypes.c_byte*length)
    values = ctypes.cast(hackrf_transfer.contents.buffer, ctypes.POINTER(array_type)).contents
    buf = copy.deepcopy(values)
    return 0

def hackrf_run(numTime = 1, sample_rate = int(2.048e6), iq_data = False):
    hackrf.start_rx_mode(callback_fun)
    time.sleep(1)
    
    iq = hackrf.packed_bytes_to_iq(buf)
    iq = iq - np.mean(iq) #dc offset
    hackrf.stop_rx_mode()
    
    if iq_data == False:
        fy = np.array(np.fft.fft(iq) * 2 / iq.size)
        fy = np.fft.fftshift(fy)
        freq = np.array(np.fft.fftfreq(iq.size, d=sample_rate))
        freq = np.fft.fftshift(freq)
        return fy, freq
    if iq_data == True:
        return iq

def save_data(iq, center_freq, savef = False):
    strname = str(center_freq/1e6) + 'e6' #+ str(time.strftime('%m/%d_%H:%M', time.localtime()))
    print(strname)
    if savef == True:
        np.savez(strname, data_pts = data_pts, fy = fy, freq = freq, iq = iq)
    return 


if __name__ == '__main__':
    center_frequency = 105e6
    fy = 0
    freq = 0
    iq = 0
    data_pts = setParameters(center_frequency)
    print(data_pts)
    fy,freq = hackrf_run()
    #print(Fy.size)
    #print(xfreq.size)
    #print(iq.size)
    
    strname = str(center_frequency/1e6) + 'e6'
    np.savez(strname, data_pts = data_pts, fy = fy, freq = freq, iq = iq)