#!/usr/bin/env python3
# (c) 2023 Felipe Correa da Silva Sanches <juca@members.fsf.org>
# Licensed under GPL version 3 or later

import os
import sys

import importlib  
tlcs900h_disasm = importlib.import_module("tlcs900h-disasm")
TLCS900H_Trace = tlcs900h_disasm.TLCS900H_Trace

if not (len(sys.argv) == 2):
    sys.exit(f"usage: {sys.argv[0]} <rom_file>")


rom_file = sys.argv[1]
disasm_dir = f"output"
KNOWN_LABELS = {}
POSSIBLY_UNUSED_CODEBLOCKS = {}

RELOCATION_BLOCKS = (
    # physical,  logical, length 
    (0x000000,  0xe00000, 0x200000),
)

rom = open(rom_file, "rb")
entry_points = []
jump_table_from = []

def read_symbols(base_addr, num_symbols):
    global entry_points
    rom.seek(base_addr)
    string_addresses = []
    address = -1
    for i in range(num_symbols+1):
        address = ord(rom.read(1))
        address = ord(rom.read(1)) << 8 | address
        address = ord(rom.read(1)) << 16 | address
        address = ord(rom.read(1)) << 24 | address
        string_addresses.append(address)

    print(hex(len(string_addresses)))

    symbol_name = ""
    symbol_names = []
    while len(symbol_names) < num_symbols:
        c = rom.read(1)
        if ord(c) == 0xFF:
            pass
        elif ord(c) == 0:
            symbol_names.append(symbol_name)
            symbol_name = ""
        else:
            symbol_name += c.decode("utf8")

    n = ord(rom.read(1))
    n = (ord(rom.read(1)) << 8) | n
    assert n == num_symbols


    routine_addresses = []
    address = -1
    for i in range(num_symbols+1):
        address = ord(rom.read(1))
        address = ord(rom.read(1)) << 8 | address
        address = ord(rom.read(1)) << 16 | address
        address = ord(rom.read(1)) << 24 | address
        routine_addresses.append(address)

    print(hex(len(routine_addresses)))

    print(len(symbol_names))
    for i in range(num_symbols):
        print(f"{routine_addresses[i]:06X}: {symbol_names[i]}")
        KNOWN_LABELS[routine_addresses[i]] = symbol_names[i]
        if routine_addresses[i] not in entry_points:
            entry_points.append(routine_addresses[i])


def read_jump_table(called_from, base_addr, num_entries):
    global entry_points
    if called_from not in jump_table_from:
        jump_table_from.append(called_from)
    for n in range(num_entries):
        rom.seek((base_addr & 0x1FFFFF) + n*4)
        address = ord(rom.read(1))
        address = ord(rom.read(1)) << 8 | address
        address = ord(rom.read(1)) << 16 | address
        address = ord(rom.read(1)) << 24 | address
        if address not in entry_points:
            entry_points.append(address)


def ignore_jump_table(called_from, base_addr):
    if called_from not in jump_table_from:
        jump_table_from.append(called_from)


def register_jump_table_addresses(called_from, addresses):
    global entry_points
    # print(f"from: {hex(called_from)}")
    # print(list(map(hex, addresses)))

    if called_from not in jump_table_from:
        jump_table_from.append(called_from)

    for address in addresses:
        if address not in entry_points:
            entry_points.append(address)

def read_addresses_with_16bit_offsets(base_addr, offsets_addr, num_entries):
    addresses = []
    for i in range(num_entries):
        rom.seek((offsets_addr & 0x1fffff) + 2*i)
        offset = ord(rom.read(1))
        offset = (ord(rom.read(1)) << 8) | offset
        addresses.append(base_addr + offset)
    return addresses


def read_jump_table_16bit_offsets(called_from, base_addr, offsets_addr, num_entries):
    addresses = read_addresses_with_16bit_offsets(base_addr, offsets_addr, num_entries)
    register_jump_table_addresses(called_from, addresses)


for code_test in (
    (0xEF4784, 0xE00178, [0x00, 0xa6, 0x20, 0xa6, 0x43, 0x5b, 0x76, 0x9a]),
    (0xF46524, 0xE44A42, [0x00, 0x33, 0x47, 0x47, 0x0e, 0x33, 0x1c, 0x3c]),
    (0xF4670F, 0xe44a6a, [0x00, 0xa3, 0x07, 0x0e, 0x15, 0x1c, 0x23, 0x29, 0xa3, 0x2f, 0x35, 0x3b, 0x41, 0x47, 0x4d]),
    (0xF4677E, 0xE44A52, [0x00, 0x34, 0x06, 0x0c, 0x12, 0x18, 0x1e, 0x24, 0x34, 0x2a, 0x34]),
    (0xFE137D, 0xEE8F06, [0x00, 0x0f, 0x1e, 0x2d, 0x3b, 0x49, 0x57, 0x65, 0x73, 0x81, 0x8f, 0x9d, 0x9d, 0xab]),
    (0xFEEB06, 0xEED3C6, [0x00, 0x08, 0x12, 0x1c, 0x39, 0x40]),
    (0xFEEB97, 0xEED3D2, [0x00, 0x05, 0x0a, 0x0f, 0x2d, 0x34])):
    base_address, offsets_addr, offsets = code_test
    num_entries = len(offsets)
    addresses = read_addresses_with_16bit_offsets(base_address, offsets_addr, num_entries)
