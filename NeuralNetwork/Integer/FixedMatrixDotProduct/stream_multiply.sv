module stream_multiply
#(
parameter BITS = 16
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

always @(posedge clk)
    out_valid <= in_valid;

always @(posedge clk)
    if (in_valid)
        c <= a * b;
    else
        c <= 0;

endmodule
