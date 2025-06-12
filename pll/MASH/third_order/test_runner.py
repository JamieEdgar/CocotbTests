# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def test_third_order():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent

    sources = [proj_path / "stage.sv",
               proj_path / "second_order.sv",
               proj_path / "third_order.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="third_order",
        build_args=["--timing"]
    )

    runner.test(hdl_toplevel="third_order", test_module="test_third_order,")


if __name__ == "__main__":
    test_third_order()
