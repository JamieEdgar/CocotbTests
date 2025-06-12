# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def stream_accumulate():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent

    sources = [proj_path / "stream_accumulate.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="stream_accumulate",
        build_args=["--timing"]
    )

    runner.test(hdl_toplevel="stream_accumulate", test_module="test_stream_accumulate,")


if __name__ == "__main__":
    stream_accumulate()
