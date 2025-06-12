/* verilator lint_off WIDTHEXPAND */

module half_stream_fm_exp2
#(
parameter BITS = 16,
parameter LENGTH = 10
)
(
input rstn,
input clk,
input in_valid,
input [BITS-1:0] a,
output logic out_valid,
output logic [BITS-1:0] c
);

half_fm_exp2
half_fm_exp2_1
(
.rstn,
.clk,
.in_valid,
.a,
.out_valid,
.c
);

endmodule
