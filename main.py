import uhd
import numpy as np
import matplotlib.pyplot as plt

run = True
def setUp():
    usrp = uhd.usrp.MultiUSRP()
    usrp.set_rx_rate(10e6, 0)
    usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(101e6), 0)
    usrp.set_rx_gain(10, 0)
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
    return usrp, metadata, recv_buffer, streamer


# Receive Samples
def rx(usrp, metadata, recv_buffer, streamer):
    num_samps = 10000
    sample_rate = usrp.get_rx_rate()
    center_freq = usrp.get_rx_freq()
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


# Plot freq domain
start = setUp()
while run:
    try:
        rx(start[0], start[1], start[2], start[3])
    except KeyboardInterrupt:
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
        start[3].issue_stream_cmd(stream_cmd)
        run = False