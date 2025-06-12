`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 12/01/2018 04:52:42 PM
// Design Name: 
// Module Name: half_predict_layer1_tb
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

/* verilator lint_off WIDTHTRUNC */

module read_W1_tb(
);

import conversions_pkg::*;
import file_pkg::*;
import testbench_functions_pkg::*;

parameter LAYER1_NEURONS = 784;
parameter LAYER2_NEURONS = 50;

`define SEEK_SET 0
`define SEEK_CUR 1
`define SEEK_END 2

reg rstn;
reg clk;
reg start;
reg [15:0] x[LAYER1_NEURONS];
reg [15:0] xzeros[LAYER1_NEURONS] = '{default: 0};
reg [15:0] W1[LAYER1_NEURONS][LAYER2_NEURONS];
reg [15:0] W1zeros[LAYER1_NEURONS][LAYER2_NEURONS] = '{default: '{default: 0}};
reg [15:0] b1[LAYER2_NEURONS];
reg [15:0] b1zeros[LAYER2_NEURONS] = '{default: 0};
wire done;
wire [15:0] l[LAYER2_NEURONS];

reg [7:0] memory[0:76815];
reg [7:0] memory2[0:50*8-1];
reg [7:0] memory3[0:7];
integer fileId;
integer imageFileId;
reg [7:0] image_bytes[784];
reg [15:0] image_halves[784];

wire [31:0] l_singles[LAYER2_NEURONS];

integer count = 0;

/*
generate
  genvar g;
  for (g = 0 ; g < LAYER2_NEURONS; g = g + 1)
    assign l_singles[g] = SingleFromHalf(l[g]);
endgenerate
*/

task ReadFile;
  integer r;
  begin
    fileId = $fopen("../../../MNIST/mnist_network.bin", "rb");
    $display("fileID = %d", fileId);
    r = $fread(memory, fileId);
    $fclose(fileId);
  end
endtask

string FileName = "../../../MNIST/mnist_network.bin";

initial
  begin
    testbench_functions_pkg::DEBUG = 1;
    rstn = 1;
    start = 0;
    x = xzeros;
    W1 = W1zeros;
    b1 = b1zeros;
    @(posedge clk);
    @(posedge clk);
    rstn = 0;
    repeat (10) @(posedge clk);
    @(posedge clk);
    rstn = 1;
    @(posedge clk);
    @(posedge clk);
    LoadW1(FileName, W1);
    @(posedge clk);
    repeat (100) @(posedge clk);
    //$stop;
  end

initial
  begin
    clk = 0;
    forever #10 clk = ~clk;
  end

endmodule
