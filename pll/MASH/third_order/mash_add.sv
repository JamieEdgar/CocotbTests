/* verilator lint_off WIDTHEXPAND */

module mash_add
(
input c,
input [2:0] dn,
input [2:0] dn_d,
output logic [3:0] result
);

always_comb
    result = {3'b0,c} + {dn[2],dn} - {dn_d[2],dn_d};

endmodule
