# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def top_test():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent

    sources = [proj_path / "mux.sv",
               proj_path / "program_counter.sv",
               proj_path / "alu.sv",
               proj_path / "unregistered_memory.sv",
               proj_path / "registers.sv",
               proj_path / "top.sv"
                ]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="top"
    )

    runner.test(hdl_toplevel="top", test_module="top_test,")


if __name__ == "__main__":
    top_test()
