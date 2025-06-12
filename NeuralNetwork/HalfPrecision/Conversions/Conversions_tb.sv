`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 12/01/2018 04:52:42 PM
// Design Name: 
// Module Name: half_predict_layer1_tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////

/* verilator lint_off WIDTHTRUNC */
/* verilator lint_off REALCVT */
/* verilator lint_off WIDTHEXPAND */

module Conversions_tb(
);

function [31:0] SingleFromHalf;
  input [15:0] half;
  reg sign;
  reg [7:0] exponent;
  reg [22:0] mantissa;
  begin
    sign = half[15];
    exponent = 8'd127 + {3'b0,half[14:10]} - 8'd15;
    mantissa = {half[9:0],13'b0};
    SingleFromHalf = (half[14:0] == 0) ?
                        32'b0 :
                        {sign,exponent,mantissa};
  end
endfunction

function real DoubleFromHalf;
  input [15:0] half;
  reg sign;
  reg [10:0] exponent;
  reg [51:0] mantissa;
  logic [63:0] double_bits;
  begin
    sign = half[15];
    exponent = 11'd1023 + {6'b0,half[14:10]} - 11'd15;
    mantissa = {half[9:0],42'b0};
    double_bits = (half[14:0] == 0) ?
                        64'b0 :
                        {sign,exponent,mantissa};
    DoubleFromHalf = $bitstoreal(double_bits);
  end
endfunction

//       1         11            52
// sign 63  exp 62-52 mantissa 51-0
// 01111111 = 127  01111111111 = 1023

function [15:0] DoubleToHalf;
  input real  a_real;
  reg [63:0] a_double;
  reg [4:0] a_exp;
  begin
    a_double = $realtobits(a_real);
    $display("Double Exp = %b %d", a_double[62:52], a_double[62:52]);
    if (a_double[62:52] < (11'd1023 - 15))
      DoubleToHalf = 16'b0;
    else
      begin
        if (a_double[62:52] > (1023 + 16))
          DoubleToHalf = {a_double[63],15'b111_1111_1111_1111};
        else
          begin
            a_exp = a_double[62:52] - 1023 + 15;
            DoubleToHalf = (a_double==0) ? 0 : {a_double[63],a_exp,a_double[51:42]};
          end
      end
  end
endfunction


reg rstn;
reg clk;

task Test();
  real data1;
  logic [15:0] half;
  real data2;
  for (int i = 1; i < 10; i ++)
    begin
      @(posedge clk);
      data1 = 0.1 * $itor(i);
      half = DoubleToHalf(data1);
      data2 = DoubleFromHalf(half);
      $display("%64b %b %b ", $realtobits(data1), half, $realtobits(data2));
      $display("%e %e ", data1, data2);
    end
endtask

initial
  begin
    rstn = 1;
    @(posedge clk);
    @(posedge clk);
    rstn = 0;
    repeat (10) @(posedge clk);
    @(posedge clk);
    rstn = 1;
    @(posedge clk);
    @(posedge clk);
    Test();
    @(posedge clk);
    repeat (100) @(posedge clk);
    //$stop;
  end

initial
  begin
    clk = 0;
    forever #10 clk = ~clk;
  end

endmodule
