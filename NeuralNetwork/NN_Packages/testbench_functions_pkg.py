from file_pkg import ReadDoubles
from conversion_pkg import *
import numpy as np

LAYER1_NEURONS = 784
LAYER2_NEURONS = 50
OUTPUT_NODES = 10

DEBUG = 0

#output logic [15:0] W1[LAYER1_NEURONS][LAYER2_NEURONS]
def LoadW1(FileName):
    if (DEBUG): print("W1")
    offset = 4916;
    W1 = []
    for i in range(784):
        count = 0;
        w1_data_set = ReadDoubles(FileName, offset, 50);
        if (DEBUG): print("W1 %d", i);
        offset2 = 0;
        new_row = []
        for j in range(50):
            new_row.append(DoubleToHalf(w1_data_set[j]));
            if (count < 10):
                  if (DEBUG): print(w1_data_set[j]);
                  count = count + 1;
                  if (DEBUG): print(DoubleFromHalf(W1[i][j]));
            offset = offset + 8;
            offset2 = offset2 + 8;
        offset = offset + 10;
        W1.append(new_row)
    return W1

# output logic [15:0] b1[LAYER2_NEURONS]
def Loadb1(FileName):
    offset = 4416
    b1_data_set = ReadDoubles(FileName, offset, 50)
    b1 = []
    for i in range(50):
        b1.append(DoubleToHalf(b1_data_set[i]))
    return b1

# output logic [15:0] W2[LAYER2_NEURONS][OUTPUT_NODES]
def LoadW2(FileName):
    offset = 326356
    W2 = []
    for i in range(50):
        new_row = []
        w2_data_set = ReadDoubles(FileName, offset, 10)
        for j in range(10):
            new_row.append(DoubleToHalf(w2_data_set[j]))
            offset = offset + 8
        offset = offset + 10
        W2.append(new_row)
    return W2

# output logic [15:0] b2[OUTPUT_NODES]
def Loadb2(FileName):
    offset = 4826
    b2_data_set = ReadDoubles(FileName, offset, 10)
    b2 = []
    for i in range(10):
        b2.append(DoubleToHalf(b2_data_set[i]))
        offset = offset + 8
    return b2

def LoadImage(image_file, image):
    with open(image_file, 'rb') as file:
        offset = 16 + 28 * 28 * image;
        image_bytes = 28 * 28
        SEEK_SET = 0
        file.seek(offset, SEEK_SET)
        data = file.read(image_bytes)
    return data

def GetOneHotLabel(label_file, image):
    with open(label_file, 'rb') as file:
        offset = 8 + image;
        image_bytes = 1
        SEEK_SET = 0
        file.seek(offset, SEEK_SET)
        data = file.read(image_bytes)
    result = np.zeros(10)
    result[data[0]] = 1
    return result

def CreateHalves(image_bytes):
    halves = []
    divisor = 255.0;
    for i in range(784):
        next_half = int(image_bytes[i]) / divisor;
        halves.append(DoubleToHalf(next_half))
    return halves

if __name__ == "__main__":
  print(LoadW1("../MNIST/mnist_network.bin"))
