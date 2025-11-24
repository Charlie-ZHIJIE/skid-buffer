"""Temporary test runner for skid_buffer GOLDEN EXAMPLE"""
import os
from pathlib import Path
from cocotb_tools.runner import get_runner

def test_skid_buffer_golden():
    """Test golden implementation"""
    sim = os.getenv("SIM", "icarus")
    proj_path = Path(__file__).resolve().parent

    # Use GOLDEN_EXAMPLE file
    sources = [proj_path / "sources/skid_buffer_GOLDEN_EXAMPLE.sv"]
    
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="skid_buffer",
        always=True,
    )
    runner.test(
        hdl_toplevel="skid_buffer",
        test_module="test_skid_buffer_hidden"
    )

if __name__ == "__main__":
    test_skid_buffer_golden()

