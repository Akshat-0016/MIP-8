"""
MIP-8 ISA definitions.

Instruction format:

15          12 11      10 9       8 7             0
+-------------+----------+----------+---------------+
|   OPCODE    |    RD    |    RS    |      IMM      |
+-------------+----------+----------+---------------+

OPCODE : 4 bits
RD     : 2 bits
RS     : 2 bits
IMM    : 8 bits
"""

OPCODES = {
    "NOP": 0b0000,
    "STORE": 0b0001,
    "LOAD-MEM": 0b0010,
    "MOV": 0b0011,
    "ADD": 0b0100,
    "SUB": 0b0101,
    "AND": 0b0110,
    "OR": 0b0111,
    "XOR": 0b1000,
    "NOT": 0b1001,
    "INC": 0b1010,
    "DEC": 0b1011,
    "LOAD": 0b1100,
    "JMP": 0b1101,
    "JZ": 0b1110,
    "HALT": 0b1111,
}


REGISTERS = {
    "R0": 0b00,
    "R1": 0b01,
    "R2": 0b10,
    "R3": 0b11,
}


def register_number(name):
    name = name.upper()

    if name not in REGISTERS:
        raise ValueError(f"Unknown register: {name}")

    return REGISTERS[name]


def opcode_number(name):
    name = name.upper()

    if name not in OPCODES:
        raise ValueError(f"Unknown opcode: {name}")

    return OPCODES[name]


def encode(opcode, rd=0, rs=0, imm=0):
    if not 0 <= opcode <= 0xF:
        raise ValueError("Opcode must be 4 bits")

    if not 0 <= rd <= 0x3:
        raise ValueError("RD must be 2 bits")

    if not 0 <= rs <= 0x3:
        raise ValueError("RS must be 2 bits")

    if not 0 <= imm <= 0xFF:
        raise ValueError("IMM must be 8 bits")

    return (opcode << 12) | (rd << 10) | (rs << 8) | imm
