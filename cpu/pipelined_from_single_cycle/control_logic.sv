module control_logic
#(
parameter BITS=32
)
(
input rstn,
input clk,
input [BITS-1:0] instruction,
output logic reg_imed,
output logic dm_write,
output logic reg_write
);

always_comb
  reg_imed = () ? 1 : 0;

always_comb
  dm_write = () ? 1 : 0;

always_comb
  reg_write = () ? 1 : 0;

endmodule
