/* verilator lint_off WIDTHTRUNC */
/* verilator lint_off WIDTHEXPAND */

module half_fixed_matrix_dot_vector
#(
parameter BITS = 16,
parameter WIDTH = 40,
parameter HEIGHT = 10,  // Module assumes HEIGHT < WIDTH/MULTS
parameter MULTS = 2
)
(
input rstn,
input clk,
input in_valid,
input load_matrix,
input [BITS-1:0] matrix_a_in[MULTS],
input [BITS-1:0] vector_b[MULTS],
output logic out_valid,
output logic [BITS-1:0] c
);

logic [$clog2(WIDTH/MULTS):0] sample_in_count = 0;
logic [$clog2(HEIGHT):0] row_in_count = 0;

logic out_valids[HEIGHT];
logic [BITS-1:0] cs[HEIGHT];
logic [BITS-1:0] cs_reg[HEIGHT];

logic [$clog2(HEIGHT+1):0] count = HEIGHT+1;

always @(posedge clk)
    if (out_valids[0])
        cs_reg <= cs;
    else
        cs_reg <= cs_reg;

always @(posedge clk)
    if (out_valids[0] == 1)
        count <= 0;
    else
        if (count < HEIGHT+1)
            count <= count + 1;
        else
            count <= count;

always @(posedge clk)
    if ((count > 0) && (count < HEIGHT+1))
        c <= cs_reg[count-1];
    else
        c <= 0;

always @(posedge clk)
    out_valid <= ((count > 0) && (count < HEIGHT+1)) ? 1 : 0;

always @(posedge clk)
    if (load_matrix)
        if (sample_in_count == WIDTH/MULTS-1)
            sample_in_count <= 0;
        else
            sample_in_count <= sample_in_count + 1;
    else
        sample_in_count <= 0;

always @(posedge clk)
    if (load_matrix)
        if (sample_in_count == WIDTH/MULTS-1)
            if (row_in_count == HEIGHT-1)
                row_in_count <= 0;
            else
                row_in_count <= row_in_count + 1;
        else
            row_in_count <= row_in_count;
    else
        row_in_count <= 0;

genvar g;
for (g = 0; g < HEIGHT; g++)
half_fixed_vector_dot_vector
#(
.BITS(BITS),
.LENGTH(WIDTH),
.MULTS(MULTS)
)
vector_dps
(
.rstn,
.clk,
.in_valid,
.load_a((row_in_count == g) && load_matrix),
.vector_a_in(matrix_a_in),
.vector_b,
.out_valid(out_valids[g]),
.c(cs[g])
);

endmodule
