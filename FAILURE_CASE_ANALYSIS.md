# Failure Case Analysis: Bash Heredoc Timeout

This document analyzes a critical failure pattern observed during AI agent evaluation of the skid buffer problem.

---

## Overview

**Failure Rate**: ~40% of failed attempts (before mitigation)  
**Agent Model**: Claude Sonnet 4.5  
**Problem**: Skid Buffer (Medium difficulty)  
**Failure Type**: Timeout (5 minutes) during file editing operations

---

## A. Symptoms

### External Observable Behavior

**What went wrong**:
1. Agent attempted to edit the Verilog source file (`sources/skid_buffer.sv`)
2. Agent's tool call appeared to execute but never returned
3. After 5 minutes (300 seconds), the execution timed out with error:
   ```
   Error executing tool bash: timed out: bash has not returned in 300.0 seconds
   ```
4. Agent consumed significant steps (typically 8-10 out of 15 available) before timing out
5. No actual code modifications were made to the target file
6. Test results showed baseline (unimplemented) code still present

### Specific Trace Example

**Episode ID**: Episode 3 (from initial evaluation)  
**Steps Used**: 3/15 before timeout  
**Final State**: FAILED - No implementation completed

**Agent's Tool Call**:
```json
{
  "id": "toolu_01LzxKKADSD18C9FqiH6Dxz8",
  "name": "bash",
  "arguments": {
    "command": "cd /home/ubuntu/example-verilog-codebase && cat << 'EOF' > sources/skid_buffer.sv\n`timescale 1ns/1ps\n\nmodule skid_buffer #(\n    parameter DATA_WIDTH = 64\n)(\n    input                    clk,\n    input                    rst_n,\n    input  [DATA_WIDTH-1:0]  s_data,\n    input                    s_valid,\n    output                   s_ready,\n    output [DATA_WIDTH-1:0]  m_data,\n    output                   m_valid,\n    input                    m_ready\n);\n\n    // [Implementation code]\n\nendmodule\nEOF"
  }
}
```

**Expected Behavior**: File should be written and control returned to agent  
**Actual Behavior**: Command hangs indefinitely until 5-minute timeout

---

## B. Root Cause

### Underlying Technical Bug

The root cause is a **design flaw in the MCP (Model Context Protocol) bash tool** when handling heredoc syntax.

#### The Bug Chain

1. **Agent's Intent**: 
   - Agent wants to write a complete Verilog file
   - Chooses `cat << 'EOF' > file` heredoc syntax (common in shell scripting)

2. **MCP Bash Tool Implementation**:
   - The bash tool wraps the user's command with its own sentinel
   - It appends `echo '<<exit>>'` after the command to detect completion
   - For heredoc, this creates:
   ```bash
   cat << 'EOF' > sources/skid_buffer.sv
   [content]
   EOF
   echo '<<exit>>'  # MCP's sentinel
   ```

3. **The Fatal Flaw**:
   - When `EOF` terminator is followed by the sentinel on a new line, bash interprets this as:
     - The heredoc `EOF` terminator (line by itself)
     - Then tries to execute `echo '<<exit>>'` as the next command
   - However, the heredoc parsing gets confused by the newline handling
   - In some cases, bash waits for additional input, creating a **stdin blocking state**
   - The MCP tool waits for the `<<exit>>` sentinel that never arrives
   - **Result**: Infinite hang until timeout

4. **Why It's Not an Environment Issue**:
   - The same heredoc command works fine in a normal interactive bash shell
   - The bug is specific to the MCP tool's command wrapping mechanism
   - The issue is reproducible across different file contents and sizes

### Connection to Observed Symptoms

| Symptom | Root Cause Connection |
|---------|----------------------|
| 5-minute timeout | MCP tool's hardcoded timeout limit while waiting for `<<exit>>` sentinel |
| No file modifications | Bash never completes the command, so file write never happens |
| High step consumption | Agent repeats timeout pattern across multiple attempts before giving up |
| Baseline code remains | File editing failed, so original TODO implementation stays unchanged |

---

## C. Faulty Assumptions / Missed Insights

### Agent's Flawed Reasoning

#### Assumption 1: "Bash heredoc is the most reliable way to write files"
**Why it's wrong**:
- Heredoc is powerful in interactive shells
- But it's fragile when commands are wrapped by frameworks
- Special characters, newlines, and EOF markers can break wrapping logic

**What the agent missed**:
- The instructions explicitly warned: "⚠️ CRITICAL: Use str_replace_based_edit_tool ONLY for file editing. NO bash heredoc! ⚠️"
- Despite the warning, agent's training bias toward bash scripting overrode the explicit instruction

#### Assumption 2: "If a tool is available, it's safe to use for its apparent purpose"
**Why it's wrong**:
- Tool availability doesn't guarantee correctness in all scenarios
- The `bash` tool was available but fundamentally broken for file editing via heredoc
- Tools can have edge cases or bugs that aren't immediately obvious

**What the agent missed**:
- Should have tested with a simple command first (e.g., `echo "test" > file`)
- Should have switched tools after first timeout instead of retrying same approach

#### Assumption 3: "Timeout errors are transient and retrying will succeed"
**Why it's wrong**:
- Some errors are deterministic based on the command structure
- Retrying the exact same bash heredoc command will always timeout
- No amount of retries can fix a fundamental tool bug

**What the agent missed**:
- Failed to recognize the pattern: "This specific command structure times out"
- Needed to try a completely different approach (different tool, not different heredoc syntax)

### Misconceptions About File Editing

#### Misconception 1: "More powerful tools are better"
**Reality**: Simple, purpose-built tools often work better than general-purpose tools

- `str_replace_based_edit_tool`: Designed specifically for editing files, handles escaping and special characters safely
- `bash heredoc`: General scripting construct, prone to quoting/escaping issues when wrapped

#### Misconception 2: "Shell commands are universally compatible"
**Reality**: Shell commands behave differently when executed through wrappers/frameworks

- Direct bash: Heredoc works fine
- MCP-wrapped bash: Sentinel injection breaks heredoc parsing
- The execution context matters as much as the command syntax

### Missing Domain Knowledge

#### Knowledge Gap 1: MCP Tool Implementation Details
**What agent didn't know**:
- MCP bash tool injects a sentinel (`<<exit>>`) for completion detection
- This injection can interfere with heredoc EOF markers
- The tool has a 5-minute hard timeout

**Impact**:
- Agent couldn't anticipate the failure mode
- Couldn't debug why the command hung
- Couldn't reason about alternative approaches

#### Knowledge Gap 2: Heredoc Edge Cases
**What agent didn't know**:
- EOF marker must be on a line by itself with no trailing characters
- Additional output after EOF can confuse bash's heredoc parser
- Quoting the delimiter (`'EOF'` vs `EOF`) affects variable expansion but not this bug

**Impact**:
- Agent tried variations like changing EOF to ENDOFFILE
- None of these variations addressed the actual root cause

#### Knowledge Gap 3: Tool Selection Strategy
**What agent didn't know**:
- When multiple tools are available, prefer the most specific one
- File editing problems should use file editing tools, not shell scripting
- Problem descriptions often contain tool recommendations for a reason

**Impact**:
- Agent defaulted to bash (most familiar from training data)
- Ignored the specialized `str_replace_based_edit_tool` that was explicitly mentioned

---

## D. The Fix: How We Resolved This

### Mitigation Strategy

We implemented a **multi-layered defense** to prevent this failure mode:

#### Layer 1: Remove the Broken Tool
**Action**: Removed `bash` from the `allowed_tools` list in agent configuration

**Before**:
```json
"allowed_tools": ["bash", "str_replace_based_edit_tool"]
```

**After**:
```json
"allowed_tools": ["str_replace_based_edit_tool"]
```

**Rationale**: 
- If a tool is fundamentally broken for the primary use case (file editing), remove it
- Forces agent to use the correct tool
- Prevents wasted steps on timeout attempts

#### Layer 2: Explicit Instructions
**Action**: Updated problem description with clear guidance

**Added to description**:
```
Note: Only str_replace_based_edit_tool is available. Use it for both viewing and editing files.

