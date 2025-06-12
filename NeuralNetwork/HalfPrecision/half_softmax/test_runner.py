# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def half_softmax():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent
    top_path = proj_path.parent.parent.parent

    files_path = top_path / "NeuralNetwork/HalfPrecision/Files/"
    faster_files_path = top_path / "NeuralNetwork/HalfPrecision/FasterFiles/"

    sources = [ files_path / "delay.sv",
                files_path / "delay_v.sv",
                files_path / "leading_zero_count.sv",
                files_path / "integer_divide.sv",
                files_path / "half_add.sv",
                files_path / "half_add_v_h.sv",
                files_path / "half_add_v_v.sv",
                files_path / "half_fm_exp2.sv",
                files_path / "half_integer_part.sv",
                files_path / "half_two_int_power.sv",
                files_path / "half_exp.sv",
                files_path / "half_exp_v.sv",
                files_path / "half_sum_v.sv",
                files_path / "half_divide_v_h.sv",
                files_path / "half_max.sv",
                files_path / "half_max_v.sv",
                files_path / "half_multiply.sv",
                files_path / "half_pade_approximation_exp.sv",
                files_path / "half_divide.sv",
                files_path / "half_softmax_v.sv"
                ]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="half_softmax_v"
    )

    runner.test(hdl_toplevel="half_softmax_v", test_module="half_softmax_test,")


if __name__ == "__main__":
    half_softmax()
