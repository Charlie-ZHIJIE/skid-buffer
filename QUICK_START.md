# 🚀 Quick Start - Create a New Verilog Problem

## 5-Minute Setup

### 1️⃣ Copy and edit (2 minutes)

```bash
# Duplicate the template
cd /home/charlie/Desktop/GitHub
cp -r verilog-problem-template my-new-problem
cd my-new-problem

# Update these files:
# - sources/your_module.sv        -> interface + TODO placeholder
# - tests/test_your_module.py     -> hidden cocotb tests
# - docs/Specification.md         -> formal spec
# - prompt.txt                    -> agent instructions
```

### 2️⃣ Create Git branches (1 minute)

```bash
git init
git add .
git commit -m "baseline"

# Required branches
git branch my_problem_baseline          # TODO baseline
git checkout -b my_problem_test         # add tests
git add tests/ && git commit -m "tests"
git checkout -b my_problem_golden       # full RTL
# implement sources/, then:
git add sources/ && git commit -m "golden"
```

### 3️⃣ Register the problem (1 minute)

Add this snippet to `verilog-coding-template/src/hud_controller/problems/basic.py`:

```python
PROBLEM_REGISTRY.append(
    ProblemSpec(
        id="my_problem",
        description="""⚠️ Use str_replace_based_edit_tool ONLY. NO bash heredoc! ⚠️
[Your description...]
""",
        difficulty="easy",
        base="my_problem_baseline",
        test="my_problem_test",
        golden="my_problem_golden",
        test_files=["tests/test_my_problem.py"],
    )
)
```

### 4️⃣ Build & validate (1 minute)

```bash
cd /home/charlie/Desktop/GitHub/verilog-coding-template

# bump Dockerfile cache buster
sed -i 's/random=random[0-9]*/random=random'$(date +%s)'/' Dockerfile

# build, validate, JSON
uv run utils/imagectl3.py verilog_ -bvj --ids my_problem
```

## ✅ Done!

Once you see "All validation steps passed," run the agent evaluation:

```bash
export ANTHROPIC_API_KEY="..."
uv run hud eval local-hud-my-problem.json claude \
  --model claude-sonnet-4-5-20250929 \
  --max-steps 15 \
  --group-size 1 \
  --yes
```

## 📋 Key reminders

1. ✅ Add `` `timescale 1ns/1ps `` to every Verilog file
2. ✅ Call `await Timer(1, units="ns")` before checking DUT outputs
3. ✅ Tool name must be `str_replace_based_edit_tool` (not `str_replace_editor`)
4. ✅ Branch naming: `{problem}_baseline`, `{problem}_test`, `{problem}_golden`
5. ✅ Document signal priorities (e.g., load > rst > ena) when relevant

See `SETUP_GUIDE.md` for the full walkthrough. 📖
