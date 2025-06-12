module stream_multiply_accumulate
#(
parameter LENGTH = 10
)
(
input   clk,
input in_valid,
input [7:0] a,
input [7:0] b,
output logic out_valid,
output logic [15:0] c
);

logic in_valid_d;
logic [15:0] mult;
logic [15:0] sum;
logic [7:0] count = 0;
logic first_sum = 0;
logic last_sum = 0;
logic last_sum_d;

always @(posedge clk)
    if (last_sum_d)
        begin
            out_valid <= 1;
            c <= sum;
        end
    else
        begin
            out_valid <= 0;
            c <= 0;
        end

always @(posedge clk)
    if (in_valid)
        if (count == LENGTH-1)
            last_sum <= 1;
        else
            last_sum <= 0;
    else
        last_sum <= 0;

always @(posedge clk)
    last_sum_d <= last_sum;

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
        if (count == 0)
            first_sum <= 1;
        else
            first_sum <= 0;
    else
        first_sum <= 0;

always @(posedge clk)
    in_valid_d <= in_valid;

always @(posedge clk)
    mult <= a * b;

always @(posedge clk)
    if (in_valid_d)
        if (first_sum != 1)
            sum <= sum + mult;
        else
            sum <= mult;
    else
        sum <= 0;


endmodule
