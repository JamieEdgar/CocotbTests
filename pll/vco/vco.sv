module vco
#(
parameter BITS = 8
)
(
input clk,
input [BITS-1:0] x,
output real y
);

real angle = 0;
real offset;

always @(posedge clk)
  if (x != 0)
    offset = (2*3.14159*((1.0/(128+x))));
  else
    offset = 0;

always @(posedge clk)
  begin
    if ((angle + offset) < 3.14159*2)
      angle = (angle + offset);
    else
      angle = (angle + offset) - 3.14159*2;
  end

always_comb y = $cos(angle);

endmodule
