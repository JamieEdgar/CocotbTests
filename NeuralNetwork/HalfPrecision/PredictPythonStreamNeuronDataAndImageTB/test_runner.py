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
    faster_files_path = top_path / "NeuralNetwork/HalfPrecision/FasterFiles/"

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
               faster_files_path / "half_predict_layer1.sv",
               files_path / "half_softmax_v.sv",
               files_path / "delay_v.sv",
               files_path / "half_exp_v.sv",
               files_path / "half_sum_v.sv",
               files_path / "half_max.sv",
               files_path / "half_max_v.sv",
               files_path / "half_add_v_h.sv",
               faster_files_path / "half_stream_to_vector.sv",
               faster_files_path / "half_fixed_vector_add_vector.sv",
               faster_files_path / "half_stream_accumulate.sv",
               faster_files_path / "half_stream_multiply_accumulate.sv",
               faster_files_path / "half_vector_dot_vector.sv",
               faster_files_path / "half_fixed_vector_dot_vector.sv",
               faster_files_path / "half_fixed_matrix_dot_vector.sv",
               faster_files_path / "half_predict_layer2.sv",
               faster_files_path / "half_predict.sv"
               ]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="half_predict",
        parameters={
                    "LAYER1_MULTS" : 4
                    }
    )

    runner.test(hdl_toplevel="half_predict", test_module="test_predict_stream_neuron_and_image")


if __name__ == "__main__":
    test_predict()
