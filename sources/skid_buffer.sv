`timescale 1ns/1ps

module skid_buffer #(
    parameter DATA_WIDTH = 64
)(
    input                    clk,
    input                    rst_n,
    input  [DATA_WIDTH-1:0]  s_data,
    input                    s_valid,
    output                   s_ready,
    output [DATA_WIDTH-1:0]  m_data,
    output                   m_valid,
    input                    m_ready
);
    // TODO: Implement two-entry skid buffer.
    // Requirements (see docs/Specification.md):
    // - Provide up to two beats of storage between source and sink.
    // - Assert s_ready when at least one entry is free.
    // - Assert m_valid when buffer0 holds valid data; drive m_data accordingly.
    // - On reset (rst_n=0) clear both entries asynchronously.
    // - Maintain ordering while handling enqueue/dequeue per ready/valid handshake.
endmodule

