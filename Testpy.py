import HackRF_Snippet
import time 

center_frequency = 105e6

HackRF_Snippet.setParameters(center_frequency)
iq = HackRF_Snippet.hackrf_run(iq_data = True)
print(iq.size)
HackRF_Snippet.save_data(iq,center_frequency)