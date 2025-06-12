module stream_multiply
#(
parameter LENGTH = 10
)
(
input   clk,
input in_valid,
input [7:0] a,
input [7:0] b,
output logic out_valid,
output logic [15:0] c
);

always @(posedge clk)
    out_valid <= in_valid;

always @(posedge clk)
    if (in_valid)
        c <= a * b;
    else
        c <= 0;

endmodule
