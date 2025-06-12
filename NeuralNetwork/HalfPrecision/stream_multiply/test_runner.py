# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def half_stream_multiply():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent
    top_path = proj_path.parent.parent.parent

    files_path = top_path / "NeuralNetwork/HalfPrecision/Files/"

    sources = [ files_path / "leading_zero_count.sv",
                files_path / "half_multiply.sv",
                proj_path / "half_stream_multiply.sv"
                ]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="half_stream_multiply",
        build_args=["--timing"]
    )

    runner.test(hdl_toplevel="half_stream_multiply", test_module="half_stream_multiply_test,")


if __name__ == "__main__":
    half_stream_multiply()
