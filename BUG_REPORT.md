# Skid Buffer Golden Implementation - Bug Report

## Test Results

✅ **PASS** (2/4):
- `test_reset_flush` - Async reset works correctly
- `test_full_throughput_stream` - Pass-through mode works correctly

❌ **FAIL** (2/4):
- `test_alternating_backpressure_preserves_order` - Data ordering violated
- `test_random_handshake_stress` - Data duplication detected

## Bug Details

### Issue 1: Data Ordering Violated
```
Expected: 258 (0x102)
Got:      257 (0x101)
```

### Issue 2: Data Duplication
```
Expected: [1280, 1281, 1282, 1283, 1284, ...]
Got:      [1280, 1281, 1281, 1282, 1283, ...]  ← 1281 appears twice
```

## Root Cause Analysis

The bug occurs in the combinational logic when **both dequeue and enqueue happen simultaneously**.

### Current Logic (BUGGY):
```verilog
always @(*) begin
    // Apply dequeue first
    if (will_dequeue) begin
        if (buffer1_valid) begin
            buffer0_next       = buffer1;  // Move buffer1 to buffer0
            buffer0_valid_next = 1'b1;
            buffer1_valid_next = 1'b0;     // Clear buffer1
        end else begin
            buffer0_valid_next = 1'b0;
        end
    end

    // Then enqueue using updated state
    if (will_enqueue) begin
        if (!buffer0_valid_next) begin
            buffer0_next       = s_data;   // Direct to buffer0
            buffer0_valid_next = 1'b1;
        end else begin
            buffer1_next       = s_data;   // Go to buffer1
            buffer1_valid_next = 1'b1;
        end
    end
end
```

### Problem Scenario:

**Case 1: Both buffers valid, simultaneous dequeue + enqueue**
- Initial: buffer0_valid=1, buffer1_valid=1
- Dequeue: buffer0 → output, buffer1 → buffer0, buffer1_valid=0
- Enqueue: New data → buffer1
- Result: **Data from buffer0 is lost** (never output)

**Case 2: Only buffer0 valid, simultaneous dequeue + enqueue**
- Initial: buffer0_valid=1, buffer1_valid=0
- Dequeue: buffer0 → output, buffer0_valid=0
- Enqueue: sees buffer0_valid_next=0, so new data → buffer0
- Result: **New data goes to buffer0** (should be fine, but timing issue)

## The Fundamental Issue

The current implementation tries to handle dequeue-then-enqueue in combinational logic, but the logic doesn't correctly handle all cases where both operations happen simultaneously.

## Potential Fixes

### Option 1: Separate the operations more clearly

```verilog
always @(*) begin
    buffer0_next       = buffer0;
    buffer1_next       = buffer1;
    buffer0_valid_next = buffer0_valid;
    buffer1_valid_next = buffer1_valid;
    
    // Handle all 4 cases explicitly
    case ({will_dequeue, will_enqueue})
        2'b00: begin
            // No operation
        end
        2'b01: begin
            // Only enqueue
            if (!buffer0_valid) begin
                buffer0_next       = s_data;
                buffer0_valid_next = 1'b1;
            end else begin
                buffer1_next       = s_data;
                buffer1_valid_next = 1'b1;
            end
        end
        2'b10: begin
            // Only dequeue
            if (buffer1_valid) begin
                buffer0_next       = buffer1;
                buffer1_valid_next = 1'b0;
            end else begin
                buffer0_valid_next = 1'b0;
            end
        end
        2'b11: begin
            // Both dequeue and enqueue
            if (buffer1_valid) begin
                // Both buffers were full
                buffer0_next = buffer1;       // Move buffer1 to output
                buffer1_next = s_data;        // New data to buffer1
                // Both stay valid
            end else begin
                // Only buffer0 was full
                buffer0_next       = s_data;  // New data replaces buffer0
                buffer0_valid_next = 1'b1;
            end
        end
    endcase
end
```

### Option 2: Use a different skid buffer architecture

Consider using a more standard two-register skid buffer with explicit state machine.

## Recommendations

1. **Fix the combinational logic** to handle simultaneous operations correctly
2. **Add more test cases** for edge cases
3. **Verify with waveform dump** to understand exact timing
4. **Consider using a proven skid buffer implementation** from literature

## Test Command

```bash
cd /home/charlie/Desktop/GitHub/verilog-problems
uv run pytest tests/test_skid_buffer_hidden.py -v
```

## Status

🔴 **BLOCKED** - Golden implementation needs fixing before proceeding with:
- Creating baseline version
- Setting up Git branches
- Registering in framework
- Running agent evaluation

## Next Steps

1. Fix the golden implementation
2. Re-run tests to confirm all 4 tests pass
3. Then proceed with framework integration