Implementation Steps:
1. View the file using: str_replace_based_edit_tool(command="view", path="...")
2. Edit using: str_replace_based_edit_tool(command="str_replace", path="...", old_str="...", new_str="...")
```

**Rationale**:
- Make it impossible to miss which tool to use
- Provide concrete examples of the correct tool invocations
- Reduce ambiguity in agent's decision-making

#### Layer 3: Warning Messages (Preserved for Documentation)
**Action**: Kept strong warnings in problem description

**Example warning**:
```
⚠️ CRITICAL: Use str_replace_based_edit_tool ONLY for file editing. NO bash heredoc! ⚠️

Bash heredoc (cat >, echo >, tee) will TIMEOUT (5 minutes) and WASTE your limited steps!
```

**Rationale**:
- Even though bash is removed, warnings help if tool set changes
- Documents the issue for future reference
- Educates about the failure mode

### Results After Fix

| Metric | Before Fix | After Fix |
|--------|-----------|-----------|
| Timeout Rate | ~40% | 0% |
| Average Steps to Completion | 12-15 (if successful) | 8-10 |
| Success Rate | 60% | 80% |
| Time per Episode | 8-10 minutes | 4-5 minutes |

**Key Improvements**:
- ✅ Zero timeout failures
- ✅ Faster completion (no wasted timeout waits)
- ✅ More consistent behavior across episodes
- ✅ Better step efficiency

---

## E. Lessons Learned

### For Problem Designers

1. **Curate Tool Sets Carefully**
   - Not all available tools should be exposed to agents
   - Test tools thoroughly in the evaluation environment, not just locally
   - When in doubt, provide fewer, more reliable tools

2. **Explicit Is Better Than Implicit**
   - Don't assume agents will discover the "right" tool
   - Provide explicit step-by-step instructions with tool names
   - Show example tool invocations in the problem description

3. **Defense in Depth**
   - Use multiple layers of guidance (tool restriction + instructions + warnings)
   - Each layer catches agents at different reasoning stages
   - Redundancy in guidance is acceptable for critical issues

### For Agent Developers

1. **Tool Bugs Are Real**
   - Framework tools can have bugs or edge cases
   - Timeout errors can indicate tool bugs, not just environment issues
   - Test tool interactions, not just tool APIs

2. **Respect Explicit Instructions**
   - When a problem says "use tool X, not tool Y", there's usually a good reason
   - Training data bias (preference for bash) shouldn't override explicit guidance
   - Treat problem-specific instructions as constraints, not suggestions

3. **Fail Fast and Switch**
   - If a tool times out once, try a different tool immediately
   - Don't retry the same approach multiple times
   - Step budget is precious; timeouts are expensive

### For Evaluation Frameworks

1. **Shorter Timeouts for Interactive Operations**
   - 5 minutes is too long for a file editing command
   - Consider 30-60 second timeouts with exponential backoff
   - Fail fast to preserve step budget

2. **Tool Validation**
   - Validate that wrapped tools behave correctly
   - Test edge cases (heredocs, special characters, large inputs)
   - Provide tool compatibility matrices

3. **Better Error Messages**
   - "timed out: bash has not returned" doesn't indicate root cause
   - Could include: "Note: bash heredoc commands may not work in this environment"
   - Help agents learn from failures

---

## F. Conclusion

This failure case demonstrates a critical lesson: **tool availability does not equal tool correctness**. The bash tool was available and seemed appropriate for file editing, but a subtle interaction between heredoc syntax and MCP's sentinel injection created a deterministic timeout failure.

The fix required both **removing the problematic tool** and **providing explicit guidance** on the correct tool. This dual approach reduced timeout failures from 40% to 0% and improved overall success rate from 60% to 80%.

**Key Takeaway**: When designing AI agent evaluations, prioritize tool reliability over tool flexibility. A small set of reliable, purpose-built tools outperforms a large set of general-purpose tools with edge cases.

---

**Document Version**: 1.0  
**Last Updated**: November 2025  
**Related Documents**: 
- [GRADER_ANALYSIS.md](GRADER_ANALYSIS.md) - Technical analysis of test suite
- [README.md](README.md) - Evaluation results summary

