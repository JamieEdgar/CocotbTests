module half_stream_multiply_accumulate
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

logic out_valid_sm;
logic [BITS-1:0] c_sm;


half_multiply
stream_multiply1
(
.rstn,
.clk,
.in_valid,
.a,
.b,
.out_valid(out_valid_sm),
.c(c_sm)
);

 half_stream_accumulate
#(
.BITS(BITS),
.LENGTH(LENGTH)
)
stream_accumulate1
(
.rstn,
.clk,
.in_valid(out_valid_sm),
.a(c_sm),
.out_valid,
.c
);

endmodule
