import streamlit as st
import pandas as pd
import numpy as np
import heartpy as hp
from scipy.signal import butter, filtfilt, find_peaks
import os

# Specify the correct data directory
data_dir = "../PTT_Data"

# Function to load data based on selected subject and activity
def load_data(subject, activity):
    data_file = os.path.join(data_dir, f"s{subject}_{activity}.csv")
    return pd.read_csv(data_file)

# Function to calculate physiological parameters
def calculate_parameters(df):
    df['time'] = pd.to_datetime(df['time'])

    # Calculate Heart Rate (HR)
    peaks, _ = find_peaks(df['ecg'], distance=200)
    peak_times = df['time'].iloc[peaks]
    rr_intervals = peak_times.diff().dropna().dt.total_seconds()
    hr = 60 / rr_intervals.mean()

    # Calculate Breathing Rate (BR)
    ppg_signal = df['pleth_1']
    ppg_peaks, _ = find_peaks(ppg_signal, distance=200)
    ppg_peak_times = df['time'].iloc[ppg_peaks]
    br_intervals = ppg_peak_times.diff().dropna().dt.total_seconds()
    br = 60 / br_intervals.mean()

    # Calculate DeltaSpO2
    red_signal = df['pleth_1']
    infrared_signal = df['pleth_2']
    ratio_of_ratios = (red_signal / red_signal.mean()) / (infrared_signal / infrared_signal.mean())
    spo2 = 110 - 25 * ratio_of_ratios.mean()

    # Calculate Stress Level
    hrv = rr_intervals.std()
    stress_level = np.log(hrv)
    
    return hr, br, spo2, stress_level

# Function to apply a Butterworth bandpass filter
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

# Function to process and plot signals using HeartPy
def process_and_plot_signal_heartpy(signal, sample_rate, title, apply_filter=False, lowcut=0.5, highcut=50.0):
    if apply_filter:
        # Apply filter only if requested
        signal = butter_bandpass_filter(signal, lowcut, highcut, sample_rate, order=2)
    
    # Analyze and plot using HeartPy
    wd, m = hp.process(signal, sample_rate=sample_rate)
    fig = hp.plotter(wd, m, title=title, show=False)  # show=False to prevent immediate rendering
    st.pyplot(fig)

# Main function to create the Streamlit app
def main():
    st.set_page_config(layout="wide", page_title="Advanced Physiological Dashboard")

    st.markdown("""
        <style>
        .main-title {
            font-size: 36px;
            color: #4B0082;
            font-weight: bold;
            text-align: center;
        }
        .metric-box {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            border-radius: 10px;
            background-color: #e8f0fe;  /* Light blue color */
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .metric-box h3 {
            margin: 0;
            font-size: 24px;
            color: #333;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Physiological Parameters Dashboard")
    st.sidebar.header("Select Options")
    subject = st.sidebar.selectbox("Select Subject", list(range(1, 23)))
    activity = st.sidebar.selectbox("Select Activity", ["sit", "walk", "run"])

    df = load_data(subject, activity)

    with st.expander("Data Overview", expanded=True):
        st.write(df.head())

    with st.container():
        st.markdown("<h3 class='main-title'>Calculated Physiological Parameters</h3>", unsafe_allow_html=True)
        hr, br, spo2, stress_level = calculate_parameters(df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"<div class='metric-box'><h3>Heart Rate (HR)<br>{hr:.2f} BPM</h3></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-box'><h3>Breathing Rate (BR)<br>{br:.2f} BPM</h3></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-box'><h3>SpO2<br>{spo2:.2f} %</h3></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-box'><h3>Stress Level<br>{stress_level:.2f}</h3></div>", unsafe_allow_html=True)

    sample_rate = 1000.0  # Adjust this to your data's actual sample rate

    with st.container():
        st.markdown("<h3 class='main-title'>Raw and Filtered ECG Signals</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            # Plot raw ECG signal without filtering
            process_and_plot_signal_heartpy(df['ecg'].values, sample_rate, 'Raw ECG Signal', apply_filter=False)
        with col2:
            # Plot filtered ECG signal with filtering applied
            process_and_plot_signal_heartpy(df['ecg'].values, sample_rate, 'Filtered ECG Signal', apply_filter=True)

    # User selection for PPG signals
    ppg_option = st.radio("Select PPG Signal Display Option:", ("PPG Signal 1 Only", "All PPG Signals"))

    with st.container():
        st.markdown("<h3 class='main-title'>Raw and Filtered PPG Signals</h3>", unsafe_allow_html=True)
        
        if ppg_option == "PPG Signal 1 Only":
            # Display only the first PPG signal
            col1, col2 = st.columns(2)
            with col1:
                process_and_plot_signal_heartpy(df['pleth_1'].values, sample_rate, 'Raw PPG Signal 1', apply_filter=False, lowcut=0.5, highcut=5.0)
            with col2:
                process_and_plot_signal_heartpy(df['pleth_1'].values, sample_rate, 'Filtered PPG Signal 1', apply_filter=True, lowcut=0.5, highcut=5.0)
        
        elif ppg_option == "All PPG Signals":
            # Display all PPG signals
            for i in range(1, 7):
                col1, col2 = st.columns(2)
                with col1:
                    process_and_plot_signal_heartpy(df[f'pleth_{i}'].values, sample_rate, f'Raw PPG Signal {i}', apply_filter=False, lowcut=0.5, highcut=5.0)
                with col2:
                    process_and_plot_signal_heartpy(df[f'pleth_{i}'].values, sample_rate, f'Filtered PPG Signal {i}', apply_filter=True, lowcut=0.5, highcut=5.0)

if __name__ == "__main__":
    main()
