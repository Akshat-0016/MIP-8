import sys
from pathlib import Path

from isa import (
    OPCODES,
    REGISTERS,
    encode,
    opcode_number,
    register_number,
)


def parse_number(value):
    value = value.strip()

    if value.lower().startswith("0x"):
        return int(value, 16)

    return int(value, 10)


def clean_line(line):
    # Remove comments
    line = line.split(";", 1)[0].strip()

    if not line:
        return None

    return line


def parse_register(token):
    token = token.strip().upper()

    if token not in REGISTERS:
        raise ValueError(f"Invalid register: {token}")

    return register_number(token)


def assemble_line(line):
    parts = line.replace(",", " ").split()

    if not parts:
        return None

    mnemonic = parts[0].upper()

    # -------------------------
    # No-operand instructions
    # -------------------------
    if mnemonic in ("NOP", "HALT"):
        if len(parts) != 1:
            raise ValueError(f"{mnemonic} takes no operands")

        return encode(opcode_number(mnemonic))

    # -------------------------
    # LOAD immediate
    # LOAD Rn, imm
    # -------------------------
    if mnemonic == "LOAD":
        if len(parts) != 3:
            raise ValueError("LOAD syntax: LOAD Rn, immediate")

        rd = parse_register(parts[1])
        imm = parse_number(parts[2])

        if not 0 <= imm <= 0xFF:
            raise ValueError("Immediate must be 0x00..0xFF")

        # RS=00 means immediate
        return encode(OPCODES["LOAD"], rd=rd, rs=0, imm=imm)

    # -------------------------
    # STORE
    # STORE Rn, address
    # -------------------------
    if mnemonic == "STORE":
        if len(parts) != 3:
            raise ValueError("STORE syntax: STORE Rn, address")

        rd = parse_register(parts[1])
        address = parse_number(parts[2])

        if not 0 <= address <= 0xFF:
            raise ValueError("Address must be 0x00..0xFF")

        # Hardware verified:
        # RD = source register
        # IMM = RAM address
        # RS = 00
        return encode(
            OPCODES["STORE"],
            rd=rd,
            rs=0,
            imm=address,
        )

    # -------------------------
    # LOAD-MEM
    # LOAD-MEM Rn, address
    # -------------------------
    if mnemonic == "LOAD-MEM":
        if len(parts) != 3:
            raise ValueError("LOAD-MEM syntax: LOAD-MEM Rn, address")

        rd = parse_register(parts[1])
        address = parse_number(parts[2])

        if not 0 <= address <= 0xFF:
            raise ValueError("Address must be 0x00..0xFF")

        # Hardware verified:
        # RD = destination register
        # IMM = RAM address
        # RS = 00
        return encode(
            OPCODES["LOAD-MEM"],
            rd=rd,
            rs=0,
            imm=address,
        )

    # -------------------------
    # Register-register ALU
    # ADD Rd, Rs
    # SUB Rd, Rs
    # AND Rd, Rs
    # OR Rd, Rs
    # XOR Rd, Rs
    # NOT Rd, Rs
    # INC Rd, Rs
    # DEC Rd, Rs
    # -------------------------
    alu_instructions = {
        "MOV",
        "ADD",
        "SUB",
        "AND",
        "OR",
        "XOR",
        "NOT",
        "INC",
        "DEC",
    }

    if mnemonic in alu_instructions:
        if len(parts) != 3:
            raise ValueError(f"{mnemonic} syntax: {mnemonic} Rd, Rs")

        rd = parse_register(parts[1])
        rs = parse_register(parts[2])

        return encode(
            OPCODES[mnemonic],
            rd=rd,
            rs=rs,
            imm=0,
        )

    # -------------------------
    # Jump instructions
    # -------------------------
    if mnemonic in ("JMP", "JZ"):
        if len(parts) != 2:
            raise ValueError(f"{mnemonic} syntax: {mnemonic} address")

        address = parse_number(parts[1])

        if not 0 <= address <= 0xFF:
            raise ValueError("Address must be 0x00..0xFF")

        return encode(
            OPCODES[mnemonic],
            rd=0,
            rs=0,
            imm=address,
        )

    raise ValueError(f"Unknown instruction: {mnemonic}")


def assemble(source):
    words = []

    for line_number, raw_line in enumerate(source.splitlines(), 1):
        line = clean_line(raw_line)

        if line is None:
            continue

        try:
            word = assemble_line(line)
        except ValueError as exc:
            raise ValueError(f"Line {line_number}: {exc}") from exc

        if word is not None:
            words.append(word)

    if len(words) > 256:
        raise ValueError("Program exceeds 256 instructions")

    return words


def intel_hex_record(address, data):
    record_type = 0x00
    length = len(data)

    checksum_sum = (
        length + ((address >> 8) & 0xFF) + (address & 0xFF) + record_type + sum(data)
    )

    checksum = (-checksum_sum) & 0xFF

    return (
        f":{length:02X}{address:04X}{record_type:02X}{data.hex().upper()}{checksum:02X}"
    )


def to_intel_hex(words):
    lines = []

    address = 0

    # Digital ROM is configured for big-endian import.
    # Therefore each 16-bit instruction is emitted:
    # high byte, low byte.
    for word in words:
        high = (word >> 8) & 0xFF
        low = word & 0xFF

        lines.append(intel_hex_record(address, bytes([high, low])))

        address += 2

    # EOF record
    lines.append(":00000001FF")

    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python assembler/assembler.py <program.asm>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Error: file not found: {input_path}")
        sys.exit(1)

    source = input_path.read_text()

    try:
        words = assemble(source)
    except ValueError as exc:
        print(f"Assembly error: {exc}")
        sys.exit(1)

    output_path = input_path.with_suffix(".hex")
    output_path.write_text(to_intel_hex(words))

    print(f"Assembled {len(words)} instruction(s).")
    print(f"Output: {output_path}")

    for address, word in enumerate(words):
        print(f"{address:02X}: {word:04X}")


if __name__ == "__main__":
    main()
