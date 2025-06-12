# test_runner.py

import os
from pathlib import Path

from cocotb.runner import get_runner


def read_W1():
    sim = os.getenv("SIM", "verilator")

    proj_path = Path(__file__).resolve().parent
    top_path = proj_path.parent.parent.parent
    pkg_path = top_path / "Packages/"
    nn_pkg_pat = top_path / "NeuralNetwork/NN_Packages/"

    sources = [pkg_path / "file_pkg.sv",
               nn_pkg_pat / "conversions_pkg.sv",
               nn_pkg_pat / "testbench_functions_pkg.sv",
               proj_path / "read_Image_tb.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="read_Image_tb",
        build_args=["--timing"]
    )

    runner.test(hdl_toplevel="read_Image_tb", test_module="read_Image")


if __name__ == "__main__":
    read_W1()
