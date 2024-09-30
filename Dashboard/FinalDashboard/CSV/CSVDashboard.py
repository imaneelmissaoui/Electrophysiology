import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import time
import heartpy as hp


import readSignalsFromCSV
import biometricsCSV as biometrics
import CSVChartPlotFunctions

# Initialize empty DataFrames to store signal data
ppg_data = []
ecg_data = []

# Initialize variables for real-time biometrics
heart_rate_value = "NA"
breathingrate_value = "NA"
spo2_value= "NA"
temperature_value="NA"

st.set_page_config(layout="wide")
# Dark theme for the dashboard
with open("style.css", 'r') as style:
    st.markdown(style.read()  ,    unsafe_allow_html=True)

# Layout for real-time PPG and ECG charts with biometrics on the right
col1 ,col2 = st.columns([3, 1])

with col1:
    # Create the dropdown menu for pleth signal selection
    # st.markdown('<h2 class="custom-title">Real-Time PPG and ECG Dashboard</h2>', unsafe_allow_html=True)
    ecg_chart_placeholder = st.empty()
    ppg1_chart_placeholder = st.empty()
    ppg2_chart_placeholder = st.empty()
    ppg3_chart_placeholder = st.empty()
    ppg4_chart_placeholder = st.empty()
    ppg5_chart_placeholder = st.empty()
    ppg6_chart_placeholder = st.empty()
    ppgCharts = [ppg1_chart_placeholder,ppg2_chart_placeholder,
                    ppg3_chart_placeholder,ppg4_chart_placeholder,
                    ppg5_chart_placeholder,ppg6_chart_placeholder]




with col2:
    col3,col4 = st.columns([1,0.0001],vertical_alignment='center')
    with col3:
        # st.markdown('<h3>Biometrics</h3>', unsafe_allow_html=True)
        option = st.selectbox(
        "Select which pleth signal to visualize",
        ["pleth1", "pleth2", "pleth3", "pleth4", "pleth5", "pleth6", "all"]
        )
        st.write(f"Displaying: {option}")
        selectedRange = []
        if option == "pleth1": selectedRange = range(1,2) 
        if option == "pleth2": selectedRange = range(2,3) 
        if option == "pleth3": selectedRange = range(3,4) 
        if option == "pleth4": selectedRange = range(4,5) 
        if option == "pleth5": selectedRange = range(5,6) 
        if option == "pleth6": selectedRange = range(6,7) 
        if option == "all": selectedRange = range(1,7) 

        hr_box = st.empty()
        br_box = st.empty()
        spo2_box= st.empty()
        temp_box= st.empty()
    

# Initialize variables for timing
start_time = time.time()
time_step = 1 # Update every second
duration = 120  # Each acquisition lasts 2 minutes
SAMPLINGRATE = 500 # Sampling rate for the signals

# Continuous loop for real-time data acquisition and processing
while True:
    # Read CSV fresh every update step. Disadvantage of Streaming data from files like this, if very slow.
    # Seek to find an alternative for reading only the updated data.
    readSignalsFromCSV.read_csv_into_pd()




    
    CSVChartPlotFunctions.plotECG(ecg_chart_placeholder,SAMPLINGRATE)
    ppg_data_array = []
    for i in range(1,7):
        ppg_data_array.append(CSVChartPlotFunctions.UpdatePPGData(i,SAMPLINGRATE))
    for i in selectedRange:
        CSVChartPlotFunctions.PlotPPGData(ppg_data_array[i-1],ppgCharts,i,SAMPLINGRATE)
    
 
    # Update biometrics every 10 seconds

    #elapsed_time = time.time() - start_time
    #if elapsed_time >= 10:  # Recalculate Biometrics 
    #start_time = time.time()  # Reset the timer
    # Update Biometrics, if not enough samples are available nothing happens. 
    heart_rate_value, breathingrate_value, temperature_value = biometrics.calculate_biometrics(ppg_data_array[0],sample_rate=SAMPLINGRATE)  # Pass the last minute of PPG data
    spo2_value = biometrics.calculate_bloodOxygen(ppg_data_array[0],ppg_data_array[1],SAMPLINGRATE)
    # Display biometrics on the right
    hr_box.markdown(
    f"""
    <div class="BDiv">
        <h2 style='color: #37FD12;'>Heart Rate</h2>
        <h1 style='color: #37FD12; font-weight: bold;'>{heart_rate_value}</h1>
        <p style='color: #37FD12;'>BPM</p>
    </div>
    """,
    unsafe_allow_html=True
)
    br_box.markdown(
    f"""
    <div class="BDiv">
        <h2 style='color: #B80F0A;'>Breathing Rate</h2>
        <h1 style='color: #B80F0A; font-weight: bold;'>{breathingrate_value}</h1>
        
    </div>
    """,
    unsafe_allow_html=True
)
    spo2_box.markdown(
    f"""
    <div class="BDiv">
        <h2 style='color: #FFF200;'>SpO2</h2>
        <h1 style='color: #FFF200; font-weight: bold;'>{spo2_value}</h1>
        <p style='color: #FFF200;'>%</p>
        
    </div>
    """,
    unsafe_allow_html=True
)
    temp_box.markdown(
    f"""
    <div class="BDiv">
        <h2 style='color: white;'>Temperature</h2>
        <h1 style='color: white; font-weight: bold;'>{temperature_value}</h1>
        <p style='color: white;'>°C</p>
        
    </div>
    """,
    unsafe_allow_html=True
)

    time.sleep(time_step)  # Simulate a real-time update every second
