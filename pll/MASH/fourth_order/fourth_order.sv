module fourth_order
#(
parameter BITS=8
)
(
input clk,
input [BITS-1:0] f,
output logic [4:0] dn = '0
);

logic s0_c;
logic [BITS-1:0] s0_ab;
logic [3:0] s3_dn;
logic [3:0] s3_dn_d = '0;

always @(posedge clk)
  begin
    s3_dn_d <= s3_dn;
  end

always @(posedge clk)
  begin
    dn <= {4'b0, s0_c} +{s3_dn[3],s3_dn} - {s3_dn_d[3],s3_dn_d};
  end


third_order
#(.BITS(BITS))
third_order1
(
.clk,
.f(s0_ab),
.dn(s3_dn)
);

stage
#(.BITS(BITS))
stage0
(
.clk,
.a(f),
.c(s0_c),
.ab(s0_ab)
);

endmodule
