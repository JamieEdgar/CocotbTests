`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 12/01/2018 10:59:56 AM
// Design Name: 
// Module Name: half_two_int_power
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

module half_two_int_power(
input rstn,
input clk,
input in_valid,
input [15:0] a,
output reg out_valid,
output reg [15:0] c
);

wire [4:0] exp;

assign exp = (a[14:10] > 14) ?
                (a[15]) ?
                    15 - ({1'b1,a[9:0]} >> (11 - (a[14:10] - 14) )) :
                    15 + ({1'b1,a[9:0]} >> (11 - (a[14:10] - 14) )) :
                15;
                
 always @(posedge clk)
   if (!rstn)     
     out_valid <= 0;
   else
     out_valid <= in_valid;          

always @(posedge clk)
  if (!rstn)
    c <= 0;
  else
    c <= {1'b0, exp , 10'b0 };

endmodule
