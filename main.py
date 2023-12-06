import uhd
import numpy as np
import matplotlib.pyplot as plt
from signal import Signal


def set_up():
    signal = Signal()
    usrp = uhd.usrp.MultiUSRP()
    usrp.set_rx_rate(signal.rate, 0)
    usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(signal.freq), 0)
    usrp.set_rx_gain(signal.gain, 0)
    # Set up the stream and receive buffer
    st_args = uhd.usrp.StreamArgs("fc32", "sc16")
    st_args.channels = [0]
    metadata = uhd.types.RXMetadata()
    streamer = usrp.get_rx_stream(st_args)
    recv_buffer = np.zeros((1, 1000), dtype=np.complex64)
    # Start Stream
    stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
    stream_cmd.stream_now = True
    streamer.issue_stream_cmd(stream_cmd)
    return usrp, metadata, recv_buffer, streamer, signal


# Receive Samples
def rx(metadata, recv_buffer, streamer, signal):
    num_samps = signal.num_samps
    sample_rate = signal.rate
    center_freq = signal.freq
    rx_samples = np.zeros(num_samps, dtype=np.complex64)
    for i in range(num_samps//1000):
        streamer.recv(recv_buffer, metadata)
        rx_samples[i*1000:(i+1)*1000] = recv_buffer[0]

# Calculate power spectral density (frequency domain version of signal)
    psd = np.abs(np.fft.fftshift(np.fft.fft(rx_samples)))**2
    psd_dB = 10*np.log10(psd)
    f = np.linspace(sample_rate/-2 + center_freq, sample_rate/2 + center_freq, len(psd))
    plt.cla()
    plt.plot(f/1e6, psd_dB)
    plt.draw()
    plt.ylim(-50, 50)
    plt.xlabel("Frequency [MHz]")
    plt.ylabel("PSD")
    plt.pause(0.01)

run = True
# Plot freq domain
start = set_up()
while run:
    try:
        rx(start[1], start[2], start[3], start[4])
    except KeyboardInterrupt:
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
        start[3].issue_stream_cmd(stream_cmd)
        run = False
