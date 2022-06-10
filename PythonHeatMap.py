import serial, os, time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

i = 0
t_0 = time.time()
enc = 'utf-8'
r = 24
c = 10
m = [[0 for x in range(c)] for y in range(r)]


# ser = serial.Serial('/dev/tty.usbmodem14103', 230400, timeout=1)


# ser = serial.Serial('/dev/tty.usbmodem14103', 115200, timeout=1)


def readTriplet():
    """
    16-bit data is sent as triplet pattern of 3 Bytes.
    Start byte is 0x00, second byte is LSB, second bit is MSB
    Transfer is started on first detected start byte, is reset in case of pattern mismatch
    :return: decoded uint16 value
    """
    while not ord(ser.read()) == 0:  # Wait for start byte
        pass
    data = ord(ser.read()) + (ord(ser.read()) << 8)  # Construct 16-bit int from LSB and MSB
    # print(data)
    return data


def generate_matrix():
    while not (readTriplet() == 0xffff):  # Wait for new frame signal
        pass
    for x in range(c):
        for y in range(r):
            val_read = readTriplet()
            if val_read == 0xffff:
                break
            else:
                # print(val_read)
                m[y][x] = int(val_read)
    # print(m)
    # print('\n'.join([' '.join([f'{item:6}' for item in row]) for row in m]))
    return m


def nextFrame(matrix):
    pad.set_data(matrix)
    print(ser.in_waiting)
    return pad


def matrixGenerator():
    while True:
        yield generate_matrix()


with serial.Serial('/dev/tty.usbmodem14103', 230400, timeout=1) as ser:
    n = 0
    fig, ax = plt.subplots()
    pad = ax.matshow(generate_matrix(), vmin=0, vmax=4095)
    ax.autoscale(False)
    plt.colorbar(pad)
    an = animation.FuncAnimation(fig, nextFrame, matrixGenerator)
    plt.show()
