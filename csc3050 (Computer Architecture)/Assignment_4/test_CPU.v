`include "CPU.v"
`timescale 1ns/1ps

module test_CPU;

    reg RESET = 0;
    CPU test_CPU (RESET);

endmodule