`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 12/01/2018 02:48:51 PM
// Design Name: 
// Module Name: half_predict_layer1
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


module half_predict_layer1
#(
parameter LAYER1_NEURONS = 10,
parameter LAYER2_NEURONS = 10,
parameter MULTS = 2
)
(
input rstn,
input clk,
input in_valid,
input load_W1,
input load_b1,
input [15:0] neuron_data_in[MULTS],
input [15:0] x[MULTS],
output out_valid,
output [15:0] layer1_out
);

wire [15:0] x_dot_W1;
wire done_x_dot_W1;
wire [15:0] x_dot_W1_plus_b1;
wire done_x_dot_W1_plus_b1;

half_fixed_matrix_dot_vector #(.WIDTH(LAYER1_NEURONS), .HEIGHT(LAYER2_NEURONS), .MULTS(MULTS))
half_fixed_matrix_dot_vector1
(
.rstn(rstn),
.clk(clk),
.in_valid(in_valid),
.load_matrix(load_W1),
.matrix_a_in(neuron_data_in),
.vector_b(x),
.out_valid(done_x_dot_W1),
.c(x_dot_W1)
);

half_fixed_vector_add_vector
#(.LENGTH(LAYER2_NEURONS))
half_add_v_v1
(
.rstn(rstn),
.clk(clk),
.in_valid(done_x_dot_W1),
.load_a(load_b1),
.vector_a_in(neuron_data_in[0]),
.vector_b(x_dot_W1),
.out_valid(done_x_dot_W1_plus_b1),
.c(x_dot_W1_plus_b1)
);

half_sigmoid
half_sigmoid1
(
.rstn,
.clk,
.in_valid(done_x_dot_W1_plus_b1),
.a(x_dot_W1_plus_b1),
.out_valid,
.c(layer1_out)
);

endmodule
