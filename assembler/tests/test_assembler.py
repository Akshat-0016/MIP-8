import sys
from pathlib import Path

# Allow importing assembler/assembler.py
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from assembler import assemble


def test_nop():
    assert assemble("NOP") == [0x0000]


def test_halt():
    assert assemble("HALT") == [0xF000]


def test_load_immediate():
    assert assemble("LOAD R1, 5") == [0xC405]


def test_load_hex():
    assert assemble("LOAD R2, 0x7D") == [0xC87D]


def test_mov():
    assert assemble("MOV R1, R2") == [0x34A0]


def test_add():
    assert assemble("ADD R1, R2") == [0x44A0]


def test_sub():
    assert assemble("SUB R3, R0") == [0x5C00]


def test_and():
    assert assemble("AND R1, R3") == [0x47A0]


def test_or():
    assert assemble("OR R2, R1") == [0x7480]


def test_xor():
    assert assemble("XOR R0, R2") == [0x8820]


def test_not():
    assert assemble("NOT R1, R0") == [0x9400]


def test_inc():
    assert assemble("INC R2, R0") == [0xA800]


def test_dec():
    assert assemble("DEC R3, R1") == [0xBD00]


def test_jmp():
    assert assemble("JMP 0x20") == [0xD020]


def test_jz():
    assert assemble("JZ 0x40") == [0xE040]


def test_comments():
    program = """
        ; load 5
        LOAD R1, 5

        ; stop
        HALT
    """

    assert assemble(program) == [
        0xC405,
        0xF000,
    ]
