import cocotb
from cocotb.triggers import Timer
import numpy as np
import sys
from pathlib import Path
proj_path = Path(__file__)
pkgs = proj_path.parent.parent.parent / 'NN_Packages/'
sys.path.append(str(pkgs))
from conversion_pkg import RealToHalf, DoubleFromHalf, VectorRealToHalf, MatrixRealToHalf
from conversion_pkg import VectorHalfToReal, BytesToReal
from testbench_functions_pkg import LoadImage, GetOneHotLabel

displayed = False
current_image = 0
image_solutions = [7, 2, 1, 0, 4, 1, 4, 9, 6, 9]
confidence = []
image_filename = "../../../fashion/t10k-images-idx3-ubyte"
label_filename = "../../../fashion/t10k-labels-idx1-ubyte"

async def toggle_clk(dut):
    dut.clk.value = 0
    await Timer(1, units="ns")
    dut.clk.value = 1
    await Timer(1, units="ns")
    check_for_results(dut)

async def release_reset(dut):
    dut.in_valid.value = 0
    dut.load_W1;value = 0
    dut.load_b1.value = 0
    dut.load_W2.value = 0
    dut.load_b2.value = 0
    dut.rstn.value = 1
    await toggle_clk(dut)
    dut.rstn.value = 0
    dut.in_valid.vlue = 0
    await toggle_clk(dut)
    dut.rstn.value = 1
    await toggle_clk(dut)

z_count = 0
a1_count = 0
a2_count = 0

def check_for_results(dut):
    global z_count, a1_count, a2_count
    global Z1, A1, A2
    if dut.half_predict_layer1_1.done_x_dot_W1_plus_b1.value:
        Z1[int(z_count % 50)][int(z_count / 50)] = DoubleFromHalf(int(dut.half_predict_layer1_1.x_dot_W1_plus_b1.value))
        z_count += 1
        if z_count >= 50*64:
            z_count = 0
    if dut.half_predict_layer1_1.out_valid.value:
        A1[int(a1_count % 50)][int(a1_count / 50)] = DoubleFromHalf(int(dut.half_predict_layer1_1.layer1_out.value))
        a1_count += 1
        if a1_count >= 50*64:
            a1_count = 0
    if dut.half_predict_layer2_1.out_valid.value:
        for i in range(10):
            A2[i][a2_count] = DoubleFromHalf(int(dut.half_predict_layer2_1.y[i].value))
        a2_count += 1
        if a2_count >= 64:
            a2_count = 0

async def load_matrix_halves(dut, r, c, mults, mat, label):
    #print("load_matrix_halves")
    for i in range(r):
        for j in range(int(c/mults)):
            for k in range(mults):
                # Note that rows are loaded in order, columns stream up.
                dut.neuron_data_in[k].value = (mat[i][c - mults -mults*j+k])
            #print(label, "neuron_data_in", i, VectorHalfToReal(dut.neuron_data_in.value))
            await toggle_clk(dut)
            #print(dut.neuron_data_in.value)

async def load_vector_halves(dut, l, mults, vec, label):
    #print("load vector halves")
    for i in range(int(l/mults)):
        for j in range(mults):
            dut.neuron_data_in[j].value = (vec[l-mults-(i*mults)+j])
        await(toggle_clk(dut))
        #print(label, "neuron_data_in", i, DoubleFromHalf(dut.neuron_data_in[0].value), l-mults-(i*mults)+0)

async def set_parameters(dut, w1data, b1data, w2data, b2data):
    global LAYER1_MULTS
    #print("load parameters")

    #print("loading w1data")
    dut.load_W1.value = 1
    await load_matrix_halves(dut, 50, 784, LAYER1_MULTS, w1data, "W1")
    dut.load_W1.value = 0

    #print("loading b1data")
    dut.load_b1.value = 1
    await load_vector_halves(dut, 50, 1, b1data, "b1")
    dut.load_b1.value = 0


    #print("loading w2data")
    dut.load_W2.value = 1
    await load_matrix_halves(dut, 10, 50, 1, w2data, "W2") # other input is ignored
    dut.load_W2.value = 0

    #print("loading b2data")
    dut.load_b2.value = 1
    await load_vector_halves(dut, 10, 1, b2data, "b2") # other input is ignored
    dut.load_b2.value = 0



async def test_vector(dut, l, mults, vec):
    #print("load vector")
    for i in range(int(l/mults)):
        for j in range(mults):
            dut.x[j].value = RealToHalf(vec[(i*mults)+j])
        dut.in_valid.value = 1
        await(toggle_clk(dut))
    dut.in_valid.value = 0

