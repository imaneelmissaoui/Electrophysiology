# This script just copies data from one file to another to simulate a new file being written.
# It is to be viewed separately from the other code.  
import pandas as pd
import numpy as np
import time

pd_dataframe = pd.read_csv('sample_base_data.csv', sep=',')
time_step = 1
print(pd_dataframe.shape)
samplesRead = 0
while samplesRead < pd_dataframe.shape[0]:
    samplesRead += 500
    pd_newdataframe = pd_dataframe.iloc[:int((samplesRead/500)*500)]
    pd_newdataframe.to_csv("sim_run_data.csv")
    
    time.sleep(time_step)  # Simulate a real-time update every second
