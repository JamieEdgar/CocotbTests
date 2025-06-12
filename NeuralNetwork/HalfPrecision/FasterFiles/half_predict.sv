`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 12/01/2018 02:46:49 PM
// Design Name: 
// Module Name: half_predict
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


module half_predict
#(
parameter LAYER1_NEURONS = 784,
parameter LAYER2_NEURONS = 50,
parameter OUTPUT_NODES = 10,
parameter LAYER1_MULTS = 2
)
(
input rstn,
input clk,
input in_valid,
input load_W1,
input load_b1,
input load_W2,
input load_b2,
input [15:0] x[LAYER1_MULTS],
input [15:0] neuron_data_in[LAYER1_MULTS],
output out_valid,
output [15:0] y[OUTPUT_NODES]
);

logic out_valid_layer1;
logic [15:0] layer1_out;

half_predict_layer1
#(
.LAYER1_NEURONS(LAYER1_NEURONS),
.LAYER2_NEURONS(LAYER2_NEURONS),
.MULTS(LAYER1_MULTS)
)
half_predict_layer1_1
(
.rstn,
.clk,
.in_valid,
.load_W1,
.load_b1,
.neuron_data_in,
.x,
.out_valid(out_valid_layer1),
.layer1_out
);

// Currently, layer 2 loads data in a single column
logic [15:0] layer_1_out_array[1];
logic [15:0] layer_2_neuron_data_in[1];

assign layer_1_out_array[0] = layer1_out;
assign layer_2_neuron_data_in[0] = neuron_data_in[0];

half_predict_layer2
#(
.LAYER2_NEURONS(LAYER2_NEURONS),
.OUTPUT_NODES(OUTPUT_NODES),
.MULTS(1)
)
half_predict_layer2_1
(
.rstn,
.clk,
.in_valid(out_valid_layer1),
.load_W2,
.load_b2,
.neuron_data_in(layer_2_neuron_data_in),
.x(layer_1_out_array),
.out_valid,
.y
);

endmodule
