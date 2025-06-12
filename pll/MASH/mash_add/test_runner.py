# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def test_mash_add():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent

    sources = [proj_path / "mash_add.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="mash_add",
        build_args=["--timing"]
    )

    runner.test(hdl_toplevel="mash_add", test_module="test_mash_add,")


if __name__ == "__main__":
    test_mash_add()
