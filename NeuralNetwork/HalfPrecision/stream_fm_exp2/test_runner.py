# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def half_stream_fm_exp2():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent
    top_path = proj_path.parent.parent.parent

    files_path = top_path / "NeuralNetwork/HalfPrecision/Files/"

    sources = [ files_path / "delay.sv",
                files_path / "leading_zero_count.sv",
                files_path / "integer_divide.sv",
                files_path / "half_add.sv",
                files_path / "half_fm_exp2.sv",
                files_path / "half_integer_part.sv",
                files_path / "half_two_int_power.sv",
                files_path / "half_exp.sv",
                files_path / "half_multiply.sv",
                files_path / "half_pade_approximation_exp.sv",
                files_path / "half_divide.sv",
                proj_path / "half_stream_fm_exp2.sv"
                ]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="half_stream_fm_exp2",
        build_args=["--timing"]
    )

    runner.test(hdl_toplevel="half_stream_fm_exp2", test_module="half_stream_fm_exp2_test,")


if __name__ == "__main__":
    half_stream_fm_exp2()
