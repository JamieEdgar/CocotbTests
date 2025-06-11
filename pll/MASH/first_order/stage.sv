module stage
#(
parameter BITS=8
)
(
input clk,
input [BITS-1:0] a,
output logic c = 0,
output logic [BITS-1:0] ab = '0
);

logic [BITS-1:0] b = '0;

always @(posedge clk)
  begin
    {c,ab} <= a + b;
    b <= ab;
  end

endmodule
