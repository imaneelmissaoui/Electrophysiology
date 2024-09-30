import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import time
import heartpy as hp

import simulateSignals
import biometrics


# Initialize empty DataFrames to store signal data
ppg_data = []
ecg_data = []

# Initialize variables for real-time biometrics
heart_rate_value = "NA"
breathingrate_value = "NA"

st.set_page_config(layout="wide")
# Dark theme for the dashboard
with open("style.css", 'r') as style:
    st.markdown(style.read()  ,    unsafe_allow_html=True)

# Layout for real-time PPG and ECG charts with biometrics on the right
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<h2 class="custom-title">Real-Time PPG and ECG Dashboard</h2>', unsafe_allow_html=True)
    ppg_chart_placeholder = st.empty()
    ecg_chart_placeholder = st.empty()

with col2:
    st.markdown('<h3>Biometrics</h3>', unsafe_allow_html=True)
    hr_box = st.empty()
    br_box = st.empty()
    

# Initialize variables for timing
start_time = time.time()
time_step = 1 # Update every second
duration = 120  # Each acquisition lasts 2 minutes
SAMPLINGRATE = 100 # Sampling rate for the signals
HEART_RATE = 80  # Heart rate in beats per minute

# Continuous loop for real-time data acquisition and processing
while True:
    # Simulate new data points
    time_stamp = pd.Timestamp.now()
    ppg_value = simulateSignals.simulate_ppg()
    ecg_value = simulateSignals.simulate_ecg()

    # Append new data to the signal buffers
    ppg_data = np.concatenate((ppg_data,ppg_value))
    ecg_data =np.concatenate((ecg_data,ecg_value))
    
    # Keep only the last 2 minutes (120 seconds) of data
    if len(ppg_data) > 12000:  # Assuming a 100 Hz sampling rate
        ppg_data = ppg_data[-12000:]
    if len(ecg_data) > 12000:
        ecg_data = ecg_data[-12000:]

    # Plot the PPG data
    ppg_fig = go.Figure()
    ppg_fig.add_trace(go.Scatter(x=(np.array(range((len(ppg_data))))/SAMPLINGRATE).tolist(), y=ppg_data, mode='lines', name='PPG', line=dict(color='green')))
    ppg_fig.update_layout(
        title='PPG Signal',
        xaxis_title='Time in seconds',
        xaxis = dict(
        tickmode = 'linear',
        tick0=0, dtick = 1,
        ),
        xaxis_ticksuffix = 's',
        yaxis_title='Signal Value',
        template='plotly_dark',
        plot_bgcolor='rgba(30, 30, 30, 1)',  # Dark background for plot
        paper_bgcolor='rgba(30, 30, 30, 1)',  # Dark background for paper
        height=300,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    ppg_chart_placeholder.plotly_chart(ppg_fig, use_container_width=True)

    # Plot the ECG data
    ecg_fig = go.Figure()
    ecg_fig.add_trace(go.Scatter(x=list(range(len(ecg_data))), y=ecg_data, mode='lines', name='ECG', line=dict(color='red')))
    ecg_fig.update_layout(
        title='ECG Signal',
        xaxis_title='Time',
        yaxis_title='Signal Value',
        template='plotly_dark',
        plot_bgcolor='rgba(30, 30, 30, 1)',  # Dark background for plot
        paper_bgcolor='rgba(30, 30, 30, 1)',  # Dark background for paper
        height=300,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    ecg_chart_placeholder.plotly_chart(ecg_fig, use_container_width=True)

    # Update biometrics every 10 seconds
    elapsed_time = time.time() - start_time
    if elapsed_time >= 10:  # Recalculate biometrics every 10 seconds
        start_time = time.time()  # Reset the timer
        heart_rate_value, breathingrate_value = biometrics.calculate_biometrics(ppg_data)  # Pass the last minute of PPG data

    # Display biometrics on the right
    hr_box.markdown(f'<div class="biometrics-box">Heart Rate: {heart_rate_value}</div>', unsafe_allow_html=True)
    br_box.markdown(f'<div class="biometrics-box">Breathing Rate: {breathingrate_value}</div>', unsafe_allow_html=True)

    time.sleep(time_step)  # Simulate a real-time update every second
