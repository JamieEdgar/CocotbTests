module second_order
#(
parameter BITS=8
)
(
input clk,
input [BITS-1:0] f,
output logic [2:0] dn = '0
);

logic c[2];
logic [BITS-1:0] ab[2];
logic c_d[2] = '{default: '0};

always @(posedge clk)
  begin
    dn[1:0] <= c[0] + c[1] - c_d[1];
    dn[2] <= (c[0] + c[1] == 0) ? c_d[1] : 0;
    c_d[1] <= c[1];
  end

stage
#(.BITS(BITS))
stage1
(
.clk,
.a(f),
.c(c[0]),
.ab(ab[0])
);

stage
#(.BITS(BITS))
stage2
(
.clk,
.a(ab[0]),
.c(c[1]),
.ab(ab[1])
);

endmodule
