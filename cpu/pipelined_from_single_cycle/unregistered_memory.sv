module unregistered_memory
#(
parameter BITS=32,
parameter DEPTH=256
)
(
input rstn,
input clk,
input write_en,
input [$clog2(DEPTH)-1:0] write_address,
input [BITS-1:0] data_in,
input [$clog2(DEPTH)-1:0] read_address,
output logic [BITS-1:0] data_out
);

logic [BITS-1:0] memory[DEPTH];

assign data_out = memory[read_address];

always @(posedge clk)
  begin
    memory <= memory;
    if (write_en)
        memory[write_address] <= data_in;
  end

endmodule
