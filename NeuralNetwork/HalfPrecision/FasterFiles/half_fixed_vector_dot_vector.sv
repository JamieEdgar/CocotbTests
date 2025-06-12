/* verilator lint_off WIDTHTRUNC */
/* verilator lint_off WIDTHEXPAND */

module half_fixed_vector_dot_vector
#(
parameter BITS = 16,
parameter LENGTH = 10,
parameter MULTS = 2
)
(
input rstn,
input clk,
input in_valid,
input load_a,
input [BITS-1:0] vector_a_in[MULTS],
input [BITS-1:0] vector_b[MULTS],
output out_valid,
output logic [BITS-1:0] c
);

logic [BITS-1:0] vector_a[LENGTH];
logic [BITS-1:0] a[MULTS];

logic in_valid_d = 0;
logic [$clog2(LENGTH/MULTS):0] count = 0;

always @(posedge clk)
    if (in_valid == 1)
        if (count < LENGTH/MULTS-1)
            count <= count + 1;
        else
            count <= 0;
    else
        count <= count;


always @(posedge clk)
    if (load_a)
        begin
            for (int i = 1; i < LENGTH/MULTS; i++)
                for (int j = 0; j < MULTS; j++)
                    vector_a[MULTS*i+j] <= vector_a[MULTS*(i-1)+j];
            for (int i = 0; i < MULTS; i++)
                vector_a[i] <= vector_a_in[i];
        end
    else
        vector_a <= vector_a;

genvar g;
for (g = 0; g < MULTS; g++)
always_comb
    a[g] = vector_a[count*MULTS + g];

half_vector_dot_vector
#(
.BITS(BITS),
.LENGTH(LENGTH),
.MULTS(MULTS)
)
half_vector_dot_vector1
(
.rstn,
.clk,
.in_valid,
.vector_a(a),
.vector_b,
.out_valid,
.c
);

endmodule
