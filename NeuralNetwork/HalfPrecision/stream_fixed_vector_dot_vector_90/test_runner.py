# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def half_fixed_vector_dot_vector():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent
    top_path = proj_path.parent.parent.parent

    files_path = top_path / "NeuralNetwork/HalfPrecision/Files/"
    faster_files_path = top_path / "NeuralNetwork/HalfPrecision/FasterFiles/"

    sources = [ files_path / "leading_zero_count.sv",
                files_path / "half_add.sv",
                files_path / "half_multiply.sv",
                faster_files_path / "half_stream_accumulate.sv",
                faster_files_path / "half_stream_multiply_accumulate.sv",
                faster_files_path / "half_vector_dot_vector.sv",
                faster_files_path / "half_fixed_vector_dot_vector.sv"
                ]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="half_fixed_vector_dot_vector",
        parameters={"LENGTH" :  90,
                    "MULTS" : 2}
    )

    runner.test(hdl_toplevel="half_fixed_vector_dot_vector", test_module="half_fixed_vector_dot_vector_test,")


if __name__ == "__main__":
    half_fixed_vector_dot_vector()
