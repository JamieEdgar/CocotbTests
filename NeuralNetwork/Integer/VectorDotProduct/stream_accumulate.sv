module stream_accumulate
#(
parameter BITS = 8,
parameter LENGTH = 10
)
(
input   clk,
input in_valid,
input [BITS-1:0] a,
output logic out_valid,
output logic [BITS-1:0] c
);

logic in_valid_d;
logic [BITS-1:0] sum = 0;

always @(posedge clk)
    if (in_valid == 0 && in_valid_d == 1)
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
    in_valid_d <= in_valid;

always @(posedge clk)
    if (in_valid)
        sum <= sum + a;
    else
        sum <= 0;


endmodule
