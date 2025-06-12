package testbench_functions_pkg;

import file_pkg::*;
import conversions_pkg::*;

parameter LAYER1_NEURONS = 784;
parameter LAYER2_NEURONS = 50;
parameter OUTPUT_NODES = 10;

logic DEBUG = 0;

task LoadW1(input string FileName, output logic [15:0] W1[LAYER1_NEURONS][LAYER2_NEURONS]);
  real w1_data_set[];
  integer offset;
  integer i;
  integer j;
  integer offset2;
  integer count;
  reg [63:0] data_bits;
  real data;
  begin
    if (DEBUG) $display("W1");
    offset = 4916;
    for (i = 0; i < 784; i = i + 1)
      begin
        count = 0;
        ReadDoubles(FileName, offset, 50, w1_data_set);
        //@(posedge clk); // Perhaps this is being interrupted?
        if (DEBUG) $display("W1 %d", i);
        offset2 = 0;
        for (j = 0; j < 50; j = j + 1)
          begin
            W1[i][j] = DoubleToHalf(w1_data_set[j]);
            //$write("%f ", data);
            //if (i == 783)
              if (count < 10)
                begin
                  if (DEBUG) $write("%e ", w1_data_set[j]);
                  count = count + 1;
                  if (DEBUG) $write("%e ", DoubleFromHalf(W1[i][j]));
                end
            offset = offset + 8;
            offset2 = offset2 + 8;
          end
        offset = offset + 10;
      end
    $display("");
  end
endtask

task Loadb1(input string FileName, output logic [15:0] b1[LAYER2_NEURONS]);
  real b1_data_set[];
  integer offset;
  integer i;
  reg [63:0] data_bits;
  real data;
  begin
    offset = 4416;
    ReadDoubles(FileName, offset, 50, b1_data_set);
    for (i = 0; i < 50; i = i + 1)
      begin
        b1[i] = DoubleToHalf(b1_data_set[i]);
        offset = offset + 8;
      end
  end
endtask

task LoadW2(input string FileName, output logic [15:0] W2[LAYER2_NEURONS][OUTPUT_NODES]);
  real w2_data_set[];
  integer offset;
  integer i;
  integer j;
  reg [63:0] data_bits;
  real data;
  begin
    offset = 326356;
    for (i = 0; i < 50; i = i + 1)
      begin
        ReadDoubles(FileName, offset, 10, w2_data_set);
        for (j = 0; j < 10; j = j + 1)
          begin
            W2[i][j] = DoubleToHalf(w2_data_set[j]);
            offset = offset + 8;
          end
        offset = offset + 10;
      end
  end
endtask

task Loadb2(input string FileName, output logic [15:0] b2[OUTPUT_NODES]);
  real b2_data_set[];
  integer offset;
  integer i;
  reg [63:0] data_bits;
  real data;
  begin
    offset = 4826;
    ReadDoubles(FileName, offset, 10, b2_data_set);
    for (i = 0; i < 10; i = i + 1)
      begin
        b2[i] = DoubleToHalf(b2_data_set[i]);
        offset = offset + 8;
      end
  end
endtask

endpackage
