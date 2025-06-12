/* verilator lint_off WIDTHTRUNC */

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

function [15:0] RealToHalf;
  input real  a_real;
  reg [31:0] a_single;
  reg [4:0] a_exp;
  begin
    a_single = $realtobits(a_real);
    if (a_single[30:23] < (127 - 15))
      RealToHalf = 16'b0;
    else
      begin
        if (a_single[30:23] > (127 + 16))
          RealToHalf = {a_single[31],15'b111_1111_1111_1111};
        else
          begin
            a_exp = a_single[30:23] - 127 + 15;
            RealToHalf = (a_single==0) ? 0 : {a_single[31],a_exp,a_single[22:13]};
          end
      end
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
