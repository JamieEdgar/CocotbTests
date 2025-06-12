`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 12/01/2018 06:46:00 PM
// Design Name: 
// Module Name: half_predict_tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module half_predict_tb(
);

import conversions_pkg::*;
import testbench_functions_pkg::*;

string mnist_network_file = "../../../MNIST/mnist_network.bin";
string image_file = "../../../MNIST/t100-images.idx3-ubyte";

parameter LAYER1_NEURONS = 784;
parameter LAYER2_NEURONS = 50;
parameter OUTPUT_NODES = 10;

`define SEEK_SET 0
`define SEEK_CUR 1
`define SEEK_END 2

reg rstn;
reg clk;
reg start;
reg [15:0] x[LAYER1_NEURONS] = '{default: 0};
reg [15:0] W1[LAYER1_NEURONS][LAYER2_NEURONS] = '{default: '{default: 0}};
reg [15:0] b1[LAYER2_NEURONS] = '{default: 0};
reg [15:0] W2[LAYER2_NEURONS][OUTPUT_NODES] = '{default: '{default: 0}};
reg [15:0] b2[OUTPUT_NODES] = '{default: 0};
wire done;
wire [15:0] y[OUTPUT_NODES];

reg [7:0] memory[0:400000];
reg [7:0] image_bytes[784];
reg [15:0] image_halves[784];

wire [31:0] y_singles[OUTPUT_NODES];

generate
  genvar g;
  for (g = 0 ; g < OUTPUT_NODES; g = g + 1)
    assign y_singles[g] = SingleFromHalf(y[g]);
endgenerate

task LoadImage;
  input integer image;
  integer offset;
  integer r;
  integer fileId;
  begin
    fileId = $fopen(image_file, "rb");
    offset = 16 + 28 * 28 * image;
    r = $fseek(fileId, offset, `SEEK_SET);
    r = $fread(image_bytes, fileId);
    $fclose(fileId);
  end
endtask

task CreateHalves;
  integer i;
  real divisor;
  real data[784];
  begin
    divisor = 255.0;
    for (i = 0; i < 784; i = i + 1)
      begin
        data[i] = $itor(image_bytes[i]);
        data[i] = data[i] / divisor;
        image_halves[i] = DoubleToHalf(data[i]);
      end
  end
endtask

task SendImage;
  input integer i;
  begin
    LoadImage(i);
    CreateHalves();
    x = image_halves;
    start = 1;
    @(posedge clk);
    start = 0;
    @(posedge clk);
  end
endtask

initial
  begin
    rstn = 1;
    start = 0;
    @(posedge clk);
    @(posedge clk);
    rstn = 0;
    repeat (10) @(posedge clk);
    @(posedge clk);
    rstn = 1;
    @(posedge clk);
    @(posedge clk);
    LoadW1(mnist_network_file, W1);
    Loadb1(mnist_network_file, b1);
    LoadW2(mnist_network_file, W2);
    Loadb2(mnist_network_file, b2);
    @(posedge clk);
    SendImage(0);
    @(posedge clk);
    repeat(1250) @(posedge clk);
    rstn = 0;
    repeat(10) @(posedge clk);
    @(posedge clk);
    rstn = 1;
    repeat(10)@(posedge clk);
    @(posedge clk);
    SendImage(1);
    @(posedge clk);
    repeat(1250) @(posedge clk);
    rstn = 0;
    repeat(10) @(posedge clk);
    @(posedge clk);
    rstn = 1;
    repeat(10) @(posedge clk);
    @(posedge clk);
    SendImage(2);
    @(posedge clk);
    repeat(1250) @(posedge clk);
    @(posedge clk);
    //$stop;
  end

initial
  begin
    clk = 0;
    forever #10 clk = ~clk;
  end

half_predict #(.LAYER1_NEURONS(LAYER1_NEURONS), .LAYER2_NEURONS(LAYER2_NEURONS),
                 .OUTPUT_NODES(OUTPUT_NODES))
half_predict1
(
.rstn(rstn),
.clk(clk),
.start(start),
.x(x),
.W1(W1),
.b1(b1),
.W2(W2),
.b2(b2),
.done(done),
.y(y)
);

endmodule
