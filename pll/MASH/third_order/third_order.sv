module third_order
#(
parameter BITS=8
)
(
input clk,
input [BITS-1:0] f,
output logic [3:0] dn = '0
);

logic s0_c;
logic [BITS-1:0] s0_ab;
logic [2:0] s2_dn;
logic [2:0] s2_dn_d = '0;

always @(posedge clk)
  begin
    s2_dn_d <= s2_dn;
  end

always @(posedge clk)
  begin
    //dn <= {2'b0, s0_c} + s2_dn - s2_dn_d; more bits are needed for fourth order
    dn <= {3'b0, s0_c} +{s2_dn[2],s2_dn} - {s2_dn_d[2],s2_dn_d};
  end

second_order second_order1
(
.clk,
.f(s0_ab),
.dn(s2_dn)
);

stage stage0
(
.clk,
.a(f),
.c(s0_c),
.ab(s0_ab)
);

endmodule
