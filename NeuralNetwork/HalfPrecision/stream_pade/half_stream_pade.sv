/* verilator lint_off WIDTHEXPAND */

module half_stream_pade
#(
parameter BITS = 16,
parameter LENGTH = 10
)
(
input rstn,
input clk,
input in_valid,
input [BITS-1:0] a,
output logic out_valid,
output logic [BITS-1:0] c
);

half_pade_approximation_exp
half_pade_1
(
.rstn,
.clk,
//.in_valid,
.fpart(a),
//.out_valid,
.x(c)
);

endmodule
