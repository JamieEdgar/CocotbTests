# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def Conversions():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent

    sources = [proj_path / "Conversions_tb.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="Conversions_tb",
        build_args=["--timing"]
    )

    runner.test(hdl_toplevel="Conversions_tb", test_module="Conversions")


if __name__ == "__main__":
    Conversions()
