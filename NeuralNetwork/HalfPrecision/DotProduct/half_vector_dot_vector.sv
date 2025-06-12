module half_vector_dot_vector
#(
parameter WIDTH = 10,
parameter MULTS = 2
)
(
input rstn,
input clk,
input start,
input [15:0] vector_a[MULTS],
input [15:0] vector_b[MULTS],
output done,
output [15:0] c
);

endmodule
