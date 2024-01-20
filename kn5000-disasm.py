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
disasm_version10 = True

POSSIBLY_UNUSED_CODEBLOCKS = {}
KNOWN_LABELS = {}

parse_interrupt_table = True
RELOCATION_BLOCKS = (
    # physical,  logical, length 
    (0x000000,  0xe00000, 0x200000),
)

entry_points = []
jump_table_from = []

rom = open(rom_file, "rb")

def read_n_symbols(base_addr, num_symbols):
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


def read_some_symbols(base_addr, prefix="table"):
    global entry_points
    print(f"Reading some symbols from address 0x{base_addr:08X}...")
    rom.seek(base_addr)
    pointers = []
    address = -1
    while True:
        address = ord(rom.read(1))
        address = ord(rom.read(1)) << 8 | address
        address = ord(rom.read(1)) << 16 | address
        address = ord(rom.read(1)) << 24 | address
        if address == 0:
            break
        else:
            pointers.append(address)

    num_symbols = len(pointers)
    print(f"num_symbols: {num_symbols}")

    other_pointers = []
    while len(other_pointers) < num_symbols+1:
        address = ord(rom.read(1))
        address = ord(rom.read(1)) << 8 | address
        address = ord(rom.read(1)) << 16 | address
        address = ord(rom.read(1)) << 24 | address
        other_pointers.append(address)

    num_other_pointers = len(other_pointers)
    print(f"num_other_pointers: {num_other_pointers}")

    if ord(rom.read(1)) != 0x00:
        print("should be 0x00")
        sys.exit(hex(rom.tell()))

    if ord(rom.read(1)) != 0xFF:
        print("should be 0xFF")
        sys.exit(hex(rom.tell()))

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

    assert len(symbol_names) == len(pointers)
    assert len(symbol_names) == len(other_pointers) - 1

    symbol_names = list(reversed(symbol_names))
    for i in range(num_symbols):
        print(f"Func {prefix}[{4*i:04X}]: {pointers[i]:06X} / {other_pointers[i]:06X} - {symbol_names[i]}")

        KNOWN_LABELS[pointers[i]] = symbol_names[i]
        if pointers[i] not in entry_points:
            entry_points.append(pointers[i])


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

    if called_from:
        if called_from not in jump_table_from:
            jump_table_from.append(called_from)
    else:
        for address in addresses:
            print(f"TODO: FIX THIS HACK: {hex(address)} is an additional entry-point lacking documentation of who calls it!")

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

if disasm_version10:
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


