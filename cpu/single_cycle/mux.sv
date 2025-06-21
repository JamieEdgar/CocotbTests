module mux
#(
parameter BITS=32
)
(
input s,
input [BITS-1:0] i0,
input [BITS-1:0] i1,
output [BITS-1:0] o
);

assign o = s ? i1 : i0;

endmodule
