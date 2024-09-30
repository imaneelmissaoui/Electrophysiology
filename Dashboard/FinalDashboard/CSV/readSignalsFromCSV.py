import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import time
import heartpy as hp

# Could be made dyanmic per sample chunk later. If we assume Timestamps
SAMPLE_RATE = 500 # Samples a second.
pd_dataframe = pd.DataFrame()

def read_ppg(number = 1):
    ppg_waveform = pd_dataframe["pleth_"+str(number)].to_numpy()
    return ppg_waveform
# Simulate ECG signal
def read_ecg():
    ecg_waveform = pd_dataframe["ecg"].to_numpy()
    return ecg_waveform

def read_time():
    time_stamps = pd_dataframe["time"].to_numpy()
    return np.datetime64(time_stamps)

def read_temp(number=1):
    temp = pd_dataframe["temp_"+str(number)].to_numpy()
    return temp

def read_csv_into_pd():
    global pd_dataframe
    pd_dataframe = pd.read_csv('sim_run_data.csv', sep=',')
