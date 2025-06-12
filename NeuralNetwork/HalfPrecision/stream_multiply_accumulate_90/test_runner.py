# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def half_stream_multiply_accumulate():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent
    top_path = proj_path.parent.parent.parent

    files_path = top_path / "NeuralNetwork/HalfPrecision/Files/"
    faster_files_path = top_path / "NeuralNetwork/HalfPrecision/FasterFiles/"

    sources = [ files_path / "leading_zero_count.sv",
                files_path / "half_add.sv",
                files_path / "half_multiply.sv",
                faster_files_path / "half_stream_accumulate.sv",
                faster_files_path / "half_stream_multiply_accumulate.sv"
                ]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="half_stream_multiply_accumulate",
        parameters={"LENGTH" :  90}
    )

    runner.test(hdl_toplevel="half_stream_multiply_accumulate", test_module="half_stream_multiply_accumulate_test,")


if __name__ == "__main__":
    half_stream_multiply_accumulate()
