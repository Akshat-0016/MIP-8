# MIP-8

**MIP-8 (Mini Instruction Processor - 8 bit)** is a custom 8-bit processor
designed and implemented using digital logic in the Digital simulator.

The project is inspired by the concepts explored in **Nand2Tetris**, but
implements its own instruction set, datapath, control logic, memory system,
and assembler.

## Features

- 8-bit datapath
- 16-bit instructions
- 4 general-purpose 8-bit registers
- 256-byte RAM
- 256-instruction ROM
- 8-bit Program Counter
- Instruction Register
- 8-operation ALU
- Hardwired combinational control decoder
- Conditional and unconditional jumps
- Python assembler
- Intel HEX output for ROM

## Architecture

## Architecture

```text
             +------+
             |  PC  |
             +--+---+
                |
                v
             +------+
             | ROM  |
             +--+---+
                |
                v
             +------+
             |  IR  |
             +--+---+
                |
                v
           +---------+
           | Decoder |
           +----+----+
                |
       +--------+--------+
       |        |        |
       v        v        v
   Register    ALU      RAM
    Bank        |        |
       |        |        |
       +--------+--------+
                |
                v
             Writeback
```

```text
## Components

| Component | Description |
|----------------------|-------------------------------------------|
|          ALU         | 8-bit arithmetic and logic operations     |
|     Register Bank    | Four 8-bit general-purpose registers      |
|    Program Counter   | 8-bit instruction address counter         |
| Instruction Register | Holds and decodes the current instruction |
|          ROM         | Stores 256 16-bit instructions            |
|          RAM         | Stores 256 bytes of data                  |
|        Decoder       | Generates hardwired control signals       |
|       Assembler      | Converts assembly programs into Intel HEX |
|----------------------|-------------------------------------------|

Instruction Set

MIP-8 supports:

NOP
STORE
LOAD-MEM
MOV
ADD
SUB
AND
OR
XOR
NOT
INC
DEC
LOAD
JMP
JZ
HALT

The complete instruction-set specification is available in
ISA.md.

Example Program
LOAD R1, 5
STORE R1, 0x20
LOAD-MEM R2, 0x20
HALT

This program:

Loads 5 into R1
Stores R1 into RAM address 0x20
Reads RAM address 0x20 into R2
Halts the processor

Expected result:

R1 = 5
RAM[0x20] = 5
R2 = 5
Assembler

The project includes a Python assembler.

From the project root:

python assembler/assembler.py programs/test.asm

The assembler generates an Intel HEX file which can be loaded into the
Digital ROM.

Project Structure
MIP-8/
├── ALU.dig
├── RegisterBank.dig
├── PC.dig
├── IR.dig
├── ROM.dig
├── RAM.dig
├── DECODER.dig
├── CPU.dig
├── MIP8.dig
├── MIP8.circ
├── ISA.md
├── README.md
├── assembler/
│   ├── assembler.py
│   ├── isa.py
│   └── tests/
└── programs/
    ├── test.asm
    └── test.hex
Project Goal

The goal of MIP-8 is to build a complete small processor from fundamental
digital logic components, define a custom instruction set, create an assembler
for it, and demonstrate the complete path from assembly source code to
processor execution.
```
