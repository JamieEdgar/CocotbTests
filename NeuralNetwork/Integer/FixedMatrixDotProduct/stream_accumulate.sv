/* verilator lint_off WIDTHEXPAND */

module stream_accumulate
#(
parameter BITS = 8,
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

logic [BITS-1:0] sum;
logic [$clog2(LENGTH):0] count = 0;
logic first_sum = 1;
logic last_sum = 0;

assign out_valid = (last_sum) ? 1 : 0;
assign c = (last_sum) ? sum : 0;

always @(posedge clk)
    if (in_valid)
        if (count == LENGTH-1)
            last_sum <= 1;
        else
            last_sum <= 0;
    else
        last_sum <= 0;

always @(posedge clk)
  if (in_valid)
    if (count < LENGTH-1)
        count <= count + 1;
    else
        count <= 0;
  else
    count <= 0;

always @(posedge clk)
    if (in_valid)
        if (count == LENGTH-1)
            first_sum <= 1;
        else
            first_sum <= 0;
    else
        first_sum <= 0;

integer_add
#(
.BITS(BITS)
)
integer_add1
(
.rstn,
.clk,
.in_valid,
.a,
.b((first_sum != 1) ? sum : 0),
.out_valid(),
.c(sum)
);

endmodule
