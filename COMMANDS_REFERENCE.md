# 🔧 Common Command Reference

## 📦 Create a new problem

```bash
# 1. copy the template
cd /home/charlie/Desktop/GitHub
cp -r verilog-problem-template my-new-problem
cd my-new-problem

# 2. edit the key files
# - sources/*.sv
# - tests/*.py
# - docs/Specification.md
# - prompt.txt
```

## 🌿 Git workflow

```bash
# initialize repo
git init
git add .
git commit -m "Initial commit: baseline"

# baseline branch
git branch my_problem_baseline

# test branch
git checkout -b my_problem_test
git add tests/
git commit -m "Add tests"

# golden branch
git checkout my_problem_baseline
git checkout -b my_problem_golden
# implement sources/
git add sources/
git commit -m "Add golden solution"

# push (if using GitHub)
git push -u origin my_problem_baseline
git push -u origin my_problem_test
git push -u origin my_problem_golden

# return to main branch
git checkout main  # or my_problem
```

## 🐳 Docker image commands

```bash
cd /home/charlie/Desktop/GitHub/verilog-coding-template

# build only
uv run utils/imagectl3.py verilog_ -b --ids my_problem

# validate only
uv run utils/imagectl3.py verilog_ -v --ids my_problem

# JSON only
uv run utils/imagectl3.py verilog_ -j --ids my_problem

# build + validate
uv run utils/imagectl3.py verilog_ -bv --ids my_problem

# build + validate + JSON (recommended)
uv run utils/imagectl3.py verilog_ -bvj --ids my_problem

# build multiple problems
uv run utils/imagectl3.py verilog_ -bvj --ids problem1 problem2 problem3

# build everything
uv run utils/imagectl3.py verilog_ -bvj
```

## 🤖 Agent evaluation

```bash
cd /home/charlie/Desktop/GitHub/verilog-coding-template

# API key
export ANTHROPIC_API_KEY="your-api-key-here"

# default run
uv run hud eval local-hud-my-problem.json claude \
  --model claude-sonnet-4-5-20250929 \
  --max-steps 15 \
  --group-size 1 \
  --yes

# more steps
uv run hud eval local-hud-my-problem.json claude \
  --model claude-sonnet-4-5-20250929 \
  --max-steps 30 \
  --group-size 1 \
  --yes

# save logs
uv run hud eval local-hud-my-problem.json claude \
  --model claude-sonnet-4-5-20250929 \
  --max-steps 15 \
  --group-size 1 \
  --yes 2>&1 | tee evaluation.log

# run all problems
uv run hud eval local-hud.json claude \
  --model claude-sonnet-4-5-20250929 \
  --max-steps 20 \
  --full \
  --yes
```

## 🧪 Local testing

```bash
cd /home/charlie/Desktop/GitHub/my-new-problem

# run a single test file (requires iverilog)
uv run pytest tests/test_my_problem_hidden.py -v

# run all tests
uv run pytest tests/ -v

# syntax-only compile
iverilog -t null sources/my_module.sv
```

## 🔍 Debug helpers

```bash
# list Docker images
docker images | grep verilog_

# remove an image
docker rmi verilog_my_problem

# shell into container
docker run -it verilog_my_problem /bin/bash

# inspect build logs
docker build . -t test_build 2>&1 | less

# clean cache
docker system prune -a
```

## 📊 Verification checks

```bash
# inspect registry entry
cd /home/charlie/Desktop/GitHub/verilog-coding-template
grep -A 10 "id=\"my_problem\"" src/hud_controller/problems/basic.py

# pretty-print generated JSON
cat local-hud-my-problem.json | python3 -m json.tool

# list branches
cd /home/charlie/Desktop/GitHub/my-new-problem
git branch -a

# diff baseline vs golden
git diff my_problem_baseline my_problem_golden -- sources/

# view file tree
tree -L 2   # or
find . -type f | head -20
```

## 🔄 Refresh & rebuild

```bash
# bump Dockerfile cache buster
cd /home/charlie/Desktop/GitHub/verilog-coding-template
sed -i 's/ENV random=random[0-9]*/ENV random=random'$(date +%s)'/' Dockerfile
# or manually increment
# ENV random=random8 -> ENV random=random9

# copy local repo into framework
mkdir -p local-repos
cp -r /path/to/my-new-problem local-repos/problems

# rebuild without cache
docker build --no-cache -t verilog_my_problem .

# regenerate JSON configs
uv run utils/imagectl3.py verilog_ -j
```

## 📝 Quick editing

```bash
# edit registry
vim /home/charlie/Desktop/GitHub/verilog-coding-template/src/hud_controller/problems/basic.py

# edit Verilog source
vim sources/my_module.sv

# edit tests
vim tests/test_my_module_hidden.py

# edit spec
vim docs/Specification.md
```

## 🆘 Common fixes

```bash
# Issue: missing timescale
echo '`timescale 1ns/1ps' | cat - sources/my_module.sv > temp && mv temp sources/my_module.sv

# Issue: wrong tool name
grep -n "str_replace_editor" utils/imagectl3.py
# should be: str_replace_based_edit_tool

# Issue: missing Python deps
cd my-new-problem
uv pip install -e .

# Issue: branch out of sync
git fetch --all
git checkout my_problem_baseline
git pull origin my_problem_baseline
```

## 💡 Handy aliases (optional)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# navigation
alias vcd='cd /home/charlie/Desktop/GitHub/verilog-coding-template'
alias vcp='cd /home/charlie/Desktop/GitHub/verilog-problems'

# build & test
alias vbuild='uv run utils/imagectl3.py verilog_ -bvj --ids'
alias vtest='uv run hud eval local-hud-'

# clean Docker images
alias vclean='docker images | grep verilog_ | awk "{print \$3}" | xargs docker rmi'
```

Usage:
```bash
vcd                         # jump to framework
vbuild my_problem           # build my_problem
vtest my_problem.json claude --model ... --yes  # run eval
```

---

**Tip**: bookmark this file so you have the commands at your fingertips. 📌

