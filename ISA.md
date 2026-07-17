# MIP-8 ISA Specification
Version: 1.0

---

# CPU Overview

MIP-8 (Mini Instruction Processor - 8 bit)

Architecture:
- 8-bit Datapath
- 16-bit Instructions
- 8-bit Address Space
- 4 General Purpose Registers
- 256 Bytes RAM
- 256 Instructions ROM

---

# Registers

| Binary | Register |
|--------|----------|
| 00 | R0 |
| 01 | R1 |
| 10 | R2 |
| 11 | R3 |

---

# Instruction Format

15          12 11    10 9      8 7              0

+-------------+--------+--------+----------------+
|   OPCODE    |   RD   |   RS   |   IMMEDIATE    |
+-------------+--------+--------+----------------+

Opcode     : 4 bits
RD          : Destination Register
RS          : Source Register
Immediate   : 8-bit Immediate / Address

---

# ALU Operations

| ALU_SEL | Operation |
|---------|-----------|
|000|ADD|
|001|SUB|
|010|AND|
|011|OR|
|100|XOR|
|101|NOT|
|110|INC|
|111|DEC|

---

# Opcode Table

| Opcode | Mnemonic | Description |
|---------|----------|-------------|
|0000|NOP|No operation|
|0001|LOAD|Load Immediate / Memory|
|0010|STORE|Store Register|
|0011|MOV|Move Register|
|0100|ADD|RD = RD + RS|
|0101|SUB|RD = RD - RS|
|0110|AND|RD = RD & RS|
|0111|OR|RD = RD \| RS|
|1000|XOR|RD = RD ^ RS|
|1001|NOT|RD = ~RD|
|1010|INC|RD = RD + 1|
|1011|DEC|RD = RD - 1|
|1100|CMP|Compare Registers|
|1101|JMP|Jump|
|1110|JZ|Jump if Zero|
|1111|HALT|Stop Processor|

---

# Flags

ZERO
CARRY

---

# Register File

Registers : 4

Width : 8 bits

Ports:
- 2 Read Ports
- 1 Write Port

---

# Program Counter

Width : 8 bits

Functions:
- Increment
- Jump
- Reset

---

# Memories

ROM
- Address Width : 8
- Data Width : 16
- Size : 256 Instructions

RAM
- Address Width : 8
- Data Width : 8
- Size : 256 Bytes

---

# Frozen Interfaces

ALU
Inputs:
A(8)
B(8)
ALU_SEL(3)

Outputs:
RESULT(8)
ZERO
CARRY

RegisterBank

Inputs:
CLK
WE
WR_ADDR(2)
WR_DATA(8)
RD_ADDR1(2)
RD_ADDR2(2)

Outputs:
RD_DATA1(8)
RD_DATA2(8)

ProgramCounter

Inputs:
CLK
RESET
PC_EN
JUMP_EN
JUMP_ADDR(8)

Outputs:
PC(8)

Instruction Register

Inputs:
CLK
IR_EN
INSTR_IN(16)

Outputs:
OPCODE(4)
RD(2)
RS(2)
IMM(8)

ROM

Inputs:
ADDRESS(8)

Outputs:
INSTRUCTION(16)
