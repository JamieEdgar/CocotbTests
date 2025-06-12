# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def test_fourth_order():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent

    sources = [proj_path / "stage.sv",
               proj_path / "second_order.sv",
               proj_path / "third_order.sv",
               proj_path / "fourth_order.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="fourth_order",
        build_args=["--timing"]
    )

    runner.test(hdl_toplevel="fourth_order", test_module="test_fourth_order,")


if __name__ == "__main__":
    test_fourth_order()
