# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner

def test_predict():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent
    top_path = proj_path.parent.parent.parent

    pkg_path = top_path / "Packages/"
    nn_pkg_pat = top_path / "NeuralNetwork/NN_Packages/"
    files_path = top_path / "NeuralNetwork/HalfPrecision/Files/"

    sources = [pkg_path / "file_pkg.sv",
               nn_pkg_pat / "conversions_pkg.sv",
               nn_pkg_pat / "testbench_functions_pkg.sv",
               files_path / "half_add_v_v.sv",
               files_path / "half_transpose.sv",
               files_path / "half_multiply_accumulate.sv",
               files_path / "half_dot_v_v.sv",
               files_path / "half_dot_v_m.sv",
               files_path / "integer_divide.sv",
               files_path / "half_divide.sv",
               files_path / "delay.sv",
               files_path / "half_pade_approximation_exp.sv",
               files_path / "half_two_int_power.sv",
               files_path / "half_integer_part.sv",
               files_path / "leading_zero_count.sv",
               files_path / "half_add.sv",
               files_path / "half_fm_exp2.sv",
               files_path / "half_multiply.sv",
               files_path / "half_divide_v_h.sv",
               files_path / "half_exp.sv",
               files_path / "half_sigmoid.sv",
               files_path / "half_sigmoid_v.sv",
               files_path / "half_predict_layer1.sv",
               files_path / "half_softmax_v.sv",
               files_path / "delay_v.sv",
               files_path / "half_exp_v.sv",
               files_path / "half_sum_v.sv",
               files_path / "half_max.sv",
               files_path / "half_max_v.sv",
               files_path / "half_add_v_h.sv",
               files_path / "half_predict_layer2.sv",
               files_path / "half_predict.sv",
               files_path / "half_predict_loader.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="half_predict_loader",
        build_args=["--timing"]
    )

    runner.test(hdl_toplevel="half_predict_loader", test_module="test_predict")


if __name__ == "__main__":
    test_predict()
