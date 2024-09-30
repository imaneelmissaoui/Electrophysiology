import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import time
import heartpy as hp
import readSignalsFromCSV
from scipy.signal import butter,filtfilt
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    print(y)
    return y

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# Function to calculate biometrics using heartpy
def calculate_bloodOxygen(ppg1_signal,ppg2_signal,sample_rate):
    # Calculate the AC components by filtering out the DC component
    # Assuming the heartbeat frequency is around 0.5 - 4 Hz
    try:
        ac_red = butter_highpass_filter(ppg1_signal, 0.5, 100)
        ac_ir = butter_highpass_filter(ppg2_signal, 0.5, 100)
        
        #Calculate the DC components (mean of the signals)
        dc_red = np.mean(ac_red)
        dc_ir = np.mean(ac_ir)

        #Compute the Ratio of Ratios (RoR)
        ror = (np.std(ac_red) / dc_red) / (np.std(ac_ir) / dc_ir)

        #Estimate SpO2 using the empirical formula
        spo2 = 110 - 25 * ror

        bloodOxygen = f"{spo2:.2f}"
        return bloodOxygen 
        
    except:
        return "NAN"


def calculate_biometrics(ppg_signal, sample_rate):
    heart_rate_value = "NAN"
    respiratory_rate_value = "NAN"
    temperature_value = "NAN"

    #lowcut = 0.05  # low frequency cutoff in Hz (about 30 bpm)
    #highcut = 15 # high frequency cutoff in Hz (about 240 bpm)
    #fs = sample_rate  # sampling frequency of the data in Hz 

    #filtered_data = bandpass_filter(ppg_signal, lowcut, highcut, fs)


    try:
        # Ensure there is enough data for processing (at least 10 seconds of data at 100 Hz)
        if len(ppg_signal) >= 10*sample_rate:
            # Process the PPG signal with HeartPy
            
            #working_data, measures = hp.process_segmentwise(np.array(ppg_signal), sample_rate=sample_rate,segment_width=200,segment_overlap=0.25,calc_freq=True, reject_segmentwise=True)
            working_data, measures = hp.process(np.array(ppg_signal), sample_rate=sample_rate)
            
            # Extract biometrics from HeartPy's output
            #heart_rate_value = measures['bpm']
            heart_rate_value = f"{measures['bpm']:.1f}"
            #respiratory_rate_value = measures['breathingrate']#f"{measures['breathingrate']:.2f} "
            respiratory_rate_value = f"{measures['breathingrate']:.2f} "
            temperature_value = f"{np.average(readSignalsFromCSV.read_temp(1)):.2f}"
            
        else:
            heart_rate_value = "NAN"
            respiratory_rate_value = "NAN"
            temperature_value = "NAN"

        return heart_rate_value, respiratory_rate_value, temperature_value
    except Exception as e:
        st.error(f"Error calculating biometrics: {str(e)}")
        return 0,0,0