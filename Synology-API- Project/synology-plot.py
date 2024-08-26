import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('Synology-data.csv')

df["Timestamp"] = pd.to_datetime(df['Timestamp'])
timeswap = df.resample("60min", on='Timestamp')

def plot_temps():
    ax1 = plt.gca()
    plt.title("System Temperatures")

    ax1.plot(df['Timestamp'], df['Device Temperature'], color='skyblue', label="Device")
    plt.plot(df['Timestamp'], df['Disk Temperature-Drive 1'], label="Drive 1")
    plt.plot(df['Timestamp'], df['Disk Temperature-Drive 2'], label="Drive 2")
    plt.plot(df['Timestamp'], df['Disk Temperature-Drive 3'], label="Drive 3")
    plt.plot(df['Timestamp'], df['Disk Temperature-Drive 4'], label="Drive 4")
    plt.plot(df['Timestamp'], df['Disk Temperature-Drive 5'], label="Drive 5")
    plt.legend()
    plt.show()

def plot_percentages():
    ax1 = plt.gca()

    ax1.plot(df['Timestamp'], df['CPU Load'], color='purple', label='CPU Load')
    plt.plot(df['Timestamp'], df['RAM Usage'], color='#E6232E', label="RAM Usage")
    plt.plot(df['Timestamp'], df['Percentage-volume_1'], color='orange', label="Volume 1 Utilization")

    plt.legend()
    plt.show()

'''
Timestamp = X axis need to flop from TS to hours/mins
'''
plot_temps()
plot_percentages()
