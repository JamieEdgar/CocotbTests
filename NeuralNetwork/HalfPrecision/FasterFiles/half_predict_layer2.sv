`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 12/01/2018 02:50:50 PM
// Design Name: 
// Module Name: half_predict_layer2
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


module half_predict_layer2
#(
parameter LAYER2_NEURONS = 10,
parameter OUTPUT_NODES = 10,
parameter MULTS = 1
)
(
input rstn,
input clk,
input in_valid,
input load_W2,
input load_b2,
input [15:0] neuron_data_in[MULTS],
input [15:0] x[MULTS],
output out_valid,
output [15:0] y[OUTPUT_NODES]
);

wire [15:0] x_dot_W2;
wire done_x_dot_W2;
wire [15:0] x_dot_W2_plus_b2;
wire done_x_dot_W2_plus_b2;
wire out_valid_stream_to_vector;
wire [15:0] stream_to_vector_output[OUTPUT_NODES];


half_fixed_matrix_dot_vector #(.WIDTH(LAYER2_NEURONS), .HEIGHT(OUTPUT_NODES), .MULTS(MULTS))
half_fixed_matrix_dot_vector1
(
.rstn(rstn),
.clk(clk),
.in_valid(in_valid),
.load_matrix(load_W2),
.matrix_a_in(neuron_data_in),
.vector_b(x),
.out_valid(done_x_dot_W2),
.c(x_dot_W2)
);

half_fixed_vector_add_vector
#(.LENGTH(OUTPUT_NODES))
half_add_v_v1
(
.rstn(rstn),
.clk(clk),
.in_valid(done_x_dot_W2),
.load_a(load_b2),
.vector_a_in(neuron_data_in[0]),
.vector_b(x_dot_W2),
.out_valid(done_x_dot_W2_plus_b2),
.c(x_dot_W2_plus_b2)
);

half_stream_to_vector
#
(
.BITS(16),
.LENGTH(OUTPUT_NODES)
)
half_stream_to_vector1
(
.rstn,
.clk,
.in_valid(done_x_dot_W2_plus_b2),
.x(x_dot_W2_plus_b2),
.out_valid(out_valid_stream_to_vector),
.y(stream_to_vector_output)
);

half_softmax_v #(.WIDTH(OUTPUT_NODES))
half_softmax_v1
(
.rstn(rstn),
.clk(clk),
.start(out_valid_stream_to_vector),
.vector_a(stream_to_vector_output),
.done(out_valid),
.vector_c(y)
);

endmodule
