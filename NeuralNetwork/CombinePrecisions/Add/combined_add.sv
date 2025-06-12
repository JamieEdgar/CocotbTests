`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 11/30/2018 01:21:10 AM
// Design Name: 
// Module Name: combined_add
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
/* verilator lint_off WIDTHEXPAND */

module combined_add
#(
parameter WIDTH = 32,
parameter EXP = 8,
parameter HIGH_BIT = WIDTH-1
)
(
input rstn,
input clk,
input in_valid,
input [HIGH_BIT:0] a,
input [HIGH_BIT:0] b,
output reg out_valid,
output wire [HIGH_BIT:0] c
);

localparam MAN_HIGH = WIDTH - 1 - EXP - 1;  // 32 - 1 - 8 - 1 = 22
localparam EXP_HIGH = WIDTH - 1 - 1;        // 32 - 1 - 1 = 30
localparam EXP_LOW = WIDTH - 1 - EXP;       // 32 - 1 - 8 = 23

localparam SUM_WIDTH =2*(MAN_HIGH+2)+1;
localparam SUM_SHIFT = MAN_HIGH+2;
localparam SUM_OFFSET = SUM_WIDTH/2+1;
localparam SUM_BITS = $clog2(SUM_WIDTH);

reg [HIGH_BIT:0] c_int;

wire [SUM_WIDTH-1:0] sum;

wire a_zero;
wire b_zero;
wire expa_gt_expb;
wire expb_gt_expa;
wire mana_gt_manb;
wire manb_gt_mana;
wire a_gt_b;
wire [SUM_BITS-1:0] ashift;
wire [SUM_BITS-1:0] bshift;
wire minus;
wire [SUM_BITS-1:0] leading_zeros;

assign c = c_int;

assign a_zero = (a == 0); 
assign b_zero = (b == 0);     
assign expa_gt_expb = (a[EXP_HIGH:EXP_LOW] > b[EXP_HIGH:EXP_LOW]) ? 1 : 0;
assign expb_gt_expa = (b[EXP_HIGH:EXP_LOW] > a[EXP_HIGH:EXP_LOW]) ? 1 : 0;
assign mana_gt_manb = (a[MAN_HIGH:0] > b[MAN_HIGH:0]) ? 1 : 0;
assign manb_gt_mana = (b[MAN_HIGH:0] > a[MAN_HIGH:0]) ? 1 : 0;
assign a_gt_b = (expa_gt_expb | (!expb_gt_expa & mana_gt_manb));
assign ashift = expb_gt_expa ? 
                    (b[EXP_HIGH:EXP_LOW] - a[EXP_HIGH:EXP_LOW] < SUM_SHIFT) ? b[EXP_HIGH:EXP_LOW] - a[EXP_HIGH:EXP_LOW] : SUM_SHIFT
                    : 0;
assign bshift = expa_gt_expb ? 
                    (a[EXP_HIGH:EXP_LOW] - b[EXP_HIGH:EXP_LOW] < SUM_SHIFT) ? a[EXP_HIGH:EXP_LOW] - b[EXP_HIGH:EXP_LOW] : SUM_SHIFT
                    : 0;                    
assign minus = a[HIGH_BIT] != b[HIGH_BIT];

always @(posedge clk)
  out_valid <= in_valid;                    

always @(posedge clk)
  if (!rstn)
    c_int[HIGH_BIT] <= 0;
  else
    c_int[HIGH_BIT] <= (a[HIGH_BIT] == b[HIGH_BIT]) ? a[HIGH_BIT] :
             expa_gt_expb ? a[HIGH_BIT] :
             expb_gt_expa ? b[HIGH_BIT] :
             mana_gt_manb ? a[HIGH_BIT] :
             manb_gt_mana ? b[HIGH_BIT] : 0;
             
always @(posedge clk)
  if (!rstn)
    c_int[EXP_HIGH:EXP_LOW] <= 0;
  else             
    c_int[EXP_HIGH:EXP_LOW] <= (leading_zeros < SUM_WIDTH) ?
                    expb_gt_expa ?
                    b[EXP_HIGH:EXP_LOW] + (8'b1 - leading_zeros):
                    a[EXP_HIGH:EXP_LOW] + (8'b1 - leading_zeros):
                    0;
                
always @(posedge clk)
  if (!rstn)
    c_int[MAN_HIGH:0] <= 0;
  else
    c_int[MAN_HIGH:0] <= (leading_zeros < SUM_WIDTH) ?
                       (leading_zeros < SUM_OFFSET) ?
                            sum >> (SUM_OFFSET - leading_zeros):
                            sum << (leading_zeros - SUM_OFFSET):
                       0;

assign sum = (minus) ?
                (a_gt_b) ?
                    ({1'b1,a[MAN_HIGH:0]} << (SUM_SHIFT - ashift)) - ({1'b1,b[MAN_HIGH:0]} << (SUM_SHIFT - bshift)) :
                    ({1'b1,b[MAN_HIGH:0]} << (SUM_SHIFT - bshift)) - ({1'b1,a[MAN_HIGH:0]} << (SUM_SHIFT - ashift)) :
                (a_zero) ?
                    (b_zero) ?
                         0 :
                    ({1'b1,b[MAN_HIGH:0]} << (SUM_SHIFT - bshift)) :
                (b_zero) ?
                    ({1'b1,a[MAN_HIGH:0]} << (SUM_SHIFT - ashift)) :
                    ({1'b1,a[MAN_HIGH:0]} << (SUM_SHIFT - ashift)) + ({1'b1,b[MAN_HIGH:0]} << (SUM_SHIFT - bshift));

leading_zero_count #(.WIDTH(SUM_WIDTH))
leading_zero_count1
(
.a(sum),
.c(leading_zeros)
);          

endmodule
