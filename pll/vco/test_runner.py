# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def test_vco():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent

    sources = [proj_path / "vco.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="vco",
        build_args=["--timing"]
    )

    runner.test(hdl_toplevel="vco", test_module="test_vco,")


if __name__ == "__main__":
    test_vco()
