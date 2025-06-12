/* verilator lint_off WIDTHTRUNC */

module half_stream_to_vector
#
(
parameter BITS = 16,
parameter LENGTH = 10
)
(
input rstn,
input clk,
input in_valid,
input [BITS-1:0] x,
output logic out_valid = 0,
output logic [BITS-1:0] y[LENGTH] = '{default : 0}
);

logic [$clog2(LENGTH):0] count = 0;

always @(posedge clk)
    if (in_valid)
        if (count < LENGTH - 1)
            count <= count + 1;
        else
            count <= 0;

always @(posedge clk)
    if (in_valid)
        if (count == LENGTH - 1)
            out_valid <= 1;
        else
            out_valid <= 0;
    else
        out_valid <= 0;

always @(posedge clk)
    if (in_valid)
        begin
            y <= y;
            y[count] <= x;
        end
    else
        y <= '{default : 0};

endmodule
