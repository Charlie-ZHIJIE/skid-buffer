# ✅ New Verilog Problem Checklist

Review every item before submitting or testing your new problem.

## 📁 Files and Directory Layout

- [ ] `sources/your_module.sv` exists
- [ ] `tests/test_your_module_hidden.py` exists
- [ ] `docs/Specification.md` exists
- [ ] `prompt.txt` exists
- [ ] `README.md` exists
- [ ] `pyproject.toml` exists

## 🔧 Verilog Sources

- [ ] Each file starts with `` `timescale 1ns/1ps ``
- [ ] Module name is correct
- [ ] Interface definition lists every input/output port
- [ ] **Baseline branch**: implementation replaced with TODO comments
- [ ] **Golden branch**: full working implementation
- [ ] Code compiles cleanly

## 🧪 Test Files

- [ ] Proper imports (cocotb, Clock, RisingEdge, Timer)
- [ ] Every test coroutine is decorated with `@cocotb.test()`
- [ ] `await Timer(1, units="ns")` inserted before assertions
- [ ] Pytest wrapper `test_*_runner()` present
- [ ] Wrapper points to the correct source path/module name
- [ ] Tests cover the main behavioral requirements

## 📄 Docs & Config

- [ ] `Specification.md` is complete:
  - [ ] Interface description
  - [ ] Functional requirements
  - [ ] Timing constraints
  - [ ] Example or diagram (optional)
- [ ] `prompt.txt` summarizes the task clearly
- [ ] `README.md` reflects the current problem
- [ ] `pyproject.toml` has the updated project name

## 🌿 Git Branches

- [ ] `{problem_name}_baseline` created
- [ ] `{problem_name}_test` created
- [ ] `{problem_name}_golden` created
- [ ] Baseline branch only contains TODO implementation
- [ ] Test branch adds/updates tests
- [ ] Golden branch carries the final RTL
- [ ] All branches pushed to the remote (if applicable)

## 📝 Framework Registration

- [ ] Added a `ProblemSpec` entry in `verilog-coding-template/src/hud_controller/problems/basic.py`
- [ ] Problem ID is unique and correct
- [ ] Description warns "⚠️ Use str_replace_based_edit_tool ONLY"
- [ ] Tool usage instructions are included
- [ ] Branch names (base/test/golden) match reality
- [ ] `test_files` paths are accurate
- [ ] `difficulty` reflects the task (easy/medium/hard)

## 🐳 Docker Setup

- [ ] `ENV random=` cache-buster incremented in `Dockerfile`
- [ ] Local repo copied into `local-repos/problems/` if using local sources

## 🔨 Build & Validation

- [ ] Docker image builds successfully
  ```bash
  uv run utils/imagectl3.py verilog_ -b --ids your_problem
  ```
- [ ] All six validation checks pass
  ```bash
  uv run utils/imagectl3.py verilog_ -v --ids your_problem
  ```
  - [ ] ✓ Baseline compiles
  - [ ] ✓ Test patch applies
  - [ ] ✓ Test patch fails (baseline empty)
  - [ ] ✓ Golden patch applies
  - [ ] ✓ Golden patch compiles
  - [ ] ✓ Golden patch passes tests
- [ ] JSON config generated
  ```bash
  uv run utils/imagectl3.py verilog_ -j --ids your_problem
  ```

## 🤖 Agent Evaluation

- [ ] Agent eval command ran successfully
  ```bash
  uv run hud eval local-hud-your-problem.json claude --model ... --max-steps 15 --yes
  ```
- [ ] Agent bootstraps with `str_replace_based_edit_tool`
- [ ] Agent edits files using `str_replace_based_edit_tool`
- [ ] No 300-second timeout errors
- [ ] Tests pass
- [ ] Score is 1.0 (100%)

## ⚠️ Common Pitfalls

- [ ] Tool name is `str_replace_based_edit_tool`, not `str_replace_editor`
- [ ] `timescale` directive present
- [ ] `Timer` delay included before checking DUT outputs
- [ ] Branch names use underscores `_`, not dashes `-`
- [ ] Test filename ends with `_hidden`
- [ ] Golden design truly passes all tests

## 📊 Expected Agent Performance

| Difficulty | Steps | Time |
|------------|-------|------|
| Easy       | 5-10  | 30-60 s |
| Medium     | 15-25 | 1-3 min |
| Hard       | 30-50 | 3-8 min |

If the agent needs more steps or time, consider simplifying the spec, clarifying the interface, or trimming requirements.

## ✨ Final Confirmation

- [ ] I completed every checklist item above
- [ ] I ran at least one successful agent evaluation
- [ ] Difficulty matches the target audience
- [ ] Documentation is clear
- [ ] Ready for production use

---

**If everything is checked ✅, congrats - your new Verilog problem is ready!** 🎉

