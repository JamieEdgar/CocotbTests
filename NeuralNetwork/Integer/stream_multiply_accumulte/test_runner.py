# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def stream_multiply_accumulate():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent

    sources = [proj_path / "stream_multiply_accumulate.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="stream_multiply_accumulate",
        build_args=["--timing"]
    )

    runner.test(hdl_toplevel="stream_multiply_accumulate", test_module="test_stream_multiply_accumulate,")


if __name__ == "__main__":
    stream_multiply_accumulate()