#    print(hex(base_address))
#    print(list(map(hex, addresses)))
#    print(list(map(hex, [base_address + offs for offs in offsets])))
#    print("")
    assert addresses == [base_address + offs for offs in offsets]


# Sorted by base_addr:
read_jump_table(called_from=0xFCD4ED, base_addr=0xEE10D0, num_entries=8)
read_jump_table(called_from=0xFDA068, base_addr=0xEE304C, num_entries=192)
read_jump_table(called_from=0xFDA254, base_addr=0xEE4F52, num_entries=24)  # FIXME: Not sure if the length is validated.
                                                                           #        The 24 first entries seem reasonable, though. Potential overflow.

# a few other routines with no limit checking, for the same jump table:
read_jump_table(called_from=0xFDA09F, base_addr=0xEE4F52, num_entries=0)
read_jump_table(called_from=0xFDA0D3, base_addr=0xEE4F52, num_entries=0)
read_jump_table(called_from=0xFDA107, base_addr=0xEE4F52, num_entries=0)
read_jump_table(called_from=0xFDA13B, base_addr=0xEE4F52, num_entries=0)
read_jump_table(called_from=0xFDA16F, base_addr=0xEE4F52, num_entries=0)
read_jump_table(called_from=0xFDA1A3, base_addr=0xEE4F52, num_entries=0)
read_jump_table(called_from=0xFDA1E9, base_addr=0xEE4F52, num_entries=0)
read_jump_table(called_from=0xFDA7F5, base_addr=0xEE4F52, num_entries=0)

read_jump_table(called_from=0xFDDEDA, base_addr=0xEE8CF4, num_entries=32)    # Code does not seem to check limits of this table.
                                                                             # Also, it forbids address 0xFDECEF even though it
                                                                             # is not present in the table.
read_jump_table(called_from=0xFDE007, base_addr=0xEE8CF4, num_entries=32)  # This routine seems to be able to index up to 256 without checking limits :-O
                                                                           # Potential overflow to run arbitrary code in low-RAM addresses
                                                                           # if variable 0x8D34 is ever set to more than 0x1F
read_jump_table(called_from=0xEF0D64, base_addr=0xEF0D64, num_entries=3)
read_jump_table(called_from=0xEF0DA5, base_addr=0xEF0DA5, num_entries=16)
read_jump_table(called_from=0xEF3638, base_addr=0xEFA361, num_entries=5)
read_jump_table(called_from=0xEFA35C, base_addr=0xEFA361, num_entries=5)
read_jump_table(called_from=0xFE8C34, base_addr=0xEEAE04, num_entries=16)  # Code does not seem to check limits of this table.
read_jump_table(called_from=0xEF05C2, base_addr=0xFC3E65, num_entries=1)  # A single entry ?! (looks like a longer, 4-entries table)
read_jump_table(called_from=0xFC44EC, base_addr=0xFC4489, num_entries=0)  # FIXME: indexed by variable at 0x8D8A
                                                                          # unknown table-length (maybe 128 entries?), potential overflow
read_jump_table(called_from=0xFC44CA, base_addr=0xFC4489, num_entries=11)
read_jump_table(called_from=0xFC4963, base_addr=0xFC4965, num_entries=8)
read_jump_table(called_from=0xFCADA0, base_addr=0xFCADA3, num_entries=8)  # Note: fcb40b, fcadc3, fcb001, fcadd4, fcb44e
read_jump_table(called_from=0xFCB46E, base_addr=0xFCB46F, num_entries=8)
read_jump_table(called_from=0xFCB6F9, base_addr=0xFCB6F9, num_entries=4)
read_jump_table(called_from=0xFCF760, base_addr=0xFCF761, num_entries=8)
read_jump_table(called_from=0xFD058A, base_addr=0xFD175E, num_entries=192)

register_jump_table_addresses(called_from=0xFAA49B, addresses=[0xF6A95E,   # TODO: review this.
                                                               0xF6A975,   # There may be more routines that call
                                                               0xF6A98C])  # this one providing different addresses.

