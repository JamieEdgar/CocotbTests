module registers
#(
parameter BITS=32
)
(
input rstn,
input clk,
input [4:0] rs,
input [4:0] rt,
input update,
input [4:0] rd,
input [BITS-1:0] din,
output [BITS-1:0] ds,
output [BITS-1:0] dt
);

logic [BITS-1:0] registers[32];

assign ds = registers[rs];
assign dt = registers[rt];

always @(posedge clk)
  begin
    if (!rstn)
      registers <= '{default: 0};
    else
      begin
        registers <= registers;
        if (update)
          if (rd != 0)
            registers[rd] <= din;
      end
  end

endmodule