if disasm_version10:
    # TODO: add this feature to ExecTrace:
    VARIABLE_NAMES = {
        0x043C00: "Offscreen_Video_Buffer",
    }

    KNOWN_LABELS = {
        #0xE83DF8: "Start_Internal_Demo", # TODO: I am not sure about this one, yet!
        0xEF04A1: "DRAM_related_short_pause",
        0xEF04AC: "DRAM_related_short_pause_2",
        0xEF0536: "We_seem_to_be_running_boot_ROM_code",
        0xEF083E: "Detect_Area_Region_Code",
        0xEF0865: "Get_Area_Region_Code",
        0xEF0B46: "Seems_to_copy_some_data_buffers",
        0xEF18D7: "Copy_DE_words_from_XBC_to_XWA",
        0xEF18E0: "Fill_memory_at_XWA_with_DE_words_of_BC_value",
        0xEF23E8: "Start_8bit_Timer_3",
        0xEF23EC: "Stop_and_Clear_8bit_Timer_3",
        0xEF4B6B: "Infinite_Loop_at_EF4B6B", # Why?
        0xEF5088: "Set_XWA_to_320_times_XDE",
        0xEF5141: "Write_VGA_Register",
        0xEF5157: "Read_VGA_Register",
        0xEF55A7: "Some_VGA_setup",
        0xF74942: "Draw_keybed_maybe_for_indicating_split_point",
        0xF98001: "Check_for_Floppy_Disk_Change",
        0xF98009: "Detected_Floppy_Disk_Change",
        0xFB729E: "MainCPU_self_test_routines",
        0xFB72EA: "Report_test_result_by_blinking_LED",
        0xFB7348: "Test_DRAM_IC10_and_IC9",
        0xFB7400: "Test_SRAM_IC21",
        0xFB7328: "A_Short_Pause", # for how long?
        0xFB7456: "Test_PROGRAM_and_TABLE_DATA_ROMs",
            # Note:
            # PROGRAM ROMs: IC6/IC4
            # TABLE DATA ROMs: IC3/IC1
        0xFB7561: "Test_Rhythm_data_ROM_IC14", #  (first 4 bytes at 0x0040_0000
                                               #   must be “0x00, 0x01, 0x04, 0x05”)
        0xFB75D4: "Test_Custom_data_ROM_IC19",
        0xFB763A: "Test_LCD_Controller_IC206",
        0xFB7687: "Test_Video_RAM_IC207",
        0xFFFEE5: "Get_Firmware_Version",
    }

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

    read_some_symbols(0x0d72e)
    read_some_symbols(0x16284)
    read_some_symbols(0x1CA6E)
    read_some_symbols(0x1F0EC, "0xE88") # <-- These are the "0xE88-table" routines also called by HD-AE5000 ROM. See details below. 
    read_some_symbols(0x1FD2C)
    read_some_symbols(0x20260)
    read_some_symbols(0x25042)
    read_some_symbols(0x26804)
    read_some_symbols(0x3051C)
    read_some_symbols(0x55210)
    read_some_symbols(0x55DAE)
    read_some_symbols(0x5AD8C)
    read_some_symbols(0x8070A)
    read_some_symbols(0x814F4)
    read_some_symbols(0x86638)
    read_some_symbols(0xA0A56)
    read_some_symbols(0xA135A)
    read_some_symbols(0xA7FCE)
    read_some_symbols(0xAB2B4)
    read_some_symbols(0xAFA6E, "0xE0A") # <-- There are the "0xE0A-table" routines.
                               # 
                               # These functions are used by the HD-AE5000 ROM
                               # The table is copied to SRAM and then used like this:
                               # 	LD XWA (0x23D2DE)
                               # 	LD XWA (XWA + 0x0e0a)  <--- 0x0e0a is the offset within the data block copied to SRAM that corresponds to the array of func pointers 
                               # 	LD XHL (XWA + 0x00e4)  <--- 0xe4 here is the index. Get the Nth function pointer by passing 4*N here.
                               # 	LD WA, 0x01ea  <--- some parameter for the function call
                               # 	CALL T XHL
                               #
                               # Function number 0xE4, for instance, is "RegisterObjectTable"

    read_some_symbols(0xB3698)
    read_some_symbols(0xD1C9E)
    read_some_symbols(0xD2F66)
    read_some_symbols(0xD3292)

    # Experimental: read_n_symbols(0xAEBB2, 0xBC)

    ## register_jump_table_addresses(called_from=None, addresses=[0xF6EFEC])
    ## trying to find who calls the save-user-settings-to-floppy backup routine.
    ## TODO: Study routine LABEL_F6E7F8

    # These 19 base_addresses are in a list at 0xEE8C7E:
    for b in [0xEF1235, 0xEED52B, 0xE1FFB6, 0xFCF962,
              0xEE2F26, 0xEE1574, 0xEDB2E4, 0xEA066C,
              0xEB7932, 0xEDA02C, 0xED9D1E, 0xEED3DE,
              0xE44636, 0xF532A1, 0xF6F068, 0xF5E907,
              0xEED57D, 0xE9FCE2, 0xEEC288]:
        read_jump_table(called_from=0xFDDB79, base_addr=b, num_entries=4) # Among all invokations of routine at LABEL_FDDB46,
                                                                          # the only values passed via WA register are 0,1,2 or 3.
                                                                          # So, this means each of these small jump-tables have exactly 4 entries.

    # Experimental:
    # read_some_table(0xEAC9EE)



rom.close()

# These are manually detected routines (or subroutines) found while looking for calls
# to Get_Firmware_Version, investigating how the SOFT_VERSION screen is drawn
# so that we may figure out where the internal version numbers of
# MAIN PROGRAM, MAIN TABLE, SUB PROGRAM and SOUND TABLE are stored.
# By finding that we may also figure out where the SUBCPU program code may be stored.

if disasm_version10:
    MANUALLY_FOUND = [
        0xF5E985,
    ]
    for pointer in MANUALLY_FOUND:
        if pointer not in entry_points:
            entry_points.append(pointer)


# These are the ones to which we already attibuted meaningful routine names:
for pointer, label in KNOWN_LABELS.items():
    if pointer not in entry_points:
        entry_points.append(pointer)


# TODO: use jump_table_from on the ExecTrace class
#       to not report jump tables that were already documented

trace = TLCS900H_Trace(rom_file,
                       relocation_blocks=RELOCATION_BLOCKS,
                       subroutines=POSSIBLY_UNUSED_CODEBLOCKS.copy(),
                       labels=KNOWN_LABELS.copy(),
                       loglevel=0)
trace.jump_table_from = jump_table_from
trace.count_warns = 0

if parse_interrupt_table:
    trace.load_interrupt_vector()

trace.run(entry_points)
for ep in entry_points:
    trace.register_label(ep)
#trace.print_ranges()
#trace.print_grouped_ranges()

total = len(jump_table_from) + trace.count_warns
if total > 0:
    progress = len(jump_table_from) / total
    print(f"Inspected {len(jump_table_from)} documented jump tables emitting {trace.count_warns} warnings.")
    print(f"There are at least {len(jump_table_from) + trace.count_warns} jump tables.")
    print(f"Current documentation progress: {100*progress:.2f}%")

trace.save_disassembly_listing(f"{rom_file}.asm")

