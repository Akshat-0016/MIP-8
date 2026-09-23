import sys
from pathlib import Path

from isa import OPCODES, REGISTERS, encode


def parse_number(value):
    value = value.strip()

    if value.lower().startswith("0x"):
        return int(value, 16)

    return int(value, 10)


def parse_register(value):
    value = value.strip().upper()

    if value not in REGISTERS:
        raise ValueError(f"Unknown register: {value}")

    return REGISTERS[value]


def assemble_instruction(line):
    parts = line.replace(",", " ").split()

    if not parts:
        return None

    mnemonic = parts[0].upper()
    args = parts[1:]

    # -------------------------
    # NOP / HALT
    # -------------------------
    if mnemonic == "NOP":
        return encode(OPCODES["NOP"])

    if mnemonic == "HALT":
        return encode(OPCODES["HALT"])

    # -------------------------
    # LOAD Rn, immediate
    # RS = 00 means immediate
    # -------------------------
    if mnemonic == "LOAD":
        if len(args) != 2:
            raise ValueError("LOAD syntax: LOAD Rn, immediate")

        rd = parse_register(args[0])
        imm = parse_number(args[1])

        if not 0 <= imm <= 0xFF:
            raise ValueError("Immediate must fit in 8 bits")

        return encode(OPCODES["LOAD"], rd=rd, rs=0b00, imm=imm)

    # -------------------------
    # MOV Rd, Rs
    # -------------------------
    if mnemonic == "MOV":
        if len(args) != 2:
            raise ValueError("MOV syntax: MOV Rd, Rs")

        rd = parse_register(args[0])
        rs = parse_register(args[1])

        return encode(OPCODES["MOV"], rd=rd, rs=rs)

    # -------------------------
    # ALU operations
    # -------------------------
    alu_instructions = {
        "ADD": "ADD",
        "SUB": "SUB",
        "AND": "AND",
        "OR": "OR",
        "XOR": "XOR",
        "NOT": "NOT",
        "INC": "INC",
        "DEC": "DEC",
    }

    if mnemonic in alu_instructions:
        if len(args) != 2:
            raise ValueError(f"{mnemonic} syntax: {mnemonic} Rd, Rs")

        rd = parse_register(args[0])
        rs = parse_register(args[1])

        return encode(OPCODES[mnemonic], rd=rd, rs=rs)

    # -------------------------
    # JMP / JZ
    # -------------------------
    if mnemonic in ("JMP", "JZ"):
        if len(args) != 1:
            raise ValueError(f"{mnemonic} syntax: {mnemonic} address")

        address = parse_number(args[0])

        if not 0 <= address <= 0xFF:
            raise ValueError("Address must fit in 8 bits")

        return encode(OPCODES[mnemonic], imm=address)

    raise ValueError(f"Unknown instruction: {mnemonic}")


def intel_hex_record(address, data):
    """
    Create one Intel HEX data record.
    """

    record_type = 0x00
    length = len(data)

    values = [
        length,
        (address >> 8) & 0xFF,
        address & 0xFF,
        record_type,
        *data,
    ]

    checksum = (-sum(values)) & 0xFF

    return ":" + "".join(f"{x:02X}" for x in values) + f"{checksum:02X}"


def write_intel_hex(words, output_path):
    """
    Write 16-bit MIP-8 instruction words as Intel HEX.

    Each instruction occupies two bytes:
        high byte
        low byte

    Address 0 = first instruction.
    """

    data = bytearray()

    for word in words:
        data.append((word >> 8) & 0xFF)
        data.append(word & 0xFF)

    lines = []

    # 16 bytes per Intel HEX record
    chunk_size = 16

    for offset in range(0, len(data), chunk_size):
        chunk = data[offset : offset + chunk_size]

        # Intel HEX address is a BYTE address.
        lines.append(intel_hex_record(offset, chunk))

    # End-of-file record
    lines.append(":00000001FF")

    output_path.write_text("\n".join(lines) + "\n")


def assemble_file(input_path):
    source = input_path.read_text().splitlines()

    words = []

    for line_number, line in enumerate(source, start=1):
        # Remove comments
        line = line.split(";", 1)[0].strip()

        if not line:
            continue

        try:
            word = assemble_instruction(line)
        except ValueError as e:
            raise ValueError(f"Line {line_number}: {e}") from e

        words.append(word)

    return words


def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler/assembler.py <program.asm>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    output_path = input_path.with_suffix(".hex")

    try:
        words = assemble_file(input_path)
        write_intel_hex(words, output_path)

    except ValueError as e:
        print(f"Assembly error: {e}")
        sys.exit(1)

    print(f"Assembled {len(words)} instruction(s).")
    print(f"Output: {output_path}")

    for address, word in enumerate(words):
        print(f"{address:02X}: {word:04X}")


if __name__ == "__main__":
    main()