async def test_image(dut, offset, image_number):
    global LAYER1_MULTS
    global X, Y
    #print("test image")
    image = LoadImage(image_filename, image_number)
    image = BytesToReal(image)
    X[offset,:] = image
    #X[int(image_number%64)] /= 255.0   # done in bytes to real
    Y[offset,:] = GetOneHotLabel(label_filename, int(image_number))
    if (DEBUG): print("image_data", image_number, image)
    #print("max image", np.max(image))

    #print("loading image data")
    await test_vector(dut, 784, LAYER1_MULTS, image)

    count = 0
    while (count < 0):            # 0 works with latest setup
        await toggle_clk(dut)
        count = count + 1
        if count % 100 == 0:
            print(count)

def sigmoid_derivative(Z):
    s = 1 / (1 + np.exp(-Z))
    return s * (1 - s)

def update_parameters(X, Y, W1, B1, W2, B2):
    global A1, A2, Z1

    #print("Z1", Z1)
    #print("A1", A1)
    #print("A2", A2, np.mean(A2))
    batch = 64
    learning_rate = 0.1

    A = A2
    dZ = A - Y.T

    dw2 = dZ.dot(A1.T) / batch
    db2 = np.sum(dZ, axis=1, keepdims=True) / batch
    dAPrev = W2.T.dot(dZ)
    #print("db2", db2)

    dZ = dAPrev * sigmoid_derivative(Z1)
    #print("dZ", dZ, np.mean(dZ))
    dw1 = 1.0 / batch * dZ.dot(X)
    db1 = 1.0 / batch * np.sum(dZ, axis=1, keepdims=True)
    #print("dw1", dw1)

    W1 -= learning_rate * dw1
    B1 -= learning_rate * db1
    W2 -= learning_rate * dw2
    B2 -= learning_rate * db2

A2 = np.zeros((10, 64))
A1 = np.zeros((50, 64))
Z1 = np.zeros((50, 64))

X = np.zeros((64, 784))
Y = np.zeros((64, 10))

@cocotb.test()
async def my_first_test(dut):
    global LAYER1_MULTS, DEBUG, confidence
    global X, Y, z_count, a1_count, a2_count
    DEBUG = 0
    LAYER1_MULTS = int(dut.LAYER1_MULTS.value)
    print("LAYER1_MULTS", dut.LAYER1_MULTS.value)

    await release_reset(dut)
    #await load_parameters(dut)

    #np.random.seed(1)
    W1 = np.random.randn(50, 784) / np.sqrt(784)
    #print("max W1", np.max(W1))
    #print("min W1", np.min(W1))
    w1data = MatrixRealToHalf(W1)
    B1 = np.zeros((50, 1))
    b1data = VectorRealToHalf(B1)
    W2 = np.random.randn(10, 50) / np.sqrt(50)
    w2data = MatrixRealToHalf(W2)
    B2 = np.zeros((10, 1))
    b2data = VectorRealToHalf(B2)

    # 500 gave 7 of 10 correct similar to 3 epochs in software which runs all data 3 times (140 * 3)
    # Could add the inner loop to go through all data, this is just an approximation
    # 500 takes about 1.5 hours on a cheap laptop using CocoTB / Verilator
    # Streaming in the weights is very slow. Reading these from files could improve performance
    for epoch in range(10):
        print("epoch", epoch)
        #print("z_count, a1_count, a2_count", z_count, a1_count, a2_count)
        await set_parameters(dut, w1data, b1data, w2data, b2data)

        for i in range(64):
            ti = epoch*64 + i
            ti = np.random.randint(0, 8000)
            #print("test image", ti)
            await test_image(dut, i, ti)
            # Test -- does not help
            #for i in range(100):
            #    await toggle_clk(dut)

        for i in range(300):
            await toggle_clk(dut)

        update_parameters(X, Y, W1, B1, W2, B2)
        #print("X", X, np.mean(X))
        #print("Y", Y)
        w1data = MatrixRealToHalf(W1)
        b1data = VectorRealToHalf(B1)
        w2data = MatrixRealToHalf(W2)
        b2data = VectorRealToHalf(B2)
        #print("W1", W1)
        #print("B1", B1)
        #print("W2", W2)
        #print("w2data", w2data)
        #print("B2", B2)int(r-i-1)
        #print("b2data", b2data)


    await set_parameters(dut, w1data, b1data, w2data, b2data)
    epoch = 0
    for i in range(10):
        ti = epoch*64 + i
        print("test image", ti)
        await test_image(dut, i, ti)

    for i in range(300):
            await toggle_clk(dut)

    print("A2", A2[:,0:10])
    for i in range(10):
        max_value = np.max(A2[:,i])
        max_index = list(A2[:,i]).index(max_value)
        print("A2 Max", i, max_value, "selected index", max_index, "correct index", Y[i])


    for i in range(1000):
        await toggle_clk(dut)

    print("Confidence for selected images", confidence)
