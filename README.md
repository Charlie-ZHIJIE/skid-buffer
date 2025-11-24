# Skid Buffer Problem

This repository instantiates the template for a ready/valid skid buffer problem.

## Problem: Skid Buffer

Design a two-entry skid buffer that decouples upstream and downstream ready/valid handshakes without losing ordering.

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

## Usage

1. Copy this repository when creating new handshake problems
2. Modify the Verilog module name and functionality as needed
3. Update tests/spec/prompt to match new requirements
4. Create Git branches following the naming convention above
5. Register the problem in `verilog-coding-template`

