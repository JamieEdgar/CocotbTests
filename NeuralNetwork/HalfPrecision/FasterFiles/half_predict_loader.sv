module half_predict_loader
#(
parameter LAYER1_NEURONS = 784,
parameter LAYER2_NEURONS = 50,
parameter OUTPUT_NODES = 10
)
(
input rstn,
input clk,
input start,
input load_x,
input load_W1,
input load_b1,
input load_W2,
input load_b2,
input [15:0] neuron_data_in,
output done,
output [15:0] y[OUTPUT_NODES]
);

logic [15:0] x_temp[LAYER1_NEURONS];
logic [15:0] x[LAYER1_NEURONS];
logic [15:0] W1[LAYER1_NEURONS][LAYER2_NEURONS];
logic [15:0] b1[LAYER2_NEURONS];
logic [15:0] W2[LAYER2_NEURONS][OUTPUT_NODES];
logic [15:0] b2[OUTPUT_NODES];

always @(posedge clk)
  if (load_x)
    begin
      for (int i = 1; i < LAYER1_NEURONS; i++)
          x_temp[i] <=x_temp[i-1];
      x_temp[0] <= neuron_data_in;
    end
  else
    x_temp <= x_temp;

always @(posedge clk)
  if (start)
    x <= x_temp;
  else
    x <= x;

always @(posedge clk)
  if (load_W1)
    begin
      for (int i = 0; i < LAYER1_NEURONS; i++)
        begin
          if (i != 0)
            W1[i][0] <= W1[i-1][LAYER2_NEURONS-1];
          for (int j = 1; j < LAYER2_NEURONS; j++)
            W1[i][j] <= W1[i][j-1];
        end
      W1[0][0] <= neuron_data_in;
    end
  else
    W1 <= W1;

always @(posedge clk)
  if (load_b1)
    begin
      for (int i = 1; i < LAYER2_NEURONS; i++)
          b1[i] <= b1[i-1];
      b1[0] <= neuron_data_in;
    end
  else
    b1 <= b1;

always @(posedge clk)
  if (load_W2)
    begin
      for (int i = 0; i < LAYER2_NEURONS; i++)
        begin
          if (i != 0)
            W2[i][0] <= W2[i-1][OUTPUT_NODES-1];
          for (int j = 1; j < OUTPUT_NODES; j++)
            W2[i][j] <= W2[i][j-1];
        end
      W2[0][0] <= neuron_data_in;
    end
  else
    W2 <= W2;

always @(posedge clk)
  if (load_b2)
    begin
      for (int i = 1; i < OUTPUT_NODES; i++)
          b2[i] <= b2[i-1];
      b2[0] <= neuron_data_in;
    end
  else
    b2 <= b2;

half_predict
#(
.LAYER1_NEURONS(LAYER1_NEURONS),
.LAYER2_NEURONS(LAYER2_NEURONS),
.OUTPUT_NODES(OUTPUT_NODES)
)
half_predict1
(
.rstn,
.clk,
.start,
.x,
.W1,
.b1,
.W2,
.b2,
.done,
.y
);

endmodule
