# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def test_first_order():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent
    #proj_path = "/home/jamie/git/j1s1e1/VerilogPolarCodes/test_bench/"

    sources = [proj_path / "stage.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="stage",
        build_args=["--timing"]
    )

    runner.test(hdl_toplevel="stage", test_module="test_first_order,")


if __name__ == "__main__":
    test_first_order()
