/* verilator lint_off WIDTHTRUNC */
/* verilator lint_off WIDTHEXPAND */

module half_vector_dot_vector
#(
parameter BITS = 16,
parameter LENGTH = 10,
parameter MULTS = 2
)
(
input rstn,
input clk,
input in_valid,
input [BITS-1:0] vector_a[MULTS],
input [BITS-1:0] vector_b[MULTS],
output out_valid,
output logic [BITS-1:0] c
);

logic [BITS-1:0] c_mult[MULTS];
logic [BITS-1:0] c_mult_d[MULTS];
logic out_valid_mult[MULTS];
logic [BITS-1:0] sum;
logic in_valid_add;
logic [BITS-1:0] sum_in;
logic [$clog2(MULTS+1):0] count = MULTS+1;

always @(posedge clk)
    if (out_valid_mult[0])
        count <= 0;
    else
        if (count < MULTS+1)
            count <= count + 1;
        else
            count <= count;

always @(posedge clk)
    if (out_valid_mult[0])
        c_mult_d <= c_mult;
    else
        c_mult_d <= c_mult_d;

always_comb
    in_valid_add = (count < MULTS) ? 1 : 0;

always_comb
    if (count < MULTS)
        sum_in = c_mult_d[count];
    else
        sum_in = 0;

always_comb
    c = (out_valid) ? sum : 0;

genvar g;
for (g = 0; g < MULTS; g++)
half_stream_multiply_accumulate
#(
.BITS(BITS),
.LENGTH(LENGTH/MULTS)
)
mult_array
(
.rstn,
.clk,
.in_valid,
.a(vector_a[g]),
.b(vector_b[g]),
.out_valid(out_valid_mult[g]),
.c(c_mult[g])
);

half_stream_accumulate
#(
.BITS(BITS),
.LENGTH(MULTS)
)
accumulate
(
.rstn,
.clk,
.in_valid(in_valid_add),
.a(sum_in),
.out_valid,
.c(sum)
);



endmodule