# Sorted by offsets_addr:
read_jump_table_16bit_offsets(called_from=0xEF4784, base_addr=0xEF4784, offsets_addr=0xE00178, num_entries=8)
read_jump_table_16bit_offsets(called_from=0xF46524, base_addr=0xF46524, offsets_addr=0xE44A42, num_entries=8)
read_jump_table_16bit_offsets(called_from=0xF4677E, base_addr=0xF4677E, offsets_addr=0xE44A52, num_entries=11)
read_jump_table_16bit_offsets(called_from=0xF4670F, base_addr=0xF4670F, offsets_addr=0xE44A6A, num_entries=15)
read_jump_table_16bit_offsets(called_from=0xF96DD6, base_addr=0xF96DD6, offsets_addr=0xEA98B2, num_entries=12)
read_jump_table_16bit_offsets(called_from=0xFE137D, base_addr=0xFE137D, offsets_addr=0xEE8F06, num_entries=14)
read_jump_table_16bit_offsets(called_from=0xFEEB06, base_addr=0xFEEB06, offsets_addr=0xEED3C6, num_entries=6)
read_jump_table_16bit_offsets(called_from=0xFEEB97, base_addr=0xFEEB97, offsets_addr=0xEED3D2, num_entries=6)
# TODO: called_from=0xFB15DE (routine starts at 0xFB15C9).  This one reads the offsets_addr from stack
#       and I was not yet able to find which code calls this routine in order to see what can be placed on the stack.

read_symbols(0xAEBB2, 0xBC)
# read_symbols(0xAFA6E, 0xB0)


def read_32bit():
    value = ord(rom.read(1))
    value = ord(rom.read(1)) << 8 | value
    value = ord(rom.read(1)) << 16 | value
    value = ord(rom.read(1)) << 24 | value
    return value

def read_string(address):
    rom.seek(address & 0x1FFFFF)
    the_string = ""
    while True:
        c = rom.read(1)
        if ord(c) != 0:
            the_string += c.decode("utf8")
        else:
            return the_string


def read_some_table(address):
    """
       Starting at 0x00eac9ee, ending at 0x00ead43e ()
       NULL-terminated array of 24 byte entries:

       [...]

       0x00ead402 -> 0x00ead456: "IvIntWelcome"
       0x00ead406 -> 0x00ead454: (0x00 0xFF)
       0x00ead40a -> 0x00eac9d8 -> 0x00eac9dc: (0x00 0xFF)   # Are these null strings?

       0x00ead40e -> 0x00f9c5fc (routine pointer?)
       0x00ead412 -> 0x01600010
       0x00ead416 -> 0x0004001a
       0x00ead41a -> 0x00ead440: "VwUserBitmapByName"
       0x00ead41e -> 0x00ead43e: "X"
       0x00ead422 -> 0x00eac9de -> 0x00eac9e8: "file"

       0x00ead426 -> 0x00000000
       0x00ead42a -> 0x00000000
       0x00ead42e -> 0x00000000
       0x00ead432 -> 0x00000000
       0x00ead436 -> 0x00000000
       0x00ead43a -> 0x00000000
    """
    global entry_points
    n = 0
    while True:
        rom.seek((address & 0x1FFFFF) + n*24)
        routine_address = read_32bit()
        unknown1 = read_32bit()
        unknown2 = read_32bit()
        name1 = read_32bit()
        name2 = read_32bit()
        name3 = read_32bit()

        if routine_address == 0 and \
           unknown1 == 0 and \
           unknown2 == 0 and \
           name1 == 0 and \
           name2 == 0 and \
           name3 == 0:
            break

        name1 = read_string(name1)
        name2 = read_string(name2)

        rom.seek(name3 & 0x1FFFFF)
        name3 = read_string(read_32bit())
        print(f"{n}: '0x{routine_address:08X}' '{name1}' '{name2}' '{name3}'")
        n += 1

        KNOWN_LABELS[routine_address] = name1
        if routine_address not in entry_points:
            entry_points.append(routine_address)


read_some_table(0x00eac9ee)
rom.close()


# TODO: use jump_table_from on the ExecTrace class
#       to not report jump tables that were already documented

trace = TLCS900H_Trace(rom_file,
                       relocation_blocks=RELOCATION_BLOCKS,
                       subroutines=POSSIBLY_UNUSED_CODEBLOCKS.copy(),
                       labels=KNOWN_LABELS.copy(),
                       loglevel=0)
trace.jump_table_from = jump_table_from
trace.count_warns = 0
trace.load_interrupt_vector()
trace.run(entry_points)
for ep in entry_points:
    trace.register_label(ep)
#trace.print_ranges()
#trace.print_grouped_ranges()

total = len(jump_table_from) + trace.count_warns
progress = len(jump_table_from) / total
print(f"Inspected {len(jump_table_from)} documented jump tables emitting {trace.count_warns} warnings.")
print(f"There are at least {len(jump_table_from) + trace.count_warns} jump tables.")
print(f"Current documentation progress: {100*progress:.2f}%")

trace.save_disassembly_listing(f"{rom_file}.asm")

