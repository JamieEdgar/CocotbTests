/* verilator lint_off WIDTHTRUNC */
/* verilator lint_off WIDTHEXPAND */

module half_fixed_vector_add_vector
#(
parameter BITS = 16,
parameter LENGTH = 10
)
(
input rstn,
input clk,
input in_valid,
input load_a,
input [BITS-1:0] vector_a_in,
input [BITS-1:0] vector_b,
output out_valid,
output logic [BITS-1:0] c
);

logic [BITS-1:0] vector_a[LENGTH];
logic [BITS-1:0] a;

logic in_valid_d = 0;
logic [$clog2(LENGTH):0] count = 0;

always @(posedge clk)
    if (in_valid == 1)
        if (count < LENGTH-1)
            count <= count + 1;
        else
            count <= 0;
    else
        count <= count;


always @(posedge clk)
    if (load_a)
        begin
            for (int i = 1; i < LENGTH; i++)
                vector_a[i] <= vector_a[(i-1)];
            vector_a[0] <= vector_a_in;
        end
    else
        vector_a <= vector_a;

always_comb
    a = vector_a[count];

half_add
half_add1
(
.rstn,
.clk,
.in_valid,
.a(a),
.b(vector_b),
.out_valid,
.c
);

endmodule
