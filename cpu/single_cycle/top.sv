module top
#(
parameter BITS=32,
parameter PM_DEPTH=256,
parameter DM_DEPTH=256
)
(
input rstn,
input clk,
input pm_write_en,
input [$clog2(PM_DEPTH)+1:0] pm_write_address,
input [BITS-1:0] pm_data_in,
input dm_write_en,
input [$clog2(DM_DEPTH)-1:0] dm_write_address_load,
input [BITS-1:0] dm_data_in_load,
output logic debug
);

localparam RI = 6'h00;
localparam BEQ = 6'h04;
localparam LW = 6'h23;
localparam SW = 6'h2B;
localparam ADDI = 6'h08;
localparam MUL = 6'h2C;
localparam JUMP = 6'h02;

logic [BITS-1:0] pc;
logic [BITS-1:0] instruction;
logic [BITS-1:0] din;
logic [BITS-1:0] ds;
logic [BITS-1:0] dt;
logic [BITS-1:0] alu_out;
logic zero;
logic data_we;
logic [BITS-1:0] offset;
logic [BITS-1:0] absolute;
logic [BITS-1:0] alu_a;
logic [BITS-1:0] alu_b;
logic [BITS-1:0] immediate_se;
logic [BITS-1:0] dm_data_out;
logic [BITS-1:0] dm_data_in;
logic [1:0] jump;
logic immediate;
logic update;
logic [4:0] rd;
logic [$clog2(DM_DEPTH)-1:0] dm_write_address;

logic [5:0] select;
logic [5:0] opcode;
logic [5:0] alu_func;
logic [5:0] special_funct;

assign opcode = instruction[31:26];
assign alu_func = instruction[5:0];
assign special_funct = {instruction[30:28],alu_func[2:0]};
assign select = (opcode == RI) ? alu_func :
                (opcode == MUL) ? special_funct :
                                opcode;

assign immediate_se = {{16{instruction[15]}},instruction[15:0]};
assign offset = {{16{instruction[15]}},instruction[15:0]};
assign absolute = {4'b0,instruction[25:0],2'b0};
assign jump[0] = ((instruction[31:26] == BEQ) && zero) ? 1:0;
assign jump[1] = (instruction[31:26] == JUMP) ? 1:0;
assign immediate =  (   (instruction[31:26] == LW) ||
                        (instruction[31:26] == SW) ||
                        (instruction[31:26] == ADDI)
                    ) ? 1 : 0;

assign update    =  (   (instruction[31:26] ==RI) ||
                        (instruction[31:26] == LW) ||
                        (instruction[31:26] == ADDI)
                    ) ? 1 : 0;

assign rd =         (   (instruction[31:26] == ADDI) ||
                        (instruction[31:26] == LW)
                    ) ? instruction[20:16] : instruction[15:11];

assign din =        (   (instruction[31:26] == LW)
                    ) ? dm_data_out : alu_out;

assign data_we =    (   dm_write_en ||
                        (instruction[31:26] == SW)
                    ) ? 1'b1 : 1'b0;

assign dm_data_in = (   (instruction[31:26] == SW)
                    ) ? dt : dm_data_in_load;

assign dm_write_address = (   (instruction[31:26] == SW)
                          ) ? alu_out[$clog2(DM_DEPTH)-1:0] : dm_write_address_load;

program_counter
#(
.BITS(BITS)
)
pc1
(
.rstn,
.clk,
.pc_source(jump),
.offset,
.absolute,
.stall(1'b0),
.pc
);

unregistered_memory
#(
.BITS(BITS),
.DEPTH(PM_DEPTH)
)
pm
(
.rstn,
.clk,
.write_en(pm_write_en),
.write_address(pm_write_address[$clog2(PM_DEPTH)+1:2]),
.data_in(pm_data_in),
.read_address(pc[$clog2(PM_DEPTH)+1:2]),
.data_out(instruction)
);

registers
#(
.BITS(BITS)
)
reg1
(
.rstn,
.clk,
.rs(instruction[25:21]),
.rt(instruction[20:16]),
.update,
.rd,
.din,
.ds,
.dt
);

mux #(.BITS(BITS)) a_mux (.s(1'b0), .i0(ds), .i1(), .o(alu_a));
mux #(.BITS(BITS)) b_mux (.s(immediate), .i0(dt), .i1(immediate_se), .o(alu_b));

alu
#(
.BITS(BITS),
.OPTION_BITS(6)
)
alu1
(
.rstn,
.clk,
.select,
.a(alu_a),
.b(alu_b),
.c(alu_out),
.zero
);

unregistered_memory
#(
.BITS(BITS),
.DEPTH(DM_DEPTH)
)
dm
(
.rstn,
.clk,
.write_en(data_we),
.write_address(dm_write_address),
.data_in(dm_data_in),
.read_address(alu_out[$clog2(DM_DEPTH)-1:0]),
.data_out(dm_data_out)
);

endmodule
