/* verilator lint_off WIDTHEXPAND */

module half_stream_divide
#(
parameter BITS = 16,
parameter LENGTH = 10
)
(
input rstn,
input clk,
input in_valid,
input [BITS-1:0] a,
input [BITS-1:0] b,
output logic out_valid,
output logic [BITS-1:0] c
);

half_divide
half_divide1
(
.rstn,
.clk,
.in_valid,
.a,
.b,
.out_valid,
.c
);

endmodule
