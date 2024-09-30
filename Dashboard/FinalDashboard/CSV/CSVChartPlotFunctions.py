import numpy as np
import plotly.graph_objs as go
import readSignalsFromCSV
from scipy.signal import butter, filtfilt

import scipy.io.wavfile as wavf

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

CUTDATA_FLAG = True 

def plotECG(ui_element,sampling_rate=500):
    ecg_data = readSignalsFromCSV.read_ecg()
    # Cut data to the last two minutes
    if len(ecg_data) > sampling_rate*120 and CUTDATA_FLAG:
        ecg_data = ecg_data[-sampling_rate*120:]
    # Plot the ECG data
    ecg_fig = go.Figure()
    ecg_fig.add_trace(go.Scatter(x=(np.array(range((len(ecg_data))))/sampling_rate).tolist(), y=ecg_data, mode='lines', name='ECG', line=dict(color='red')))
    ecg_fig.update_layout(
        title='ECG Signal',
        xaxis_title='Time in seconds',
        xaxis = dict(
        tickmode = 'linear',
        tick0=0, dtick = 1,
        ),
        xaxis_ticksuffix = 's',
        yaxis_title='Signal Value',
        template='plotly_dark',
        #plot_bgcolor='rgba(30, 30, 30, 1)',  # Dark background for plot
        #paper_bgcolor='rgba(30, 30, 30, 1)',  # Dark background for paper
        height = 200,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    ui_element.plotly_chart(ecg_fig, use_container_width=True)



def UpdatePPGData(number = 1,sampling_rate=500):
    ppg_data = readSignalsFromCSV.read_ppg(number=number)
    # Cut data to the last two minutes
    if len(ppg_data) > sampling_rate*120 and CUTDATA_FLAG: 
        ppg_data = ppg_data[-sampling_rate*120:]
    # Draw the PPG data
    # ppg_data /= np.max(np.abs(ppg_data),axis=0)

    # Prepare data for analysis.
    # Apply the bandpass filter (set low and high cutoff frequencies based on heart rate)
    # low frequency cutoff in Hz (about 30 bpm)
    # high frequency cutoff in Hz (about 240 bpm)
    # sampling frequency of the data in Hz 
    ppg_data = bandpass_filter(ppg_data,lowcut=0.05,highcut=15,fs=100)
    return ppg_data
def PlotPPGData(ppg_data,uiElementArray,number = 1,sampling_rate=500):
    ppg_fig = go.Figure()
    ppg_fig.add_trace(go.Scatter(x=(np.array(range((len(ppg_data))))/sampling_rate).tolist(), y=ppg_data, mode='lines', name='PPG', line=dict(color='green')))
    ppg_fig.update_layout(
        title='PPG' +str(number) +' Signal',
        xaxis_title='Time in seconds',
        xaxis = dict(
        tickmode = 'linear',
        tick0=0, dtick = 1,
        ),
        xaxis_ticksuffix = 's',
        yaxis_title='Signal Value',
        template='plotly_dark',
        #plot_bgcolor='rgba(30, 30, 30, 1)',  # Dark background for plot
        #paper_bgcolor='rgba(30, 30, 30, 1)',  # Dark background for paper
        height = 200,
        margin=dict(l=0, r=0, t=30, b=0)
        
    )
    uiElementArray[number-1].plotly_chart(ppg_fig, use_container_width=True)
    