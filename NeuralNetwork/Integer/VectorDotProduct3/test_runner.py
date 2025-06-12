# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def integer_vector_dot_vector():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent

    sources = [proj_path / "stream_multiply_accumulate.sv",
               proj_path / "stream_accumulate.sv",
               proj_path / "integer_vector_dot_vector.sv"
                ]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="integer_vector_dot_vector",
        build_args=["--timing"]
    )

    runner.test(hdl_toplevel="integer_vector_dot_vector", test_module="integer_vector_dot_vector_test,")


if __name__ == "__main__":
    integer_vector_dot_vector()
