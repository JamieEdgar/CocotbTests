module half_stream_multiply
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

half_multiply
multiply1
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
