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
logic [BITS-1:0] immediate_se; // sign extended
logic [BITS-1:0] dm_data_out;
logic [BITS-1:0] dm_data_in;
logic [1:0] jump;
logic immediate;
logic update;
logic [4:0] rs;
logic [4:0] rt;
logic [4:0] rd;
logic [$clog2(DM_DEPTH)-1:0] dm_write_address;

logic [5:0] select;
logic [5:0] opcode;
logic [5:0] alu_func;
logic [5:0] special_funct;
logic [5:0] opcode_pre;
logic [5:0] opcode_d;
logic [5:0] opcode_d2;
logic [5:0] opcode_d3;
logic [BITS-1:0] dt_d;

always @(posedge clk)
    opcode_d <= opcode;

always @(posedge clk)
    opcode_d2 <= opcode_d;

always @(posedge clk)
    opcode_d3 <= opcode_d2;

always @(posedge clk)
    dt_d <= dt;

assign opcode_pre = instruction_pre[31:26];
assign opcode = instruction[31:26];
assign alu_func = instruction[5:0];
assign rs = instruction[25:21];
assign rt = instruction[20:16];

// Pipeline registers
logic [BITS-1:0] instruction_pre;
logic [BITS-1:0] alu_out_pre;
logic [BITS-1:0] dt_pre;
logic [BITS-1:0] ds_pre;
logic [BITS-1:0] dm_data_out_pre;

logic update_pre;
logic update_pre2;
logic update_pre3;

logic [5:0] select_pre;

logic [4:0] rd_d;
logic [4:0] rd_d1;
logic [4:0] rd_d2;

logic [2:0] register_busy[32];
logic stall;
logic stall_d;

always @(posedge clk)
    stall_d <= stall;

always_comb
    stall = (register_busy[instruction_pre[25:21]] > 0) ||
            ((opcode_pre != JUMP) && (opcode != JUMP) && (!stall_d && instruction_pre[25:21] == rd) && (rd != 0)); // (register_busy[instruction[25:21]] > 0) ||

always @(posedge clk)
  if (!rstn)
    register_busy <= '{default:0};
  else
    begin
      for (int i = 0; i < 32; i++)
        if (register_busy[i] > 0)
          register_busy[i] <= register_busy[i] -1;
        else
          register_busy[i] <= 0;
      for (int i = 1; i < 32; i++)  // Intensionally skip register 0
        if (rd == i[4:0] && register_busy[i] == 0)
          if (opcode == LW)
            register_busy[i] <= 2;
          else
            register_busy[i] <= 1;
    end


always @(posedge clk)
  if (!rstn)
    update <= 0;
  else
    update <= update_pre;

always @(posedge clk)
  if (!rstn)
    instruction <= 0;
  else
    if ((stall == 1) || jump[0] || jump[1])
        instruction <= 0;
    else
        instruction <= instruction_pre;

always @(posedge clk)
  if (!rstn)
    alu_out <= 0;
  else
    alu_out <= alu_out_pre;

always @(posedge clk)
  if (!rstn)
    dt <= 0;
  else
    dt <= dt_pre;

always @(posedge clk)
  if (!rstn)
    ds <= 0;
  else
    ds <= ds_pre;

always @(posedge clk)
  if (!rstn)
    dm_data_out <= 0;
  else
    dm_data_out <= dm_data_out_pre;

assign special_funct = {instruction[30:28],alu_func[2:0]};
assign select_pre = (opcode == RI) ? alu_func :
                (opcode == MUL) ? special_funct :
                                opcode;
always @(posedge clk)
    select <= select_pre;

always @(posedge clk)
    immediate_se <= {{16{instruction[15]}},instruction[15:0]};
assign offset = {{16{instruction[15]}},instruction[15:0]};
assign absolute = {4'b0,instruction[25:0],2'b0};
assign jump[0] = (opcode == BEQ) && (ds_pre==dt_pre) ? 1:0; // Need zero right away
assign jump[1] = (opcode == JUMP) ? 1:0;
always @(posedge clk)
    immediate <=  (   (opcode == LW) ||
                        (opcode == SW) ||
                        (opcode == ADDI)
                    ) ? 1 : 0;

always @ (posedge clk)
    update_pre    <=  (((opcode == RI) && (alu_func != 0)) ||
                        (opcode_d == LW) ||                // This means LW can not be
                        (opcode == ADDI)    //followed by reg write
                    ) ? 1 : 0;

always @(posedge clk)
  begin
    rd_d1    <= 0;
    if  ((opcode == RI) ||  // This means LW can not be
        (opcode == ADDI))   //followed by reg write
        rd_d1 <= rd;
    if (rd_d2 != 0)
        rd_d1 <= rd_d2;
  end

always @(posedge clk)
    rd_d <= rd_d1;

always @(posedge clk)
  if (!rstn)
    rd_d2 <= 0;
  else
    if (opcode == LW)
      begin
        rd_d2 <= rd;
        update_pre3 <= 1;
      end
    else
      begin
        rd_d2 <= 0;
        update_pre3 <= 0;
      end

assign rd =         (   (opcode == ADDI) ||
                        (opcode == LW)
                    ) ? instruction[20:16] : instruction[15:11];

assign din =        (   (opcode_d3 == LW)
                    ) ? dm_data_out : alu_out;

logic data_write_en_pre;
logic data_write_en_pre2;

assign data_we =    (   dm_write_en ||
                        (opcode_d2 == SW)
                    ) ? 1'b1 : 1'b0;

always @(posedge clk)
    data_write_en_pre <= data_write_en_pre2;

always @(posedge clk)
  begin
    data_write_en_pre2 <= 0;
    if ((opcode == SW) && ((stall==0) || (update == 1)))
      data_write_en_pre2 <= 1;
  end

assign dm_data_in = (   (opcode_d2 == SW)
                    ) ? dt_d : dm_data_in_load;

assign dm_write_address = (   (opcode_d2 == SW)
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
.stall,
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
.data_out(instruction_pre)
);

registers
#(
.BITS(BITS)
)
reg1
(
.rstn,
.clk,
.rs,
.rt,
.update,
.rd(rd_d),
.din,
.ds(ds_pre),
.dt(dt_pre)
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
.c(alu_out_pre),
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
.data_out(dm_data_out_pre)
);

endmodule
