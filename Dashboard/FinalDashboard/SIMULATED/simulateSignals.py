import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import time
import heartpy as hp
# Constants for the simulations
PPG_BASELINE = 1.0  # Baseline value for PPG
ECG_BASELINE = 0.0  # Baseline value for ECG
HEART_RATE = 75  # Heart rate in beats per minute
t_prev = time.time()
# Simulate PPG signal
def simulate_ppg(sampling_rate = 100):
    global t_prev
    t = time.time() % 60
    delta = time.time()-t_prev
    t = np.arange(t_prev,time.time(),delta/sampling_rate)[-sampling_rate:]
    
    heart_rate_hz = HEART_RATE / 60
    ppg_waveform = (
        PPG_BASELINE + 
        0.5 * (np.sin(2 * np.pi * heart_rate_hz * t) + 0.3 * np.sin(2 * np.pi * 2 * heart_rate_hz * t)) +
        0.02 * np.random.normal(size=sampling_rate)
    )
    t_prev = time.time()
    return ppg_waveform
# Simulate ECG signal
def simulate_ecg(sampling_rate = 100):
    t = time.time() % 60
    heart_rate_hz = HEART_RATE / 60 
    ecg_waveform = (
        ECG_BASELINE +
        0.8 * np.exp(-((t - (1 / heart_rate_hz * 0.5)) ** 2) / (0.01 ** 2)) +
        0.05 * np.random.normal(size=sampling_rate)
    )
    return ecg_waveform
