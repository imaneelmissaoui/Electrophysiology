import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import time
import heartpy as hp


# Function to calculate biometrics using heartpy
def calculate_biometrics(ppg_signal):
    heart_rate_value = 0
    respiratory_rate_value = 0

    try:
        # Ensure there is enough data for processing (at least 10 seconds of data at 100 Hz)
        if len(ppg_signal) >= 1000:
            # Process the PPG signal with HeartPy
            working_data, measures = hp.process(np.array(ppg_signal), sample_rate=100.0)
            
            # Extract biometrics from HeartPy's output
            heart_rate_value = f"{measures['bpm']:.1f} BPM"
            respiratory_rate_value = f"{measures['breathingrate']:.2f} "
            
            #heart_rate_value = measures['bpm']
            #respiratory_rate_value = measures['breathingrate']
            # Placeholder values for blood oxygenation and pressure
        else:
            heart_rate_value = "NA"
            respiratory_rate_value = "NA"
        return heart_rate_value, respiratory_rate_value
    except Exception as e:
        st.error(f"Error calculating biometrics: {str(e)}")
        return 0,0