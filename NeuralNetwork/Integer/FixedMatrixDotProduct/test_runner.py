# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def fixed_integer_matrix_dot_vector():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent

    sources = [ proj_path / "integer_add.sv",
                proj_path / "stream_multiply.sv",
                proj_path / "stream_accumulate.sv",
                proj_path / "stream_multiply_accumulate.sv",
                proj_path / "integer_vector_dot_vector.sv",
                proj_path / "fixed_integer_vector_dot_vector.sv",
                proj_path / "fixed_integer_matrix_dot_vector.sv"
                ]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="fixed_integer_matrix_dot_vector"
    )

    runner.test(hdl_toplevel="fixed_integer_matrix_dot_vector", test_module="fixed_integer_matrix_dot_vector_test,")


if __name__ == "__main__":
    fixed_integer_matrix_dot_vector()
