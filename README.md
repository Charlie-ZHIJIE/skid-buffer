# Skid Buffer Problem

A medium-difficulty Verilog RTL design problem featuring a 2-entry skid buffer with AXI-Stream ready/valid handshake protocol.

## Problem: Skid Buffer

Design a two-entry skid buffer that decouples upstream and downstream ready/valid handshakes without losing ordering. This is a critical component used in high-performance streaming interfaces to handle backpressure while maintaining throughput.

## Structure

```
.
├── sources/
│   ├── skid_buffer.sv                 # Baseline (TODO) implementation
│   └── skid_buffer_GOLDEN_EXAMPLE.sv  # Golden placeholder
├── tests/
│   └── test_skid_buffer_hidden.py     # cocotb test suite
├── docs/
│   └── Specification.md               # Detailed specification
├── prompt.txt                         # Agent task description
├── README.md                          # This file
└── pyproject.toml                     # Python dependencies
```

## Git Branches

- `skid_buffer` or `main`: Development branch
- `skid_buffer_baseline`: Agent starting point (with TODO)
- `skid_buffer_test`: Test branch (includes tests)
- `skid_buffer_golden`: Reference solution (complete implementation)

## AI Agent Evaluation Results

This problem has been extensively evaluated using Claude Sonnet 4.5 on the HUD.AI platform.

### Evaluation Summary

| Configuration | Success Rate | Sample Size | Key Findings |
|--------------|--------------|-------------|--------------|
| **Without Hints** | 60% | 10 episodes | Agents struggle with simultaneous enqueue+dequeue edge case |
| **With Hints** | 70-80% | 20 episodes | Explicit guidance on case 2'b11 significantly improves success |
| **Golden Solution** | 100% | All tests | Reference implementation passes all 4 test suites |

### Critical Edge Case: Simultaneous Enqueue + Dequeue

The most challenging aspect of this problem is handling the case where:
- Buffer is full (both entries occupied)
- Downstream is ready to consume (dequeue)
- Upstream has new data (enqueue)

**Challenge**: Maintaining strict FIFO ordering while processing both operations in a single cycle.

**Solution**: The golden implementation uses an explicit case statement to handle all four combinations of `{will_dequeue, will_enqueue}`, ensuring old buffered data exits before new data.

### Impact of Hints

Adding explicit hints about the simultaneous enqueue+dequeue case improved agent success rate by **15-20 percentage points**. This demonstrates that:

1. The problem tests fundamental understanding of state machine design
2. Explicit enumeration of edge cases helps agents avoid sequential logic pitfalls
3. Medium-difficulty problems benefit significantly from targeted guidance

### Documentation

For detailed analysis of the hidden grader and golden solution:
- **[GRADER_ANALYSIS.md](GRADER_ANALYSIS.md)** - Comprehensive mapping of test requirements to implementation
- **[TEST_RESULTS_SUCCESS.md](TEST_RESULTS_SUCCESS.md)** - Full local verification results
- **[docs/Specification.md](docs/Specification.md)** - Complete behavioral specification

## Usage

1. Copy this repository when creating new handshake problems
2. Modify the Verilog module name and functionality as needed
3. Update tests/spec/prompt to match new requirements
4. Create Git branches following the naming convention above
5. Register the problem in `verilog-coding-template`

## Test Suite

The hidden grader (`tests/test_skid_buffer_hidden.py`) includes:

1. **Reset Testing** - Validates asynchronous reset behavior
2. **Throughput Testing** - Verifies maximum data transfer rate
3. **Backpressure Testing** - Ensures FIFO ordering under intermittent backpressure
4. **Stress Testing** - Random handshake patterns including critical edge cases

All tests use cocotb (Python-based HDL verification) with Icarus Verilog simulator.

## Quick Start

### Local Testing

```bash
# Install dependencies
uv pip install -e .

# Run golden solution tests
uv run pytest tests/test_skid_buffer_hidden.py -v
```

### Expected Output

```
test_reset_flush PASSED
test_full_throughput_stream PASSED
test_alternating_backpressure_preserves_order PASSED
test_random_handshake_stress PASSED
```

