module alu
#(
parameter BITS=32,
parameter OPTION_BITS=8
)
(
input rstn,
input clk,
input [OPTION_BITS-1:0] select,
input [BITS-1:0] a,
input [BITS-1:0] b,
output logic [BITS-1:0] c,
output logic zero
);

localparam ADD = 6'h20;
localparam ADDI = 6'h08;
localparam AND = 6'h24;
localparam OR = 6'h25;
localparam ORI = 6'h0D;
localparam LW = 6'h23;
localparam SUB = 6'h22;
localparam SW = 6'h2B;
localparam MUL = 6'h3A; // note this combines parts of opcode and function
                        // this will allow clo and clz if desired

always_comb
  zero = (a == b) ? 1 : 0;

always_comb
  case (select)
    0:            c = a;
    ADD, ADDI,
    LW, SW:       c = a + b;
    AND:          c = a & b;
    MUL:          c = a * b;
    OR, ORI:      c = a | b;
    SUB:          c = a - b;
    default:      c = a;
  endcase

endmodule
