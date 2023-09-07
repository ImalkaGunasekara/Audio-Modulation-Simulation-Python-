import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

while True:
    # message signal
    message_frequency = int(input("message signal frequency(fm): "))
    message_amplitude = int(input("message signal amplitude(Am): "))

    sampling_rate = (message_frequency) * 100
    duration = (1 / message_frequency) * 4
    # X-axis
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    message_signal = message_amplitude * (np.cos(2 * np.pi * message_frequency * t))

    modulation_type = input("Modulation type (AM,DSB-SC,FM): ").upper()
    if modulation_type == "AM":
        carrier_frequency = int(input("carrier signal frequency_fc_(~2fm): "))
        carrier_amplitude = int(input("carrier signal amplitude_Ac_(>Am): "))
        carrier_signal = carrier_amplitude * (np.cos(2 * np.pi * carrier_frequency * t))

        AM_modulated_signal = (carrier_amplitude + message_signal) * (np.cos(2 * np.pi * carrier_frequency * t))


        # DEMODULATING

        # Define a simple low-pass filter
        def butter_lowpass(cutoff, fs, order=5):
            nyquist = 0.5 * fs
            normal_cutoff = cutoff / nyquist
            b, a = butter(order, normal_cutoff, btype='low', analog=False)
            return b, a


        # Apply the low-pass filter to the AM modulated signal
        cutoff_frequency = message_frequency + 60  # Adjust this value as needed
        b, a = butter_lowpass(cutoff_frequency, sampling_rate)
        filtered_am_modulated_signal = lfilter(b, a, AM_modulated_signal)


        # Define a moving average filter
        def moving_average(data, window_size):
            return np.convolve(data, np.ones(window_size) / window_size, mode='same')


        # Apply the moving average filter to the  signal
        window_size = 50  # Adjust this value as needed
        smoothed_signal = moving_average(filtered_am_modulated_signal, window_size)

        plt.figure(figsize=(12, 6))
        plt.subplot(4, 1, 1)
        plt.plot(t, message_signal)
        plt.xlabel("Time(s)")
        plt.ylabel("Amplitude")
        plt.title("Message signal m(t)")

        plt.subplot(4, 1, 2)
        plt.plot(t, AM_modulated_signal)
        plt.xlabel("Time(s)")
        plt.ylabel("Amplitude")
        plt.title("AM signal s(t)")

        plt.subplot(4, 1, 3)
        plt.plot(t, filtered_am_modulated_signal)
        plt.xlabel("Time(s)")
        plt.ylabel("Amplitude")
        plt.title("filtered signal")

        plt.subplot(4, 1, 4)
        plt.plot(t, smoothed_signal)
        plt.xlabel("Time(s)")
        plt.ylabel("Amplitude")
        plt.title("Smoothed demodulated signal")
        plt.tight_layout()
        plt.show()

    elif modulation_type == "DSB-SC":
        carrier_frequency = int(input("carrier signal frequency_fc_(~2fm): "))
        carrier_amplitude = int(input("carrier signal amplitude_Ac_(>Am): "))
        carrier_signal = carrier_amplitude * (np.cos(2 * np.pi * carrier_frequency * t))

        # Obtain the DSB-SC modulated signal
        amplitude_modulated_signal = message_signal * carrier_signal

        # DEMODULATING
        corrected_carrier_signal = carrier_amplitude * (np.cos(2 * np.pi * carrier_frequency * t + np.pi))

        # Demodulate the signal using coherent detection
        output_signal = amplitude_modulated_signal * corrected_carrier_signal


        # Define a simple low-pass filter
        def butter_lowpass(cutoff, fs, order=5):
            nyquist = 0.5 * fs
            normal_cutoff = cutoff / nyquist
            b, a = butter(order, normal_cutoff, btype='low', analog=False)
            return b, a


        # Apply the low-pass filter to the AM modulated signal
        cutoff_frequency = message_frequency + 60  # Adjust this value as needed
        b, a = butter_lowpass(cutoff_frequency, sampling_rate)
        demodulated_signal = lfilter(b, a, output_signal)

        plt.figure(figsize=(12, 6))
        plt.subplot(3, 1, 1)
        plt.plot(t, message_signal)
        plt.xlabel("Time(s)")
        plt.ylabel("Amplitude")
        plt.title("Message signal m(t)")

        plt.subplot(3, 1, 2)
        plt.plot(t, amplitude_modulated_signal)
        plt.xlabel("Time(s)")
        plt.ylabel("Amplitude")
        plt.title("Amplitude Modulated Signal(DSB-SC) s(t)")

        plt.subplot(3, 1, 3)
        plt.plot(t, demodulated_signal)
        plt.xlabel("Time(s)")
        plt.ylabel("Amplitude")
        plt.title("Demodulated signal m(t)")
        plt.tight_layout()
        plt.show()

    elif modulation_type == "FM":
        pass

    try_again=input("Do you want to modulate another signal(yes/no): ").lower()
    if try_again != "yes":
        break


print("bye")




