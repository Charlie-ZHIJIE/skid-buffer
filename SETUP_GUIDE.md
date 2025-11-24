# 📋 New Verilog Problem Setup Guide

This guide walks through every step required to turn the template into a brand-new problem.

## 🎯 Step 1: Copy the template and edit content

### 1.1 Copy the template

```bash
cd /home/charlie/Desktop/GitHub
cp -r verilog-problem-template my-new-problem
cd my-new-problem
```

### 1.2 Update the Verilog sources

Edit `sources/your_module.sv`:
- Rename the module
- Define the full interface (inputs/outputs)
- Baseline branch: leave TODO comments, no logic
- Golden branch: provide the full implementation

**Important:** prepend `` `timescale 1ns/1ps `` at the top of every `.sv` file.

### 1.3 Write tests

Edit `tests/test_your_module_hidden.py`:
- Decorate each coroutine with `@cocotb.test()`
- Insert `await Timer(1, units="ns")` before checking outputs
- Provide a pytest wrapper
- Update module and path names

**Sample skeleton:**
```python
@cocotb.test()
async def test_something(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # initialization
    await RisingEdge(dut.clk)
    
    # stimulus
    dut.input_signal.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")  # critical!
    assert dut.output_signal.value == expected
```

### 1.4 Draft the specification

In `docs/Specification.md`, document:
- Module name
- Interface definition (purpose of each port)
- Behavioral requirements and timing rules
- Optional timing diagram or example timeline

### 1.5 Update supporting files

- `prompt.txt`: short task description for the agent
- `README.md`: problem overview
- `pyproject.toml`: project/package metadata

## 🌿 Step 2: Git repo and branches

### 2.1 Initialize Git (for new repos)

```bash
cd /home/charlie/Desktop/GitHub/my-new-problem
git init
git add .
git commit -m "Initial commit: baseline implementation"
```

### 2.2 Create branches

Assuming the problem is called `my_problem`:

```bash
# baseline branch (TODO version)
git branch my_problem_baseline
git push -u origin my_problem_baseline

# test branch
git checkout -b my_problem_test
git add tests/
git commit -m "Add tests"
git push -u origin my_problem_test

# golden branch
git checkout my_problem_baseline
git checkout -b my_problem_golden
# implement sources/your_module.sv
git add sources/
git commit -m "Add golden solution"
git push -u origin my_problem_golden

# back to main branch
git checkout main  # or my_problem
```

**Branch naming recap**
- `{problem_name}_baseline`: TODO starting point
- `{problem_name}_test`: cocotb tests
- `{problem_name}_golden`: final reference

## 📝 Step 3: Register inside the framework

### 3.1 Update the registry

Edit `/home/charlie/Desktop/GitHub/verilog-coding-template/src/hud_controller/problems/basic.py`:

```python
PROBLEM_REGISTRY.append(
    ProblemSpec(
        id="my_problem",
        description="""⚠️ CRITICAL: Use str_replace_based_edit_tool ONLY for file editing. NO bash heredoc! ⚠️

Bash heredoc (cat >, echo >, tee) will TIMEOUT (5 minutes) and waste your limited steps!

Task: Implement [your module description] in sources/your_module.sv

Interface:
- [port1]: [description]
- [port2]: [description]
...

Requirements:
[Your requirements here]

Implementation Steps:
1. Read sources/your_module.sv using: bash(command="cat /home/ubuntu/example-verilog-codebase/sources/your_module.sv")
2. Edit using: str_replace_based_edit_tool(command="str_replace", path="/home/ubuntu/example-verilog-codebase/sources/your_module.sv", old_str="...", new_str="...")
3. Tests run automatically after you submit - do NOT create testbenches

⚠️ FINAL WARNING: Use str_replace_based_edit_tool for file editing. Bash heredoc = TIMEOUT = FAIL ⚠️

See docs/Specification.md for complete details.
""",
        difficulty="easy",  # or "medium", "hard"
        base="my_problem_baseline",
        test="my_problem_test",
        golden="my_problem_golden",
        test_files=["tests/test_your_module_hidden.py"],
    )
)
```

### 3.2 Bump the Dockerfile cache buster

Edit `/home/charlie/Desktop/GitHub/verilog-coding-template/Dockerfile`:

```dockerfile
ENV random=random8   # old value
```

Change to:
```dockerfile
ENV random=random9
```

This forces Docker to rebuild the image.

### 3.3 Local repo path (optional)

If you rely on a local checkout rather than GitHub, ensure the Dockerfile includes:

```dockerfile
COPY --chown=ubuntu:ubuntu local-repos/problems /home/ubuntu/example-verilog-codebase
```

Then copy your repo:
```bash
mkdir -p /home/charlie/Desktop/GitHub/verilog-coding-template/local-repos
cp -r my-new-problem /home/charlie/Desktop/GitHub/verilog-coding-template/local-repos/problems
```

## 🐳 Step 4: Build and validate the Docker image

### 4.1 Build

```bash
cd /home/charlie/Desktop/GitHub/verilog-coding-template
uv run utils/imagectl3.py verilog_ -b --ids my_problem
```

### 4.2 Validate

```bash
uv run utils/imagectl3.py verilog_ -v --ids my_problem
```

Expect all six checks to pass:
- ✓ Baseline compiles
- ✓ Test patch applies
- ✓ Test patch fails (baseline empty)
- ✓ Golden patch applies
- ✓ Golden patch compiles
- ✓ Golden patch passes tests

### 4.3 Generate JSON

```bash
uv run utils/imagectl3.py verilog_ -j --ids my_problem
```

This creates `local-hud-my-problem.json`.

## 🤖 Step 5: Run the agent evaluation

### 5.1 Execute the eval

```bash
cd /home/charlie/Desktop/GitHub/verilog-coding-template
export ANTHROPIC_API_KEY="your-api-key"
uv run hud eval local-hud-my-problem.json claude \
  --model claude-sonnet-4-5-20250929 \
  --max-steps 15 \
  --group-size 1 \
  --yes
```

### 5.2 Review the results

Look for:
- ✅ No timeouts
- ✅ Agent used `str_replace_based_edit_tool`
- ✅ Tests passed
- ✅ Score = 1.0 (100%)

## ⚠️ Troubleshooting

### Issue 1: `ValueError: Bad period`
Add `` `timescale 1ns/1ps `` to the top of your `.sv` file.

### Issue 2: Assertions read `XXXXXXXX`
Insert `await Timer(1, units="ns")` after the relevant `RisingEdge`.

### Issue 3: "Golden patch fails tests"
Verify the golden implementation, test expectations, and timing behavior.

### Issue 4: Agent timeout
- Ensure the prompt explicitly mandates `str_replace_based_edit_tool`
- Confirm `local-hud-*.json` lists `"str_replace_based_edit_tool"` inside `allowed_tools`

## 📚 References

- Simple Adder example: `/home/charlie/Desktop/GitHub/verilog-problems/`
- `CONTRACTOR_GUIDE.md`: `/home/charlie/Desktop/pLab test/CONTRACTOR_GUIDE.md`
- Timeout playbook: `/home/charlie/Desktop/GitHub/TIMEOUT_SOLUTIONS.md`

## ✅ Final checklist

Before submission, confirm:

- [ ] Verilog files include the `timescale` directive
- [ ] Baseline uses TODO placeholders
- [ ] Golden has the working RTL
- [ ] Tests include the `Timer` delay
- [ ] All Git branches exist and are pushed
- [ ] `basic.py` contains the ProblemSpec entry
- [ ] Dockerfile `random` value bumped
- [ ] Docker builds without errors
- [ ] All six validation checks succeed
- [ ] Agent evaluation passes with zero timeouts

Good luck! 🚀
