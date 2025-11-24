"""临时测试脚本 - 用于测试golden实现"""
import os
from pathlib import Path
from cocotb_tools.runner import get_runner

sim = os.getenv("SIM", "icarus")
proj_path = Path(__file__).resolve().parent

# 使用skid buffer的 golden 示例版本
sources = [proj_path / "sources/skid_buffer_GOLDEN_EXAMPLE.sv"]
runner = get_runner(sim)

print("=== Building with golden implementation ===")
runner.build(
    sources=sources,
    hdl_toplevel="skid_buffer",
    always=True,
    build_dir="sim_build_test"
)

print("=== Running tests ===")
runner.test(
    hdl_toplevel="skid_buffer",
    test_module="tests.test_skid_buffer_hidden",
    build_dir="sim_build_test"
)

