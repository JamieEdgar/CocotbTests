module program_counter
#(
parameter BITS=32
)
(
input rstn,
input clk,
input stall,
input [1:0] pc_source,
input [BITS-1:0] offset,
input [BITS-1:0] absolute,
output logic [BITS-1:0] pc = 0
);

always @(posedge clk)
  if (!rstn)
    pc <= 0;
  else
    if (stall == 0)
      case (pc_source)
      1: pc <= pc + (offset[29:0] << 2); // already 1 inst past beq
      2: pc <= {pc[31:28],absolute[27:0]};
      default: pc <= pc + 4;
      endcase
    else
      pc <= pc;


endmodule
