`timescale 1ns / 1ps

package file_pkg;

`define SEEK_SET 0
`define SEEK_CUR 1
`define SEEK_END 2

task ReadDoubles(input string fileName, input integer offset, input integer length, output real data[]);
  integer r;
  integer offset2;
  integer fileID;
  logic [7:0] bytes[8];
  reg [63:0] data_bits;
  begin
    data = new[length];
    fileID = $fopen(fileName, "rb");
    $fseek(fileID, offset, `SEEK_SET);
    for (int i = 0; i < length; i++)
      begin
        r = $fread(bytes, fileID);
        data_bits = {bytes[7],bytes[6],bytes[5],bytes[4],
                    bytes[3],bytes[2],bytes[1],bytes[0]};
        data[i] = $bitstoreal(data_bits);
        //$write("%f ", data[i]);
      end
    $fclose(fileID);
  end
endtask

endpackage
