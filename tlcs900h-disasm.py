#!/usr/bin/env python3
#
# (c) 2022 Felipe Correa da Silva Sanches <juca@members.fsf.org>
# Licensed under GPL version 3 or later

import os
import sys
from exectrace import ExecTrace

# tmp94c241
SFR_names = [
    # TLCS-900/H2 type 8 bit I/O:
    "P0",      "0x01",    "P0CR",    "P0FC",    "P1",      "0x05",    "P1CR",    "P1FC",
    "P2",      "0x09",    "P2CR",    "P2FC",    "P3",      "0x0d",    "P3CR",    "P3FC",
    "P4",      "0x11",    "P4CR",    "P4FC",    "P5",      "0x15",    "P5CR",    "P5FC",
    "P6",      "0x19",    "P6CR",    "P6FC",    "P7",      "0x1d",    "P7CR",    "P7FC",
    "P8",      "0x21",    "P8CR",    "P8FC",    "0x24",    "0x25",    "0x26",    "0x27",
    "PA",      "0x29",    "0x2a",    "PAFC",    "PB",      "0x2d",    "0x2e",    "PBFC",
    "PC",      "0x31",    "PCCR",    "PCFC",    "PD",      "0x35",    "PDCR",    "PDFC",
    "PE",      "0x39",    "PECR",    "PEFC",    "PF",      "0x3d",    "PFCR",    "PFFC",
    "PG",      "0x41",    "0x42",    "0x43",    "PH",      "0x45",    "PHCR",    "PHFC",
    "0x48",    "0x49",    "0x4a",    "0x4b",    "0x4c",    "0x4d",    "0x4e",    "0x4f",
    "0x50",    "0x51",    "0x52",    "0x53",    "0x54",    "0x55",    "0x56",    "0x57",
    "0x58",    "0x59",    "0x5a",    "0x5b",    "0x5c",    "0x5d",    "0x5e",    "0x5f",
    "0x60",    "0x61",    "0x62",    "0x63",    "0x64",    "0x65",    "0x66",    "0x67",
    "PZ",      "0x69",    "PZCR",    "0x6b",    "0x6c",    "0x6d",    "0x6e",    "0x6f",
    "0x70",    "0x71",    "0x72",    "0x73",    "0x74",    "0x75",    "0x76",    "0x77",
    "0x78",    "0x79",    "0x7a",    "0x7b",    "0x7c",    "0x7d",    "0x7e",    "0x7f",

    # TLCS-90 type I/O:
    "T8RUN",   "TRDC",    "T02FFCR", "0x83",    "T01MOD",  "T23MOD",  "0x86",    "0x87",
    "TREG0",   "TREG1",   "TREG2",   "TREG3",   "0x8c",    "0x8d",    "0x8e",    "0x8f",
    "TREG4L",  "TREG4H",  "TREG5L",  "TREG5H",  "CAP4L",   "CAP4H",   "CAP5L",   "CAP5H",
    "T4MOD",   "T4FFCR",  "0x9a",    "0x9b",    "0x9c",    "0x9d",    "T16RUN",  "T16CR",
    "TREG6L",  "TREG6H",  "TREG7L",  "TREG7H",  "CAP6L",   "CAP6H",   "CAP7L",   "CAP7H",
    "T6MOD",   "T6FFCR",  "0xaa",    "0xab",    "0xac",    "0xad",    "0xae",    "0xaf",
    "TREG8L",  "TREG8H",  "TREG9L",  "TREG9H",  "CAP8L",   "CAP8H",   "CAP9L",   "CAP9H",
    "T8MOD",   "T8FFCR",  "0xba",    "0xbb",    "0xbc",    "0xbd",    "0xbe",    "0xbf",
    "TREGAL",  "TREGAH",  "TREGBL",  "TREGBH",  "CAPAL",   "CAPAH",   "CAPBL",   "CAPBH",
    "TAMOD",   "TAFFCR",  "0xca",    "0xcb",    "0xcc",    "0xcd",    "0xce",    "0xcf",
    "SC0BUF",  "SC0CR",   "SC0MOD",  "BR0CR",   "SC1BUF",  "SC1CR",   "SC1MOD",  "BR1CR",
    "0xd8",    "0xd9",    "0xda",    "0xdb",    "0xdc",    "0xdd",    "0xde",    "0xdf",

    # TLCS-900/H2 type 8 bit I/O:
    "INTE45",  "INTE67",  "INTE89",  "INTEAB",  "INTET01", "INTET23", "INTET45", "INTET67",
    "INTET89", "INTETAB", "INTES0",  "INTES1",  "INTETC01","INTETC23","INTETC45","INTETC67",
    "INTE0AD", "0xf1",    "0xf2",    "0xf3",    "0xf4",    "0xf5",    "IIMC",    "INTNMWDT",
    "INTCLR",  "0xf9",    "0xfa",    "0xfb",    "0xfc",    "0xfd",    "0xfe",    "0xff",
    "DMA0V",   "DMA1V",   "DMA2V" ,  "DMA3V",   "DMA4V",   "DMA5V",   "DMA6V",   "DMA7V",
    "DMAB",    "DMAR",    "CLKMOD" , "0x10b",   "0x10c",   "0x10d",   "0x10e",   "0x10f",

    # TLCS-90 type I/O:
    "WDMOD",   "WDCR",    "0x112" ,  "0x113",   "0x114",   "0x115",   "0x116",   "0x117",
    "0x118",   "0x119",   "0x11a",   "0x11b",   "0x11c",   "0x11d",   "0x11e",   "0x11f",
    "ADREG04L","ADREG04H","ADREG15L","ADREG15H","ADREG26L","ADREG26H","ADREG37L","ADREG37H",
    "ADMOD1",  "ADMOD2",  "0x12a",   "0x12b",   "0x12c",   "0x12d",   "0x12e",   "0x12f",
    "DAREG0",  "DAREG1",  "DADRV",   "0x133",   "0x134",   "0x135",   "0x136",   "0x137",
    "0x138",   "0x139",   "0x13a",   "0x13b",   "0x13c",   "0x13d",   "0x13e",   "0x13f",

    # TLCS-900/H2 type 8 bit I/O:
    "B0CSL",   "B0CSH",   "MAMR0",   "MSAR0",   "B1CSL",   "B1CSH",   "MAMR1",   "MSAR1",
    "B2CSL",   "B2CSH",   "MAMR2",   "MSAR2",   "B3CSL",   "B3CSH",   "MAMR3",   "MSAR3",
    "B4CSL",   "B4CSH",   "MAMR4",   "MSAR4",   "B5CSL",   "B5CSH",   "MAMR5",   "MSAR5",
    "0x158",   "0x159",   "0x15a",   "0x15b",   "0x15c",   "0x15d",   "0x15e",   "0x15f",
    "DRAM0CRL","DRAM0CRH","DRAM1CRL","DRAM1CRH","DRAM0REF","DRAM1REF","PMEMCR",  "0x167",
    "0x168",   "0x169",   "0x16a",   "0x16b",   "0x16c",   "0x16d",   "0x16e",   "0x16f",
]

SPECIAL_PURPOSE_VARS = {}
for n, name in enumerate(SFR_names):
    if not name.startswith("0x"):
        SPECIAL_PURPOSE_VARS[n] = name


def format_hex_value(value):
    if isinstance(value, int):
        if value <= 0xff:
            value = "0x%02X" % value
        elif value <= 0xffff:
            value = "0x%04X" % value
        elif value <= 0xffffff:
            value = "0x%06X" % value
        else:
            value = "0x%08X" % value
    return value


def getVariableName(value):
    if value in SPECIAL_PURPOSE_VARS.keys():
        return SPECIAL_PURPOSE_VARS[value]
    else:
        return format_hex_value(value)


instructions = [
    # 00 - 1F
    ["NOP", None, None], ["NORMAL", None, None], ["PUSH", "O_SR", None], ["POP", "O_SR", None],
    ["MAX", None, None], ["HALT", None, None], ["EI", "O_I8", None], ["RETI", None, None],
    ["LD", "O_M8", "O_I8"], ["PUSH", "O_I8", None], ["LD", "O_M8", "O_I16"], ["PUSH", "O_I16", None],
    ["INCF", None, None], ["DECF", None, None], ["RET", None, None], ["RETD", "O_I16", None],
    ["RCF", None, None], ["SCF", None, None], ["CCF", None, None], ["ZCF", None, None],
    ["PUSH", "O_A", None], ["POP", "O_A", None], ["EX", "O_F", "O_F"], ["LDF", "O_I8", None],
    ["PUSH", "O_F", None], ["POP", "O_F", None], ["JP", "O_I16", None], ["JP", "O_I24", None],
    ["CALL", "O_I16", None], ["CALL", "O_I24", None], ["CALR", "O_D16", None], ["DB", None, None],

    # 20 - 3F
    ["LD", "O_C8", "O_I8"], ["LD", "O_C8", "O_I8"], ["LD", "O_C8", "O_I8"], ["LD", "O_C8", "O_I8"],
    ["LD", "O_C8", "O_I8"], ["LD", "O_C8", "O_I8"], ["LD", "O_C8", "O_I8"], ["LD", "O_C8", "O_I8"],
    ["PUSH", "O_C16", None], ["PUSH", "O_C16", None], ["PUSH", "O_C16", None], ["PUSH", "O_C16", None],
    ["PUSH", "O_C16", None], ["PUSH", "O_C16", None], ["PUSH", "O_C16", None], ["PUSH", "O_C16", None],
    ["LD", "O_C16", "O_I16"], ["LD", "O_C16", "O_I16"], ["LD", "O_C16", "O_I16"], ["LD", "O_C16", "O_I16"],
    ["LD", "O_C16", "O_I16"], ["LD", "O_C16", "O_I16"], ["LD", "O_C16", "O_I16"], ["LD", "O_C16", "O_I16"],
    ["PUSH", "O_C32", None], ["PUSH", "O_C32", None], ["PUSH", "O_C32", None], ["PUSH", "O_C32", None],
    ["PUSH", "O_C32", None], ["PUSH", "O_C32", None], ["PUSH", "O_C32", None], ["PUSH", "O_C32", None],

    # 40 - 5F
    ["LD", "O_C32", "O_I32"], ["LD", "O_C32", "O_I32"], ["LD", "O_C32", "O_I32"], ["LD", "O_C32", "O_I32"],
    ["LD", "O_C32", "O_I32"], ["LD", "O_C32", "O_I32"], ["LD", "O_C32", "O_I32"], ["LD", "O_C32", "O_I32"],
    ["POP", "O_C16", None], ["POP", "O_C16", None], ["POP", "O_C16", None], ["POP", "O_C16", None],
    ["POP", "O_C16", None], ["POP", "O_C16", None], ["POP", "O_C16", None], ["POP", "O_C16", None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["POP", "O_C32", None], ["POP", "O_C32", None], ["POP", "O_C32", None], ["POP", "O_C32", None],
    ["POP", "O_C32", None], ["POP", "O_C32", None], ["POP", "O_C32", None], ["POP", "O_C32", None],

    # 60 - 7F
    ["JR", "O_CC", "O_D8"], ["JR", "O_CC", "O_D8"], ["JR", "O_CC", "O_D8"], ["JR", "O_CC", "O_D8"],
    ["JR", "O_CC", "O_D8"], ["JR", "O_CC", "O_D8"], ["JR", "O_CC", "O_D8"], ["JR", "O_CC", "O_D8"],
    ["JR", "O_CC", "O_D8"], ["JR", "O_CC", "O_D8"], ["JR", "O_CC", "O_D8"], ["JR", "O_CC", "O_D8"],
    ["JR", "O_CC", "O_D8"], ["JR", "O_CC", "O_D8"], ["JR", "O_CC", "O_D8"], ["JR", "O_CC", "O_D8"],
    ["JRL", "O_CC", "O_D16"], ["JRL", "O_CC", "O_D16"], ["JRL", "O_CC", "O_D16"], ["JRL", "O_CC", "O_D16"],
    ["JRL", "O_CC", "O_D16"], ["JRL", "O_CC", "O_D16"], ["JRL", "O_CC", "O_D16"], ["JRL", "O_CC", "O_D16"],
    ["JRL", "O_CC", "O_D16"], ["JRL", "O_CC", "O_D16"], ["JRL", "O_CC", "O_D16"], ["JRL", "O_CC", "O_D16"],
    ["JRL", "O_CC", "O_D16"], ["JRL", "O_CC", "O_D16"], ["JRL", "O_CC", "O_D16"], ["JRL", "O_CC", "O_D16"],

    # 80 - 9F
    ["M_80", None, None], ["M_80", None, None], ["M_80", None, None], ["M_80", None, None],
    ["M_80", None, None], ["M_80", None, None], ["M_80", None, None], ["M_80", None, None],
    ["M_88", None, None], ["M_88", None, None], ["M_88", None, None], ["M_88", None, None],
    ["M_88", None, None], ["M_88", None, None], ["M_88", None, None], ["M_88", None, None],
    ["M_90", None, None], ["M_90", None, None], ["M_90", None, None], ["M_90", None, None],
    ["M_90", None, None], ["M_90", None, None], ["M_90", None, None], ["M_90", None, None],
    ["M_98", None, None], ["M_98", None, None], ["M_98", None, None], ["M_98", None, None],
    ["M_98", None, None], ["M_98", None, None], ["M_98", None, None], ["M_98", None, None],

    # A0 - BF
    ["M_A0", None, None], ["M_A0", None, None], ["M_A0", None, None], ["M_A0", None, None],
    ["M_A0", None, None], ["M_A0", None, None], ["M_A0", None, None], ["M_A0", None, None],
    ["M_A8", None, None], ["M_A8", None, None], ["M_A8", None, None], ["M_A8", None, None],
    ["M_A8", None, None], ["M_A8", None, None], ["M_A8", None, None], ["M_A8", None, None],
    ["M_B0", None, None], ["M_B0", None, None], ["M_B0", None, None], ["M_B0", None, None],
    ["M_B0", None, None], ["M_B0", None, None], ["M_B0", None, None], ["M_B0", None, None],
    ["M_B8", None, None], ["M_B8", None, None], ["M_B8", None, None], ["M_B8", None, None],
    ["M_B8", None, None], ["M_B8", None, None], ["M_B8", None, None], ["M_B8", None, None],

    # C0 - DF
    ["M_C0", None, None], ["M_C0", None, None], ["M_C0", None, None], ["M_C0", None, None],
    ["M_C0", None, None], ["M_C0", None, None], ["DB", None, None], ["oC8", None, None],
    ["oC8", None, None], ["oC8", None, None], ["oC8", None, None], ["oC8", None, None],
    ["oC8", None, None], ["oC8", None, None], ["oC8", None, None], ["oC8", None, None],
    ["M_D0", None, None], ["M_D0", None, None], ["M_D0", None, None], ["M_D0", None, None],
    ["M_D0", None, None], ["M_D0", None, None], ["DB", None, None], ["oD8", None, None],
    ["oD8", None, None], ["oD8", None, None], ["oD8", None, None], ["oD8", None, None],
    ["oD8", None, None], ["oD8", None, None], ["oD8", None, None], ["oD8", None, None],

    # E0 - FF
    ["M_E0", None, None], ["M_E0", None, None], ["M_E0", None, None], ["M_E0", None, None],
    ["M_E0", None, None], ["M_E0", None, None], ["DB", None, None], ["M_E8", None, None],
    ["M_E8", None, None], ["M_E8", None, None], ["M_E8", None, None], ["M_E8", None, None],
    ["M_E8", None, None], ["M_E8", None, None], ["M_E8", None, None], ["M_E8", None, None],
    ["M_F0", None, None], ["M_F0", None, None], ["M_F0", None, None], ["M_F0", None, None],
    ["M_F0", None, None], ["M_F0", None, None], ["DB", None, None], ["LDX", None, None],
    ["SWI", "O_I3", None], ["SWI", "O_I3", None], ["SWI", "O_I3", None], ["SWI", "O_I3", None],
    ["SWI", "O_I3", None], ["SWI", "O_I3", None], ["SWI", "O_I3", None], ["SWI", "O_I3", None]
]


mnemonic_80 = [
    # 00 - 1F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["PUSH", "O_M", None], ["DB", None, None], ["RLD", "O_A", "O_M"], ["RRD", "O_A", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["LDI", None, None], ["LDIR", None, None], ["LDD", None, None], ["LDDR", None, None],
    ["CPI", None, None], ["CPIR", None, None], ["CPD", None, None], ["CPDR", None, None],
    ["DB", None, None], ["LD", "O_M16", "O_M"], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 20 - 3F
    ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"],
    ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"],
    ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"],
    ["ADD", "O_M", "O_I8"], ["ADC", "O_M", "O_I8"], ["SUB", "O_M", "O_I8"], ["SBC", "O_M", "O_I8"],
    ["AND", "O_M", "O_I8"], ["XOR", "O_M", "O_I8"], ["OR", "O_M", "O_I8"], ["CP", "O_M", "O_I8"],

    # 40 - 5F
    ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"],
    ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"],
    ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"],
    ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"],
    ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"],
    ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"],
    ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"],
    ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"],

    # 60 - 7F
    ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"],
    ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"],
    ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"],
    ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["RLC", "O_M", None], ["RRC", "O_M", None], ["RL", "O_M", None], ["RR", "O_M", None],
    ["SLA", "O_M", None], ["SRA", "O_M", None], ["SLL", "O_M", None], ["SRL", "O_M", None],

    # 80 - 9F
    ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"],
    ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"],
    ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"],
    ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"],
    ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"],
    ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"],
    ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"],
    ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"],

    # A0 - BF
    ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"],
    ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"],
    ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"],
    ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"],
    ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"],
    ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"],
    ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"],
    ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"],

    # C0 - DF
    ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"],
    ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"],
    ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"],
    ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"],
    ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"],
    ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"],
    ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"],
    ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"],

    # E0 - FF
    ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"],
    ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"],
    ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"],
    ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"],
    ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"],
    ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"],
    ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"],
    ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"],
]


mnemonic_88 = [
    # 00 - 1F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["PUSH", "O_M", None], ["DB", None, None], ["RLD", "O_A", "O_M"], ["RRD", "O_A", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["LD", "O_M16", "O_M"], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 20 - 3F
    ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"],
    ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"],
    ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"],
    ["ADD", "O_M", "O_I8"], ["ADC", "O_M", "O_I8"], ["SUB", "O_M", "O_I8"], ["SBC", "O_M", "O_I8"],
    ["AND", "O_M", "O_I8"], ["XOR", "O_M", "O_I8"], ["OR", "O_M", "O_I8"], ["CP", "O_M", "O_I8"],

    # 40 - 5F
    ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"],
    ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"],
    ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"],
    ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"],
    ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"],
    ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"],
    ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"],
    ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"],

    # 60 - 7F
    ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"],
    ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"],
    ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"],
    ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["RLC", "O_M", None], ["RRC", "O_M", None], ["RL", "O_M", None], ["RR", "O_M", None],
    ["SLA", "O_M", None], ["SRA", "O_M", None], ["SLL", "O_M", None], ["SRL", "O_M", None],

    # 80 - 9F
    ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"],
    ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"],
    ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"],
    ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"],
    ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"],
    ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"],
    ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"],
    ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"],

    # A0 - BF
    ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"],
    ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"],
    ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"],
    ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"],
    ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"],
    ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"],
    ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"],
    ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"],

    # C0 - DF
    ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"],
    ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"],
    ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"],
    ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"],
    ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"],
    ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"],
    ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"],
    ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"],

    # E0 - FF
    ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"],
    ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"],
    ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"],
    ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"],
    ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"],
    ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"],
    ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"],
    ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"],
]

mnemonic_90 = [
    # 00 - 1F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["PUSHW", "O_M", None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["LDIW", None, None], ["LDIRW", None, None], ["LDDW", None, None], ["LDDRW", None, None],
    ["CPIW", None, None], ["CPIRW", None, None], ["CPDW", None, None], ["CPDRW", None, None],
    ["DB", None, None], ["LDW", "O_M16", "O_M"], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 20 - 3F
    ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"],
    ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"],
    ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"],
    ["ADD", "O_M", "O_I16"], ["ADC", "O_M", "O_I16"], ["SUB", "O_M", "O_I16"], ["SBC", "O_M", "O_I16"],
    ["AND", "O_M", "O_I16"], ["XOR", "O_M", "O_I16"], ["OR", "O_M", "O_I16"], ["CP", "O_M", "O_I16"],

    # 40 - 5F
    ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"],
    ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"],
    ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"],
    ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"],
    ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"],
    ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"],
    ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"],
    ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"],

    # 60 - 7F
    ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"],
    ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"],
    ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"],
    ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["RLCW", "O_M", None], ["RRCW", "O_M", None], ["RLW", "O_M", None], ["RRW", "O_M", None],
    ["SLAW", "O_M", None], ["SRAW", "O_M", None], ["SLLW", "O_M", None], ["SRLW", "O_M", None],

    # 80 - 9F
    ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"],
    ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"],
    ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"],
    ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"],
    ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"],
    ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"],
    ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"],
    ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"],

    # A0 - BF
    ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"],
    ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"],
    ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"],
    ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"],
    ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"],
    ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"],
    ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"],
    ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"],

    # C0 - DF
    ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"],
    ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"],
    ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"],
    ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"],
    ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"],
    ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"],
    ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"],
    ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"],

    # E0 - FF
    ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"],
    ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"],
    ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"],
    ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"],
    ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"],
    ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"],
    ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"],
    ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"],
]


mnemonic_98 = [
    # 00 - 1F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["PUSHW", "O_M", None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["LDW", "O_M16", "O_M"], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 20 - 3F
    ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"],
    ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"],
    ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"],
    ["ADD", "O_M", "O_I16"], ["ADC", "O_M", "O_I16"], ["SUB", "O_M", "O_I16"], ["SBC", "O_M", "O_I16"],
    ["AND", "O_M", "O_I16"], ["XOR", "O_M", "O_I16"], ["OR", "O_M", "O_I16"], ["CP", "O_M", "O_I16"],

    # 40 - 5F
    ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"],
    ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"],
    ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"],
    ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"],
    ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"],
    ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"],
    ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"],
    ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"],

    # 60 - 7F
    ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"],
    ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"],
    ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"],
    ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["RLCW", "O_M", None], ["RRCW", "O_M", None], ["RLW", "O_M", None], ["RRW", "O_M", None],
    ["SLAW", "O_M", None], ["SRAW", "O_M", None], ["SLLW", "O_M", None], ["SRLW", "O_M", None],

    # 80 - 9F
    ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"],
    ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"],
    ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"],
    ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"],
    ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"],
    ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"],
    ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"],
    ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"],

    # A0 - BF
    ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"],
    ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"],
    ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"],
    ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"],
    ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"],
    ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"],
    ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"],
    ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"],

    # C0 - DF
    ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"],
    ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"],
    ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"],
    ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"],
    ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"],
    ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"],
    ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"],
    ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"],

    # E0 - FF
    ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"],
    ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"],
    ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"],
    ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"],
    ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"],
    ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"],
    ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"],
    ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"],
]

mnemonic_a0 = [
    # 00 - 1F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 20 - 3F
    ["LD", "O_C32", "O_M"], ["LD", "O_C32", "O_M"], ["LD", "O_C32", "O_M"], ["LD", "O_C32", "O_M"],
    ["LD", "O_C32", "O_M"], ["LD", "O_C32", "O_M"], ["LD", "O_C32", "O_M"], ["LD", "O_C32", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 40 - 5F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 60 - 7F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 80 - 9F
    ["ADD", "O_C32", "O_M"], ["ADD", "O_C32", "O_M"], ["ADD", "O_C32", "O_M"], ["ADD", "O_C32", "O_M"],
    ["ADD", "O_C32", "O_M"], ["ADD", "O_C32", "O_M"], ["ADD", "O_C32", "O_M"], ["ADD", "O_C32", "O_M"],
    ["ADD", "O_M", "O_C32"], ["ADD", "O_M", "O_C32"], ["ADD", "O_M", "O_C32"], ["ADD", "O_M", "O_C32"],
    ["ADD", "O_M", "O_C32"], ["ADD", "O_M", "O_C32"], ["ADD", "O_M", "O_C32"], ["ADD", "O_M", "O_C32"],
    ["ADC", "O_C32", "O_M"], ["ADC", "O_C32", "O_M"], ["ADC", "O_C32", "O_M"], ["ADC", "O_C32", "O_M"],
    ["ADC", "O_C32", "O_M"], ["ADC", "O_C32", "O_M"], ["ADC", "O_C32", "O_M"], ["ADC", "O_C32", "O_M"],
    ["ADC", "O_M", "O_C32"], ["ADC", "O_M", "O_C32"], ["ADC", "O_M", "O_C32"], ["ADC", "O_M", "O_C32"],
    ["ADC", "O_M", "O_C32"], ["ADC", "O_M", "O_C32"], ["ADC", "O_M", "O_C32"], ["ADC", "O_M", "O_C32"],

    # A0 - BF
    ["SUB", "O_C32", "O_M"], ["SUB", "O_C32", "O_M"], ["SUB", "O_C32", "O_M"], ["SUB", "O_C32", "O_M"],
    ["SUB", "O_C32", "O_M"], ["SUB", "O_C32", "O_M"], ["SUB", "O_C32", "O_M"], ["SUB", "O_C32", "O_M"],
    ["SUB", "O_M", "O_C32"], ["SUB", "O_M", "O_C32"], ["SUB", "O_M", "O_C32"], ["SUB", "O_M", "O_C32"],
    ["SUB", "O_M", "O_C32"], ["SUB", "O_M", "O_C32"], ["SUB", "O_M", "O_C32"], ["SUB", "O_M", "O_C32"],
    ["SBC", "O_C32", "O_M"], ["SBC", "O_C32", "O_M"], ["SBC", "O_C32", "O_M"], ["SBC", "O_C32", "O_M"],
    ["SBC", "O_C32", "O_M"], ["SBC", "O_C32", "O_M"], ["SBC", "O_C32", "O_M"], ["SBC", "O_C32", "O_M"],
    ["SBC", "O_M", "O_C32"], ["SBC", "O_M", "O_C32"], ["SBC", "O_M", "O_C32"], ["SBC", "O_M", "O_C32"],
    ["SBC", "O_M", "O_C32"], ["SBC", "O_M", "O_C32"], ["SBC", "O_M", "O_C32"], ["SBC", "O_M", "O_C32"],

    # C0 - DF
    ["AND", "O_C32", "O_M"], ["AND", "O_C32", "O_M"], ["AND", "O_C32", "O_M"], ["AND", "O_C32", "O_M"],
    ["AND", "O_C32", "O_M"], ["AND", "O_C32", "O_M"], ["AND", "O_C32", "O_M"], ["AND", "O_C32", "O_M"],
    ["AND", "O_M", "O_C32"], ["AND", "O_M", "O_C32"], ["AND", "O_M", "O_C32"], ["AND", "O_M", "O_C32"],
    ["AND", "O_M", "O_C32"], ["AND", "O_M", "O_C32"], ["AND", "O_M", "O_C32"], ["AND", "O_M", "O_C32"],
    ["XOR", "O_C32", "O_M"], ["XOR", "O_C32", "O_M"], ["XOR", "O_C32", "O_M"], ["XOR", "O_C32", "O_M"],
    ["XOR", "O_C32", "O_M"], ["XOR", "O_C32", "O_M"], ["XOR", "O_C32", "O_M"], ["XOR", "O_C32", "O_M"],
    ["XOR", "O_M", "O_C32"], ["XOR", "O_M", "O_C32"], ["XOR", "O_M", "O_C32"], ["XOR", "O_M", "O_C32"],
    ["XOR", "O_M", "O_C32"], ["XOR", "O_M", "O_C32"], ["XOR", "O_M", "O_C32"], ["XOR", "O_M", "O_C32"],

    # E0 - FF
    ["OR", "O_C32", "O_M"], ["OR", "O_C32", "O_M"], ["OR", "O_C32", "O_M"], ["OR", "O_C32", "O_M"],
    ["OR", "O_C32", "O_M"], ["OR", "O_C32", "O_M"], ["OR", "O_C32", "O_M"], ["OR", "O_C32", "O_M"],
    ["OR", "O_M", "O_C32"], ["OR", "O_M", "O_C32"], ["OR", "O_M", "O_C32"], ["OR", "O_M", "O_C32"],
    ["OR", "O_M", "O_C32"], ["OR", "O_M", "O_C32"], ["OR", "O_M", "O_C32"], ["OR", "O_M", "O_C32"],
    ["CP", "O_C32", "O_M"], ["CP", "O_C32", "O_M"], ["CP", "O_C32", "O_M"], ["CP", "O_C32", "O_M"],
    ["CP", "O_C32", "O_M"], ["CP", "O_C32", "O_M"], ["CP", "O_C32", "O_M"], ["CP", "O_C32", "O_M"],
    ["CP", "O_M", "O_C32"], ["CP", "O_M", "O_C32"], ["CP", "O_M", "O_C32"], ["CP", "O_M", "O_C32"],
    ["CP", "O_M", "O_C32"], ["CP", "O_M", "O_C32"], ["CP", "O_M", "O_C32"], ["CP", "O_M", "O_C32"]
]


mnemonic_b0 = [
    # 00 - 1F
    ["LD", "O_M", "O_I8"], ["DB", None, None], ["LD", "O_M", "O_I16"], ["DB", None, None],
    ["POP", "O_M", None], ["DB", None, None], ["POPW", "O_M", None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["LD", "O_M", "O_M16"], ["DB", None, None], ["LDW", "O_M", "O_M16"], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 20 - 3F
    ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"],
    ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"],
    ["ANDCF", "O_A", "O_M"], ["ORCF", "O_A", "O_M"], ["XORCF", "O_A", "O_M"], ["LDCF", "O_A", "O_M"],
    ["STCF", "O_A", "O_M"], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"],
    ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 40 - 5F
    ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"],
    ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"],
    ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 60 - 7F
    ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"],
    ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 80 - 9F
    ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"],
    ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"],
    ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"],
    ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"],
    ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"],
    ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"],
    ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"],
    ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"],

    # A0 - BF
    ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"],
    ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"],
    ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"],
    ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"],
    ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"],
    ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"],
    ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"],
    ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"],

    # C0 - DF
    ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"],
    ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"],
    ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"],
    ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"],
    ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"],
    ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"],
    ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"],
    ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"],

    # E0 - FF
    ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"],
    ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"],
    ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"],
    ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"],
    ["RET", "O_CC", None], ["RET", "O_CC", None], ["RET", "O_CC", None], ["RET", "O_CC", None],
    ["RET", "O_CC", None], ["RET", "O_CC", None], ["RET", "O_CC", None], ["RET", "O_CC", None],
    ["RET", "O_CC", None], ["RET", "O_CC", None], ["RET", "O_CC", None], ["RET", "O_CC", None],
    ["RET", "O_CC", None], ["RET", "O_CC", None], ["RET", "O_CC", None], ["RET", "O_CC", None],
]


mnemonic_b8 = [
    # 00 - 1F
    ["LD", "O_M", "O_I8"], ["DB", None, None], ["LD", "O_M", "O_I16"], ["DB", None, None],
    ["POP", "O_M", None], ["DB", None, None], ["POPW", "O_M", None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["LD", "O_M", "O_M16"], ["DB", None, None], ["LDW", "O_M", "O_M16"], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 20 - 3F
    ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"],
    ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"],
    ["ANDCF", "O_A", "O_M"], ["ORCF", "O_A", "O_M"], ["XORCF", "O_A", "O_M"], ["LDCF", "O_A", "O_M"],
    ["STCF", "O_A", "O_M"], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"],
    ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 40 - 5F
    ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"],
    ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"],
    ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 60 - 7F
    ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"],
    ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 80 - 9F
    ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"],
    ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"],
    ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"],
    ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"],
    ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"],
    ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"],
    ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"],
    ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"],

    # A0 - BF
    ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"],
    ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"],
    ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"],
    ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"],
    ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"],
    ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"],
    ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"],
    ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"],

    # C0 - DF
    ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"],
    ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"],
    ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"],
    ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"],
    ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"],
    ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"],
    ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"],
    ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"],

    # E0 - FF
    ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"],
    ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"],
    ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"],
    ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
]

mnemonic_c0 = [
    # 00 - 1F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["PUSH", "O_M", None], ["DB", None, None], ["RLD", "O_A", "O_M"], ["RRD", "O_A", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["LD", "O_M16", "O_M"], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 20 - 3F
    ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"],
    ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"], ["LD", "O_C8", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"],
    ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"], ["EX", "O_M", "O_C8"],
    ["ADD", "O_M", "O_I8"], ["ADC", "O_M", "O_I8"], ["SUB", "O_M", "O_I8"], ["SBC", "O_M", "O_I8"],
    ["AND", "O_M", "O_I8"], ["XOR", "O_M", "O_I8"], ["OR", "O_M", "O_I8"], ["CP", "O_M", "O_I8"],

    # 40 - 5F
    ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"],
    ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"], ["MUL", "O_MC16", "O_M"],
    ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"],
    ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"], ["MULS", "O_MC16", "O_M"],
    ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"],
    ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"], ["DIV", "O_MC16", "O_M"],
    ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"],
    ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"], ["DIVS", "O_MC16", "O_M"],

    # 60 - 7F
    ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"],
    ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"], ["INC", "O_I3", "O_M"],
    ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"],
    ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"], ["DEC", "O_I3", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["RLC", "O_M", None], ["RRC", "O_M", None], ["RL", "O_M", None], ["RR", "O_M", None],
    ["SLA", "O_M", None], ["SRA", "O_M", None], ["SLL", "O_M", None], ["SRL", "O_M", None],

    # 80 - 9F
    ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"],
    ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"], ["ADD", "O_C8", "O_M"],
    ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"],
    ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"], ["ADD", "O_M", "O_C8"],
    ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"],
    ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"], ["ADC", "O_C8", "O_M"],
    ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"],
    ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"], ["ADC", "O_M", "O_C8"],

    # A0 - BF
    ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"],
    ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"], ["SUB", "O_C8", "O_M"],
    ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"],
    ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"], ["SUB", "O_M", "O_C8"],
    ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"],
    ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"], ["SBC", "O_C8", "O_M"],
    ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"],
    ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"], ["SBC", "O_M", "O_C8"],

    # C0 - DF
    ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"],
    ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"], ["AND", "O_C8", "O_M"],
    ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"],
    ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"], ["AND", "O_M", "O_C8"],
    ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"],
    ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"], ["XOR", "O_C8", "O_M"],
    ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"],
    ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"], ["XOR", "O_M", "O_C8"],

    # E0 - FF
    ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"],
    ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"], ["OR", "O_C8", "O_M"],
    ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"],
    ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"], ["OR", "O_M", "O_C8"],
    ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"],
    ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"], ["CP", "O_C8", "O_M"],
    ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"],
    ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"], ["CP", "O_M", "O_C8"],
]


# TODO: M_MUL_O_I8, M_MULS_O_I8, M_DIV_O_I8, M_DIVS_O_i8 need to be fixed
mnemonic_c8 = [
    # 00 - 1F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["LD", "O_R", "O_I8"],
    ["PUSH", "O_R", None], ["POP", "O_R", None], ["CPL", "O_R", None], ["NEG", "O_R", None],
    ["MUL", "O_R", "O_I8"], ["MULS", "O_R", "O_I8"], ["DIV", "O_R", "O_I8"], ["DIVS", "O_R", "O_I8"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DAA", "O_R", None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DJNZ", "O_R", "O_D8"], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 20 - 3F
    ["ANDCF", "O_I8", "O_R"], ["ORCF", "O_I8", "O_R"], ["XORCF", "O_I8", "O_R"], ["LDCF", "O_I8", "O_R"],
    ["STCF", "O_I8", "O_R"], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["ANDCF", "O_A", "O_R"], ["ORCF", "O_A", "O_R"], ["XORCF", "O_A", "O_R"], ["LDCF", "O_A", "O_R"],
    ["STCF", "O_A", "O_R"], ["DB", None, None], ["LDC", "O_CR8", "O_R"], ["LDC", "O_R", "O_CR8"],
    ["RES", "O_I8", "O_R"], ["SET", "O_I8", "O_R"], ["CHG", "O_I8", "O_R"], ["BIT", "O_I8", "O_R"],
    ["TSET", "O_I8", "O_R"], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 40 - 5F
    ["MUL", "O_MC16", "O_R"], ["MUL", "O_MC16", "O_R"], ["MUL", "O_MC16", "O_R"], ["MUL", "O_MC16", "O_R"],
    ["MUL", "O_MC16", "O_R"], ["MUL", "O_MC16", "O_R"], ["MUL", "O_MC16", "O_R"], ["MUL", "O_MC16", "O_R"],
    ["MULS", "O_MC16", "O_R"], ["MULS", "O_MC16", "O_R"], ["MULS", "O_MC16", "O_R"], ["MULS", "O_MC16", "O_R"],
    ["MULS", "O_MC16", "O_R"], ["MULS", "O_MC16", "O_R"], ["MULS", "O_MC16", "O_R"], ["MULS", "O_MC16", "O_R"],
    ["DIV", "O_MC16", "O_R"], ["DIV", "O_MC16", "O_R"], ["DIV", "O_MC16", "O_R"], ["DIV", "O_MC16", "O_R"],
    ["DIV", "O_MC16", "O_R"], ["DIV", "O_MC16", "O_R"], ["DIV", "O_MC16", "O_R"], ["DIV", "O_MC16", "O_R"],
    ["DIVS", "O_MC16", "O_R"], ["DIVS", "O_MC16", "O_R"], ["DIVS", "O_MC16", "O_R"], ["DIVS", "O_MC16", "O_R"],
    ["DIVS", "O_MC16", "O_R"], ["DIVS", "O_MC16", "O_R"], ["DIVS", "O_MC16", "O_R"], ["DIVS", "O_MC16", "O_R"],

    # 60 - 7F
    ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"],
    ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"],
    ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"],
    ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"],
    ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"],
    ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"],
    ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"],
    ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"],

    # 80 - 9F
    ["ADD", "O_C8", "O_R"], ["ADD", "O_C8", "O_R"], ["ADD", "O_C8", "O_R"], ["ADD", "O_C8", "O_R"],
    ["ADD", "O_C8", "O_R"], ["ADD", "O_C8", "O_R"], ["ADD", "O_C8", "O_R"], ["ADD", "O_C8", "O_R"],
    ["LD", "O_C8", "O_R"], ["LD", "O_C8", "O_R"], ["LD", "O_C8", "O_R"], ["LD", "O_C8", "O_R"],
    ["LD", "O_C8", "O_R"], ["LD", "O_C8", "O_R"], ["LD", "O_C8", "O_R"], ["LD", "O_C8", "O_R"],
    ["ADC", "O_C8", "O_R"], ["ADC", "O_C8", "O_R"], ["ADC", "O_C8", "O_R"], ["ADC", "O_C8", "O_R"],
    ["ADC", "O_C8", "O_R"], ["ADC", "O_C8", "O_R"], ["ADC", "O_C8", "O_R"], ["ADC", "O_C8", "O_R"],
    ["LD", "O_R", "O_C8"], ["LD", "O_R", "O_C8"], ["LD", "O_R", "O_C8"], ["LD", "O_R", "O_C8"],
    ["LD", "O_R", "O_C8"], ["LD", "O_R", "O_C8"], ["LD", "O_R", "O_C8"], ["LD", "O_R", "O_C8"],

    # A0 - BF
    ["SUB", "O_C8", "O_R"], ["SUB", "O_C8", "O_R"], ["SUB", "O_C8", "O_R"], ["SUB", "O_C8", "O_R"],
    ["SUB", "O_C8", "O_R"], ["SUB", "O_C8", "O_R"], ["SUB", "O_C8", "O_R"], ["SUB", "O_C8", "O_R"],
    ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"],
    ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"],
    ["SBC", "O_C8", "O_R"], ["SBC", "O_C8", "O_R"], ["SBC", "O_C8", "O_R"], ["SBC", "O_C8", "O_R"],
    ["SBC", "O_C8", "O_R"], ["SBC", "O_C8", "O_R"], ["SBC", "O_C8", "O_R"], ["SBC", "O_C8", "O_R"],
    ["EX", "O_C8", "O_R"], ["EX", "O_C8", "O_R"], ["EX", "O_C8", "O_R"], ["EX", "O_C8", "O_R"],
    ["EX", "O_C8", "O_R"], ["EX", "O_C8", "O_R"], ["EX", "O_C8", "O_R"], ["EX", "O_C8", "O_R"],

    # C0 - DF
    ["AND", "O_C8", "O_R"], ["AND", "O_C8", "O_R"], ["AND", "O_C8", "O_R"], ["AND", "O_C8", "O_R"],
    ["AND", "O_C8", "O_R"], ["AND", "O_C8", "O_R"], ["AND", "O_C8", "O_R"], ["AND", "O_C8", "O_R"],
    ["ADD", "O_R", "O_I8"], ["ADC", "O_R", "O_I8"], ["SUB", "O_R", "O_I8"], ["SBC", "O_R", "O_I8"],
    ["AND", "O_R", "O_I8"], ["XOR", "O_R", "O_I8"], ["OR", "O_R", "O_I8"], ["CP", "O_R", "O_I8"],
    ["XOR", "O_C8", "O_R"], ["XOR", "O_C8", "O_R"], ["XOR", "O_C8", "O_R"], ["XOR", "O_C8", "O_R"],
    ["XOR", "O_C8", "O_R"], ["XOR", "O_C8", "O_R"], ["XOR", "O_C8", "O_R"], ["XOR", "O_C8", "O_R"],
    ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"],
    ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"],

    # E0 - FF
    ["OR", "O_C8", "O_R"], ["OR", "O_C8", "O_R"], ["OR", "O_C8", "O_R"], ["OR", "O_C8", "O_R"],
    ["OR", "O_C8", "O_R"], ["OR", "O_C8", "O_R"], ["OR", "O_C8", "O_R"], ["OR", "O_C8", "O_R"],
    ["RLC", "O_I8", "O_R"], ["RRC", "O_I8", "O_R"], ["RL", "O_I8", "O_R"], ["RR", "O_I8", "O_R"],
    ["SLA", "O_I8", "O_R"], ["SRA", "O_I8", "O_R"], ["SLL", "O_I8", "O_R"], ["SRL", "O_I8", "O_R"],
    ["CP", "O_C8", "O_R"], ["CP", "O_C8", "O_R"], ["CP", "O_C8", "O_R"], ["CP", "O_C8", "O_R"],
    ["CP", "O_C8", "O_R"], ["CP", "O_C8", "O_R"], ["CP", "O_C8", "O_R"], ["CP", "O_C8", "O_R"],
    ["RLC", "O_A", "O_R"], ["RRC", "O_A", "O_R"], ["RL", "O_A", "O_R"], ["RR", "O_A", "O_R"],
    ["SLA", "O_A", "O_R"], ["SRA", "O_A", "O_R"], ["SLL", "O_A", "O_R"], ["SRL", "O_A", "O_R"],
]


mnemonic_d0 = [
    # 00 - 1F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["PUSHW", "O_M", None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["LDW", "O_M16", "O_M"], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 20 - 3F
    ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"],
    ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"], ["LD", "O_C16", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"],
    ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"], ["EX", "O_M", "O_C16"],
    ["ADD", "O_M", "O_I16"], ["ADC", "O_M", "O_I16"], ["SUB", "O_M", "O_I16"], ["SBC", "O_M", "O_I16"],
    ["AND", "O_M", "O_I16"], ["XOR", "O_M", "O_I16"], ["OR", "O_M", "O_I16"], ["CP", "O_M", "O_I16"],

    # 40 - 5F
    ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"],
    ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"], ["MUL", "O_C32", "O_M"],
    ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"],
    ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"], ["MULS", "O_C32", "O_M"],
    ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"],
    ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"], ["DIV", "O_C32", "O_M"],
    ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"],
    ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"], ["DIVS", "O_C32", "O_M"],

    # 60 - 7F
    ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"],
    ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"], ["INCW", "O_I3", "O_M"],
    ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"],
    ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"], ["DECW", "O_I3", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["RLCW", "O_M", None], ["RRCW", "O_M", None], ["RLW", "O_M", None], ["RRW", "O_M", None],
    ["SLAW", "O_M", None], ["SRAW", "O_M", None], ["SLLW", "O_M", None], ["SRLW", "O_M", None],

    # 80 - 9F
    ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"],
    ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"], ["ADD", "O_C16", "O_M"],
    ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"],
    ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"], ["ADD", "O_M", "O_C16"],
    ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"],
    ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"], ["ADC", "O_C16", "O_M"],
    ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"],
    ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"], ["ADC", "O_M", "O_C16"],

    # A0 - BF
    ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"],
    ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"], ["SUB", "O_C16", "O_M"],
    ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"],
    ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"], ["SUB", "O_M", "O_C16"],
    ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"],
    ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"], ["SBC", "O_C16", "O_M"],
    ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"],
    ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"], ["SBC", "O_M", "O_C16"],

    # C0 - DF
    ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"],
    ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"], ["AND", "O_C16", "O_M"],
    ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"],
    ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"], ["AND", "O_M", "O_C16"],
    ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"],
    ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"], ["XOR", "O_C16", "O_M"],
    ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"],
    ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"], ["XOR", "O_M", "O_C16"],

    # E0 - FF
    ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"],
    ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"], ["OR", "O_C16", "O_M"],
    ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"],
    ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"], ["OR", "O_M", "O_C16"],
    ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"],
    ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"], ["CP", "O_C16", "O_M"],
    ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"],
    ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"], ["CP", "O_M", "O_C16"],
]


mnemonic_d8 = [
    # 00 - 1F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["LD", "O_R", "O_I16"],
    ["PUSH", "O_R", None], ["POP", "O_R", None], ["CPL", "O_R", None], ["NEG", "O_R", None],
    ["MUL", "O_R", "O_I16"], ["MULS", "O_R", "O_I16"], ["DIV", "O_R", "O_I16"], ["DIVS", "O_R", "O_I16"],
    ["DB", None, None], ["DB", None, None], ["BS1F", "O_A", "O_R"], ["BS1B", "O_A", "O_R"],
    ["DB", None, None], ["DB", None, None], ["EXTZ", "O_R", None], ["EXTS", "O_R", None],
    ["PAA", "O_R", None], ["DB", None, None], ["MIRR", "O_R", None], ["DB", None, None],
    ["DB", None, None], ["MULA", "O_R", None], ["DB", None, None], ["DB", None, None],
    ["DJNZ", "O_R", "O_D8"], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 20 - 3F
    ["ANDCF", "O_I8", "O_R"], ["ORCF", "O_I8", "O_R"], ["XORCF", "O_I8", "O_R"], ["LDCF", "O_I8", "O_R"],
    ["STCF", "O_I8", "O_R"], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["ANDCF", "O_A", "O_R"], ["ORCF", "O_A", "O_R"], ["XORCF", "O_A", "O_R"], ["LDCF", "O_A", "O_R"],
    ["STCF", "O_A", "O_R"], ["DB", None, None], ["LDC", "O_CR16", "O_R"], ["LDC", "O_R", "O_CR16"],
    ["RES", "O_I8", "O_R"], ["SET", "O_I8", "O_R"], ["CHG", "O_I8", "O_R"], ["BIT", "O_I8", "O_R"],
    ["TSET", "O_I8", "O_R"], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["MINC1", "O_I16", "O_R"], ["MINC2", "O_I16", "O_R"], ["MINC4", "O_I16", "O_R"], ["DB", None, None],
    ["MDEC1", "O_I16", "O_R"], ["MDEC2", "O_I16", "O_R"], ["MDEC4", "O_I16", "O_R"], ["DB", None, None],

    # 40 - 5F
    ["MUL", "O_C32", "O_R"], ["MUL", "O_C32", "O_R"], ["MUL", "O_C32", "O_R"], ["MUL", "O_C32", "O_R"],
    ["MUL", "O_C32", "O_R"], ["MUL", "O_C32", "O_R"], ["MUL", "O_C32", "O_R"], ["MUL", "O_C32", "O_R"],
    ["MULS", "O_C32", "O_R"], ["MULS", "O_C32", "O_R"], ["MULS", "O_C32", "O_R"], ["MULS", "O_C32", "O_R"],
    ["MULS", "O_C32", "O_R"], ["MULS", "O_C32", "O_R"], ["MULS", "O_C32", "O_R"], ["MULS", "O_C32", "O_R"],
    ["DIV", "O_C32", "O_R"], ["DIV", "O_C32", "O_R"], ["DIV", "O_C32", "O_R"], ["DIV", "O_C32", "O_R"],
    ["DIV", "O_C32", "O_R"], ["DIV", "O_C32", "O_R"], ["DIV", "O_C32", "O_R"], ["DIV", "O_C32", "O_R"],
    ["DIVS", "O_C32", "O_R"], ["DIVS", "O_C32", "O_R"], ["DIVS", "O_C32", "O_R"], ["DIVS", "O_C32", "O_R"],
    ["DIVS", "O_C32", "O_R"], ["DIVS", "O_C32", "O_R"], ["DIVS", "O_C32", "O_R"], ["DIVS", "O_C32", "O_R"],

    # 60 - 7F
    ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"],
    ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"],
    ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"],
    ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"],
    ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"],
    ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"],
    ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"],
    ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"], ["SCC", "O_CC", "O_R"],

    # 80 - 9F
    ["ADD", "O_C16", "O_R"], ["ADD", "O_C16", "O_R"], ["ADD", "O_C16", "O_R"], ["ADD", "O_C16", "O_R"],
    ["ADD", "O_C16", "O_R"], ["ADD", "O_C16", "O_R"], ["ADD", "O_C16", "O_R"], ["ADD", "O_C16", "O_R"],
    ["LD", "O_C16", "O_R"], ["LD", "O_C16", "O_R"], ["LD", "O_C16", "O_R"], ["LD", "O_C16", "O_R"],
    ["LD", "O_C16", "O_R"], ["LD", "O_C16", "O_R"], ["LD", "O_C16", "O_R"], ["LD", "O_C16", "O_R"],
    ["ADC", "O_C16", "O_R"], ["ADC", "O_C16", "O_R"], ["ADC", "O_C16", "O_R"], ["ADC", "O_C16", "O_R"],
    ["ADC", "O_C16", "O_R"], ["ADC", "O_C16", "O_R"], ["ADC", "O_C16", "O_R"], ["ADC", "O_C16", "O_R"],
    ["LD", "O_R", "O_C16"], ["LD", "O_R", "O_C16"], ["LD", "O_R", "O_C16"], ["LD", "O_R", "O_C16"],
    ["LD", "O_R", "O_C16"], ["LD", "O_R", "O_C16"], ["LD", "O_R", "O_C16"], ["LD", "O_R", "O_C16"],

    # A0 - BF
    ["SUB", "O_C16", "O_R"], ["SUB", "O_C16", "O_R"], ["SUB", "O_C16", "O_R"], ["SUB", "O_C16", "O_R"],
    ["SUB", "O_C16", "O_R"], ["SUB", "O_C16", "O_R"], ["SUB", "O_C16", "O_R"], ["SUB", "O_C16", "O_R"],
    ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"],
    ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"],
    ["SBC", "O_C16", "O_R"], ["SBC", "O_C16", "O_R"], ["SBC", "O_C16", "O_R"], ["SBC", "O_C16", "O_R"],
    ["SBC", "O_C16", "O_R"], ["SBC", "O_C16", "O_R"], ["SBC", "O_C16", "O_R"], ["SBC", "O_C16", "O_R"],
    ["EX", "O_C16", "O_R"], ["EX", "O_C16", "O_R"], ["EX", "O_C16", "O_R"], ["EX", "O_C16", "O_R"],
    ["EX", "O_C16", "O_R"], ["EX", "O_C16", "O_R"], ["EX", "O_C16", "O_R"], ["EX", "O_C16", "O_R"],

    # C0 - DF
    ["AND", "O_C16", "O_R"], ["AND", "O_C16", "O_R"], ["AND", "O_C16", "O_R"], ["AND", "O_C16", "O_R"],
    ["AND", "O_C16", "O_R"], ["AND", "O_C16", "O_R"], ["AND", "O_C16", "O_R"], ["AND", "O_C16", "O_R"],
    ["ADD", "O_R", "O_I16"], ["ADC", "O_R", "O_I16"], ["SUB", "O_R", "O_I16"], ["SBC", "O_R", "O_I16"],
    ["AND", "O_R", "O_I16"], ["XOR", "O_R", "O_I16"], ["OR", "O_R", "O_I16"], ["CP", "O_R", "O_I16"],
    ["XOR", "O_C16", "O_R"], ["XOR", "O_C16", "O_R"], ["XOR", "O_C16", "O_R"], ["XOR", "O_C16", "O_R"],
    ["XOR", "O_C16", "O_R"], ["XOR", "O_C16", "O_R"], ["XOR", "O_C16", "O_R"], ["XOR", "O_C16", "O_R"],
    ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"],
    ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"],

    # E0 - FF
    ["OR", "O_C16", "O_R"], ["OR", "O_C16", "O_R"], ["OR", "O_C16", "O_R"], ["OR", "O_C16", "O_R"],
    ["OR", "O_C16", "O_R"], ["OR", "O_C16", "O_R"], ["OR", "O_C16", "O_R"], ["OR", "O_C16", "O_R"],
    ["RLC", "O_I8", "O_R"], ["RRC", "O_I8", "O_R"], ["RL", "O_I8", "O_R"], ["RR", "O_I8", "O_R"],
    ["SLA", "O_I8", "O_R"], ["SRA", "O_I8", "O_R"], ["SLL", "O_I8", "O_R"], ["SRL", "O_I8", "O_R"],
    ["CP", "O_C16", "O_R"], ["CP", "O_C16", "O_R"], ["CP", "O_C16", "O_R"], ["CP", "O_C16", "O_R"],
    ["CP", "O_C16", "O_R"], ["CP", "O_C16", "O_R"], ["CP", "O_C16", "O_R"], ["CP", "O_C16", "O_R"],
    ["RLC", "O_A", "O_R"], ["RRC", "O_A", "O_R"], ["RL", "O_A", "O_R"], ["RR", "O_A", "O_R"],
    ["SLA", "O_A", "O_R"], ["SRA", "O_A", "O_R"], ["SLL", "O_A", "O_R"], ["SRL", "O_A", "O_R"],
]


mnemonic_e0 = [
    # 00 - 1F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 20 - 3F
    ["LD", "O_C32", "O_M"], ["LD", "O_C32", "O_M"], ["LD", "O_C32", "O_M"], ["LD", "O_C32", "O_M"],
    ["LD", "O_C32", "O_M"], ["LD", "O_C32", "O_M"], ["LD", "O_C32", "O_M"], ["LD", "O_C32", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 40 - 5F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 60 - 7F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 80 - 9F
    ["ADD", "O_C32", "O_M"], ["ADD", "O_C32", "O_M"], ["ADD", "O_C32", "O_M"], ["ADD", "O_C32", "O_M"],
    ["ADD", "O_C32", "O_M"], ["ADD", "O_C32", "O_M"], ["ADD", "O_C32", "O_M"], ["ADD", "O_C32", "O_M"],
    ["ADD", "O_M", "O_C32"], ["ADD", "O_M", "O_C32"], ["ADD", "O_M", "O_C32"], ["ADD", "O_M", "O_C32"],
    ["ADD", "O_M", "O_C32"], ["ADD", "O_M", "O_C32"], ["ADD", "O_M", "O_C32"], ["ADD", "O_M", "O_C32"],
    ["ADC", "O_C32", "O_M"], ["ADC", "O_C32", "O_M"], ["ADC", "O_C32", "O_M"], ["ADC", "O_C32", "O_M"],
    ["ADC", "O_C32", "O_M"], ["ADC", "O_C32", "O_M"], ["ADC", "O_C32", "O_M"], ["ADC", "O_C32", "O_M"],
    ["ADC", "O_M", "O_C32"], ["ADC", "O_M", "O_C32"], ["ADC", "O_M", "O_C32"], ["ADC", "O_M", "O_C32"],
    ["ADC", "O_M", "O_C32"], ["ADC", "O_M", "O_C32"], ["ADC", "O_M", "O_C32"], ["ADC", "O_M", "O_C32"],

    # A0 - BF
    ["SUB", "O_C32", "O_M"], ["SUB", "O_C32", "O_M"], ["SUB", "O_C32", "O_M"], ["SUB", "O_C32", "O_M"],
    ["SUB", "O_C32", "O_M"], ["SUB", "O_C32", "O_M"], ["SUB", "O_C32", "O_M"], ["SUB", "O_C32", "O_M"],
    ["SUB", "O_M", "O_C32"], ["SUB", "O_M", "O_C32"], ["SUB", "O_M", "O_C32"], ["SUB", "O_M", "O_C32"],
    ["SUB", "O_M", "O_C32"], ["SUB", "O_M", "O_C32"], ["SUB", "O_M", "O_C32"], ["SUB", "O_M", "O_C32"],
    ["SBC", "O_C32", "O_M"], ["SBC", "O_C32", "O_M"], ["SBC", "O_C32", "O_M"], ["SBC", "O_C32", "O_M"],
    ["SBC", "O_C32", "O_M"], ["SBC", "O_C32", "O_M"], ["SBC", "O_C32", "O_M"], ["SBC", "O_C32", "O_M"],
    ["SBC", "O_M", "O_C32"], ["SBC", "O_M", "O_C32"], ["SBC", "O_M", "O_C32"], ["SBC", "O_M", "O_C32"],
    ["SBC", "O_M", "O_C32"], ["SBC", "O_M", "O_C32"], ["SBC", "O_M", "O_C32"], ["SBC", "O_M", "O_C32"],

    # C0 - DF
    ["AND", "O_C32", "O_M"], ["AND", "O_C32", "O_M"], ["AND", "O_C32", "O_M"], ["AND", "O_C32", "O_M"],
    ["AND", "O_C32", "O_M"], ["AND", "O_C32", "O_M"], ["AND", "O_C32", "O_M"], ["AND", "O_C32", "O_M"],
    ["AND", "O_M", "O_C32"], ["AND", "O_M", "O_C32"], ["AND", "O_M", "O_C32"], ["AND", "O_M", "O_C32"],
    ["AND", "O_M", "O_C32"], ["AND", "O_M", "O_C32"], ["AND", "O_M", "O_C32"], ["AND", "O_M", "O_C32"],
    ["XOR", "O_C32", "O_M"], ["XOR", "O_C32", "O_M"], ["XOR", "O_C32", "O_M"], ["XOR", "O_C32", "O_M"],
    ["XOR", "O_C32", "O_M"], ["XOR", "O_C32", "O_M"], ["XOR", "O_C32", "O_M"], ["XOR", "O_C32", "O_M"],
    ["XOR", "O_M", "O_C32"], ["XOR", "O_M", "O_C32"], ["XOR", "O_M", "O_C32"], ["XOR", "O_M", "O_C32"],
    ["XOR", "O_M", "O_C32"], ["XOR", "O_M", "O_C32"], ["XOR", "O_M", "O_C32"], ["XOR", "O_M", "O_C32"],

    # E0 - FF
    ["OR", "O_C32", "O_M"], ["OR", "O_C32", "O_M"], ["OR", "O_C32", "O_M"], ["OR", "O_C32", "O_M"],
    ["OR", "O_C32", "O_M"], ["OR", "O_C32", "O_M"], ["OR", "O_C32", "O_M"], ["OR", "O_C32", "O_M"],
    ["OR", "O_M", "O_C32"], ["OR", "O_M", "O_C32"], ["OR", "O_M", "O_C32"], ["OR", "O_M", "O_C32"],
    ["OR", "O_M", "O_C32"], ["OR", "O_M", "O_C32"], ["OR", "O_M", "O_C32"], ["OR", "O_M", "O_C32"],
    ["CP", "O_C32", "O_M"], ["CP", "O_C32", "O_M"], ["CP", "O_C32", "O_M"], ["CP", "O_C32", "O_M"],
    ["CP", "O_C32", "O_M"], ["CP", "O_C32", "O_M"], ["CP", "O_C32", "O_M"], ["CP", "O_C32", "O_M"],
    ["CP", "O_M", "O_C32"], ["CP", "O_M", "O_C32"], ["CP", "O_M", "O_C32"], ["CP", "O_M", "O_C32"],
    ["CP", "O_M", "O_C32"], ["CP", "O_M", "O_C32"], ["CP", "O_M", "O_C32"], ["CP", "O_M", "O_C32"],
]


mnemonic_e8 = [
    # 00 - 1F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["LD", "O_R", "O_I32"],
    ["PUSH", "O_R", None], ["POP", "O_R", None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["LINK", "O_R", "O_I16"], ["UNLK", "O_R", None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["EXTZ", "O_R", None], ["EXTS", "O_R", None],
    ["PAA", "O_R", None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 20 - 3F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["LDC", "O_CR32", "O_R"], ["LDC", "O_R", "O_CR32"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 40 - 5F
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 60 - 7F
    ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"],
    ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"], ["INC", "O_I3", "O_R"],
    ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"],
    ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"], ["DEC", "O_I3", "O_R"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 80 - 9F
    ["ADD", "O_C32", "O_R"], ["ADD", "O_C32", "O_R"], ["ADD", "O_C32", "O_R"], ["ADD", "O_C32", "O_R"],
    ["ADD", "O_C32", "O_R"], ["ADD", "O_C32", "O_R"], ["ADD", "O_C32", "O_R"], ["ADD", "O_C32", "O_R"],
    ["LD", "O_C32", "O_R"], ["LD", "O_C32", "O_R"], ["LD", "O_C32", "O_R"], ["LD", "O_C32", "O_R"],
    ["LD", "O_C32", "O_R"], ["LD", "O_C32", "O_R"], ["LD", "O_C32", "O_R"], ["LD", "O_C32", "O_R"],
    ["ADC", "O_C32", "O_R"], ["ADC", "O_C32", "O_R"], ["ADC", "O_C32", "O_R"], ["ADC", "O_C32", "O_R"],
    ["ADC", "O_C32", "O_R"], ["ADC", "O_C32", "O_R"], ["ADC", "O_C32", "O_R"], ["ADC", "O_C32", "O_R"],
    ["LD", "O_R", "O_C32"], ["LD", "O_R", "O_C32"], ["LD", "O_R", "O_C32"], ["LD", "O_R", "O_C32"],
    ["LD", "O_R", "O_C32"], ["LD", "O_R", "O_C32"], ["LD", "O_R", "O_C32"], ["LD", "O_R", "O_C32"],

    # A0 - BF
    ["SUB", "O_C32", "O_R"], ["SUB", "O_C32", "O_R"], ["SUB", "O_C32", "O_R"], ["SUB", "O_C32", "O_R"],
    ["SUB", "O_C32", "O_R"], ["SUB", "O_C32", "O_R"], ["SUB", "O_C32", "O_R"], ["SUB", "O_C32", "O_R"],
    ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"],
    ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"], ["LD", "O_R", "O_I3"],
    ["SBC", "O_C32", "O_R"], ["SBC", "O_C32", "O_R"], ["SBC", "O_C32", "O_R"], ["SBC", "O_C32", "O_R"],
    ["SBC", "O_C32", "O_R"], ["SBC", "O_C32", "O_R"], ["SBC", "O_C32", "O_R"], ["SBC", "O_C32", "O_R"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # C0 - DF
    ["AND", "O_C32", "O_R"], ["AND", "O_C32", "O_R"], ["AND", "O_C32", "O_R"], ["AND", "O_C32", "O_R"],
    ["AND", "O_C32", "O_R"], ["AND", "O_C32", "O_R"], ["AND", "O_C32", "O_R"], ["AND", "O_C32", "O_R"],
    ["ADD", "O_R", "O_I32"], ["ADC", "O_R", "O_I32"], ["SUB", "O_R", "O_I32"], ["SBC", "O_R", "O_I32"],
    ["AND", "O_R", "O_I32"], ["XOR", "O_R", "O_I32"], ["OR", "O_R", "O_I32"], ["CP", "O_R", "O_I32"],
    ["XOR", "O_C32", "O_R"], ["XOR", "O_C32", "O_R"], ["XOR", "O_C32", "O_R"], ["XOR", "O_C32", "O_R"],
    ["XOR", "O_C32", "O_R"], ["XOR", "O_C32", "O_R"], ["XOR", "O_C32", "O_R"], ["XOR", "O_C32", "O_R"],
    ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"],
    ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"], ["CP", "O_R", "O_I3"],

    # E0 - FF
    ["OR", "O_C32", "O_R"], ["OR", "O_C32", "O_R"], ["OR", "O_C32", "O_R"], ["OR", "O_C32", "O_R"],
    ["OR", "O_C32", "O_R"], ["OR", "O_C32", "O_R"], ["OR", "O_C32", "O_R"], ["OR", "O_C32", "O_R"],
    ["RLC", "O_I8", "O_R"], ["RRC", "O_I8", "O_R"], ["RL", "O_I8", "O_R"], ["RR", "O_I8", "O_R"],
    ["SLA", "O_I8", "O_R"], ["SRA", "O_I8", "O_R"], ["SLL", "O_I8", "O_R"], ["SRL", "O_I8", "O_R"],
    ["CP", "O_C32", "O_R"], ["CP", "O_C32", "O_R"], ["CP", "O_C32", "O_R"], ["CP", "O_C32", "O_R"],
    ["CP", "O_C32", "O_R"], ["CP", "O_C32", "O_R"], ["CP", "O_C32", "O_R"], ["CP", "O_C32", "O_R"],
    ["RLC", "O_A", "O_R"], ["RRC", "O_A", "O_R"], ["RL", "O_A", "O_R"], ["RR", "O_A", "O_R"],
    ["SLA", "O_A", "O_R"], ["SRA", "O_A", "O_R"], ["SLL", "O_A", "O_R"], ["SRL", "O_A", "O_R"],
]


mnemonic_f0 = [
    # 00 - 1F
    ["LD", "O_M", "O_I8"], ["DB", None, None], ["LD", "O_M", "O_I16"], ["DB", None, None],
    ["POP", "O_M", None], ["DB", None, None], ["POPW", "O_M", None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["LD", "O_M", "O_M16"], ["DB", None, None], ["LDW", "O_M", "O_M16"], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 20 - 3F */
    ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"],
    ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"], ["LDA", "O_C16", "O_M"],
    ["ANDCF", "O_A", "O_M"], ["ORCF", "O_A", "O_M"], ["XORCF", "O_A", "O_M"], ["LDCF", "O_A", "O_M"],
    ["STCF", "O_A", "O_M"], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"],
    ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"], ["LDA", "O_C32", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 40 - 5F
    ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"],
    ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"], ["LD", "O_M", "O_C8"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"],
    ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"], ["LD", "O_M", "O_C16"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 60 - 7F
    ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"],
    ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"], ["LD", "O_M", "O_C32"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],

    # 80 - 9F
    ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"],
    ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"], ["ANDCF", "O_I3", "O_M"],
    ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"],
    ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"], ["ORCF", "O_I3", "O_M"],
    ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"],
    ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"], ["XORCF", "O_I3", "O_M"],
    ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"],
    ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"], ["LDCF", "O_I3", "O_M"],

    # A0 - BF
    ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"],
    ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"], ["STCF", "O_I3", "O_M"],
    ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"],
    ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"], ["TSET", "O_I3", "O_M"],
    ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"],
    ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"], ["RES", "O_I3", "O_M"],
    ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"],
    ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"], ["SET", "O_I3", "O_M"],

    # C0 - DF
    ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"],
    ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"], ["CHG", "O_I3", "O_M"],
    ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"],
    ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"], ["BIT", "O_I3", "O_M"],
    ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"],
    ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"],
    ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"],
    ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"], ["JP", "O_CC", "O_M"],

    # E0 - FF
    ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"],
    ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"],
    ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"],
    ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"], ["CALL", "O_CC", "O_M"],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None],
    ["DB", None, None], ["DB", None, None], ["DB", None, None], ["DB", None, None]
]


reg8 = ["W", "A", "B", "C", "D", "E", "H", "L"]
reg16 = ["WA", "BC", "DE", "HL", "IX", "IY", "IZ", "SP"]
reg32 = ["XWA", "XBC", "XDE", "XHL", "XIX", "XIY", "XIZ", "XSP"]
mulreg16 = ["??", "WA", "??", "BC", "??", "DE", "??", "HL"]
cond = ["F","LT","LE","ULE","PE/OV","M/MI","Z","C","T","GE","GT","UGT","PO/NOV","P/PL","NZ","NC"]

allreg8 = [
    "RA0" ,"RW0" ,"QA0" ,"QW0" ,"RC0" ,"RB0" ,"QC0" ,"QB0" ,"RE0" ,"RD0" ,"QE0" ,"QD0" ,"RL0" ,"RH0" ,"QL0" ,"QH0" ,
    "RA1" ,"RW1" ,"QA1" ,"QW1" ,"RC1" ,"RB1" ,"QC1" ,"QB1" ,"RE1" ,"RD1" ,"QE1" ,"QD1" ,"RL1" ,"RH1" ,"QL1" ,"QH1" ,
    "RA2" ,"RW2" ,"QA2" ,"QW2" ,"RC2" ,"RB2" ,"QC2" ,"QB2" ,"RE2" ,"RD2" ,"QE2" ,"QD2" ,"RL2" ,"RH2" ,"QL2" ,"QH2" ,
    "RA3" ,"RW3" ,"QA3" ,"QW3" ,"RC3" ,"RB3" ,"QC3" ,"QB3" ,"RE3" ,"RD3" ,"QE3" ,"QD3" ,"RL3" ,"RH3" ,"QL3" ,"QH3" ,
    "r40B","r41B","r42B","r43B","r44B","r45B","r46B","r47B","r48B","r49B","r4AB","r4BB","r4CB","r4DB","r4EB","r4FB",
    "r50B","r51B","r52B","r53B","r54B","r55B","r56B","r57B","r58B","r59B","r5AB","r5BB","r5CB","r5DB","r5EB","r5FB",
    "r60B","r61B","r62B","r63B","r64B","r65B","r66B","r67B","r68B","r69B","r6AB","r6BB","r6CB","r6DB","r6EB","r6FB",
    "r70B","r71B","r72B","r73B","r74B","r75B","r76B","r77B","r78B","r79B","r7AB","r7BB","r7CB","r7DB","r7EB","r7FB",
    "r80B","r81B","r82B","r83B","r84B","r85B","r86B","r87B","r88B","r89B","r8AB","r8BB","r8CB","r8DB","r8EB","r8FB",
    "r90B","r91B","r92B","r93B","r94B","r95B","r96B","r97B","r98B","r99B","r9AB","r9BB","r9CB","r9DB","r9EB","r9FB",
    "rA0B","rA1B","rA2B","rA3B","rA4B","rA5B","rA6B","rA7B","rA8B","rA9B","rAAB","rABB","rACB","rADB","rAEB","rAFB",
    "rB0B","rB1B","rB2B","rB3B","rB4B","rB5B","rB6B","rB7B","rB8B","rB9B","rBAB","rBBB","rBCB","rBDB","rBEB","rBFB",
    "rC0B","rC1B","rC2B","rC3B","rC4B","rC5B","rC6B","rC7B","rC8B","rC9B","rCAB","rCBB","rCCB","rCDB","rCEB","rCFB",
    "RA-1","RW-1","QA-1","QW-1","RC-1","RB-1","QC-1","QB-1","RE-1","RD-1","QE-1","QD-1","RL-1","RH-1","QL-1","QH-1",
    "A"   ,"W"   ,"QA"  ,"QW"  ,"C"   ,"B"   ,"QC"  ,"QB"  ,"E"   ,"D"   ,"QE"  ,"QD"  ,"L"   ,"H"   ,"QL"  ,"QH"  ,
    "IXL" ,"IXH" ,"QIXL","QIXH","IYL" ,"IYH" ,"QIYL","QIYH","IZL" ,"IZH" ,"QIZL","QIZH","SPL" ,"SPH" ,"QSPL","QSPH",
]


allreg16 = [
    "RWA0","r01W","QWA0","r03W","RBC0","r05W","QBC0","r07W","RDE0","r09W","QDE0","r0BW","RHL0","r0DW","QHL0","r0FW",
    "RWA1","r11W","QWA1","r13W","RBC1","r15W","QBC1","r17W","RDE1","r19W","QDE1","r1BW","RHL1","r1DW","QHL1","r1FW",
    "RWA2","r21W","QWA2","r23W","RBC2","r25W","QBC2","r27W","RDE2","r29W","QDE2","r2BW","RHL2","r2DW","QHL2","r2FW",
    "RWA3","r31W","QWA3","r33W","RBC3","r35W","QBC3","r37W","RDE3","r39W","QDE3","r3BW","RHL3","r3DW","QHL3","r3FW",
    "r40W","r41W","r42W","r43W","r44W","r45W","r46W","r47W","r48W","r49W","r4AW","r4BW","r4CW","r4DW","r4EW","r4FW",
    "r50W","r51W","r52W","r53W","r54W","r55W","r56W","r57W","r58W","r59W","r5AW","r5BW","r5CW","r5DW","r5EW","r5FW",
    "r60W","r61W","r62W","r63W","r64W","r65W","r66W","r67W","r68W","r69W","r6AW","r6BW","r6CW","r6DW","r6EW","r6FW",
    "r70W","r71W","r72W","r73W","r74W","r75W","r76W","r77W","r78W","r79W","r7AW","r7BW","r7CW","r7DW","r7EW","r7FW",
    "r80W","r81W","r82W","r83W","r84W","r85W","r86W","r87W","r88W","r89W","r8AW","r8BW","r8CW","r8DW","r8EW","r8FW",
    "r90W","r91W","r92W","r93W","r94W","r95W","r96W","r97W","r98W","r99W","r9AW","r9BW","r9CW","r9DW","r9EW","r9FW",
    "rA0W","rA1W","rA2W","rA3W","rA4W","rA5W","rA6W","rA7W","rA8W","rA9W","rAAW","rABW","rACW","rADW","rAEW","rAFW",
    "rB0W","rB1W","rB2W","rB3W","rB4W","rB5W","rB6W","rB7W","rB8W","rB9W","rBAW","rBBW","rBCW","rBDW","rBEW","rBFW",
    "rC0W","rC1W","rC2W","rC3W","rC4W","rC5W","rC6W","rC7W","rC8W","rC9W","rCAW","rCBW","rCCW","rCDW","rCEW","rCFW",
    "RWA-1","rD1W","QWA-1","rD3W","RBC-1","rD5W","QBC-1","rD7W","RDE-1","rD9W","QDE-1","rDBW","RHL-1","rDDW","QHL-1","rDFW",
    "WA"  ,"rE1W","QWA" ,"rE3W","BC"  ,"rE5W","QBC" ,"rE7W","DE"  ,"rE9W","QDE" ,"rEBW","HL"  ,"rEDW","QHL" ,"rEFW",
    "IX"  ,"rF1W","QIX" ,"rF3W","IY"  ,"rF5W","QIY" ,"rF7W","IZ"  ,"rF9W","QIZ" ,"rFBW","SP"  ,"rFDW","QSP" ,"rFFW",
]

allreg32 = [
    "XWA0","XWA0","XWA0","r03L","XBC0","XBC0","XBC0","r07L","XDE0","XDE0","XDE0","r0BL","XHL0","XHL0","XHL0","r0FL",
    "XWA1","XWA1","XWA1","r13L","XBC1","XBC1","XBC1","r17L","XDE1","XDE1","XDE1","r1BL","XHL1","XHL1","XHL1","r1FL",
    "XWA2","XWA2","XWA2","r23L","XBC2","XBC2","XBC2","r27L","XDE2","XDE2","XDE2","r2BL","XHL2","XHL2","XHL2","r2FL",
    "XWA3","XWA3","XWA3","r33L","XBC3","XBC3","XBC3","r37L","XDE3","XDE3","XDE3","r3BL","XHL3","XHL3","XHL3","r3FL",
    "r40L","r41L","r42L","r43L","r44L","r45L","r46L","r47L","r48L","r49L","r4AL","r4BL","r4CL","r4DL","r4EL","r4FL",
    "r50L","r51L","r52L","r53L","r54L","r55L","r56L","r57L","r58L","r59L","r5AL","r5BL","r5CL","r5DL","r5EL","r5FL",
    "r60L","r61L","r62L","r63L","r64L","r65L","r66L","r67L","r68L","r69L","r6AL","r6BL","r6CL","r6DL","r6EL","r6FL",
    "r70L","r71L","r72L","r73L","r74L","r75L","r76L","r77L","r78L","r79L","r7AL","r7BL","r7CL","r7DL","r7EL","r7FL",
    "r80L","r81L","r82L","r83L","r84L","r85L","r86L","r87L","r88L","r89L","r8AL","r8BL","r8CL","r8DL","r8EL","r8FL",
    "r90L","r91L","r92L","r93L","r94L","r95L","r96L","r97L","r98L","r99L","r9AL","r9BL","r9CL","r9DL","r9EL","r9FL",
    "rA0L","rA1L","rA2L","rA3L","rA4L","rA5L","rA6L","rA7L","rA8L","rA9L","rAAL","rABL","rACL","rADL","rAEL","rAFL",
    "rB0L","rB1L","rB2L","rB3L","rB4L","rB5L","rB6L","rB7L","rB8L","rB9L","rBAL","rBBL","rBCL","rBDL","rBEL","rBFL",
    "rC0L","rC1L","rC2L","rC3L","rC4L","rC5L","rC6L","rC7L","rC8L","rC9L","rCAL","rCBL","rCCL","rCDL","rCEL","rCFL",
    "XWA-1","XWA-1","XWA-1","rD3L","XBC-1","XBC-1","XBC-1","rD7L","XDE-1","XDE-1","XDE-1","rDBL","XHL-1","XHL-1","XHL-1","rDFL",
    "XWA" ,"XWA" ,"XWA" ,"rE3L","XBC" ,"XBC", "XBC" ,"rE7L","XDE" ,"XDE" ,"XDE" ,"rEDL","XHL" ,"XHL" ,"XHL" ,"rEFL",
    "XIX" ,"XIX" ,"XIX" ,"rF3L","XIY" ,"XIY" ,"XIY" ,"rF7L","XIZ" ,"XIZ" ,"XIZ" ,"rFBL","XSP" ,"XSP" ,"XSP" ,"rFFL",
]


MNEMONIC = 0
OPERAND_1 = 1
OPERAND_2 = 2

class TLCS900H_Trace(ExecTrace):
    def getLabelName(self, addr):
        self.register_label(addr)
        if addr in KNOWN_LABELS:
            return KNOWN_LABELS[addr]
        elif addr in POSSIBLY_UNUSED_CODEBLOCKS:
            return "JUNK__%04X" % addr
        else:
            return "LABEL_%04X" % addr

    def output_disasm_headers(self):
        header = "; Generated by TLCS900-disasm / ExecTrace by Felipe Sanches\n"
        for var in SPECIAL_PURPOSE_VARS.keys():
            name = SPECIAL_PURPOSE_VARS[var]
            header += "%s\t\tEQU 0x%02X\n" % (name, var)

        return header

    def format_operand(self, opcode, operand, dasm, value, v):
        if operand == None:
            return ""

        elif operand == "O_A":
            return " A"

        elif operand == "O_C8":
            return " %s" % reg8[v & 0x07]

        elif operand == "O_C16":
            return " %s" % reg16[v & 0x07]

        elif operand == "O_C32":
            return " %s" % reg32[v & 0x07]

        elif operand == "O_MC16":
            return " %s" % mulreg16[v & 0x07]

        elif operand == "O_CC":
            self.condition = cond[v & 0x0F]
            return " %s" % self.condition

        elif operand == "O_CR8":
            imm = self.fetch()
            if imm & 0xe3 == 0x42:
                return " DMAM%d" % ((imm >> 2) & 7)
            else:
                return " <Unknown 8-bit ControlReg 0x%02X>" % imm

        elif operand == "O_CR16":
            imm = self.fetch()
            if imm & 0xe3 == 0x40:
                return " DMAC%d" % ((imm >> 2) & 7)
            else:
                return " <Unknown 16-bit ControlReg 0x%02X>" % imm

        elif operand == "O_CR32":
            imm = self.fetch()
            if imm & 0xe3 == 0x00:
                return " DMAS%d" % ((imm >> 2) & 7)
            if imm & 0xe3 == 0x20:
                return " DMAD%d" % ((imm >> 2) & 7)
            else:
                return " <Unknown 32-bit ControlReg 0x%02X>" % imm

        elif operand == "O_D8":
            imm = self.fetch()
            if(imm & 0x80):
                imm = -0x100 + imm
            address = ((self.PC + imm) & 0xFFFFFF)
            if dasm[MNEMONIC] == "DJNZ":
                self.conditional_branch(address)
                return " " + self.getLabelName(address)
            elif dasm[MNEMONIC] == "JR":
                if self.condition == "T":
                   self.unconditional_jump(address)
                elif self.condition != "F":
                   self.conditional_branch(address)
                return " " + self.getLabelName(address)
            else:
                return " 0x%06x" % (address)

        elif operand == "O_D16":
            imm = self.fetch()
            imm = imm | (self.fetch() << 8)
            if(imm & 0x8000):
                imm = -0x10000 + imm
            address = ((self.PC + int(imm)) & 0xFFFFFF)
            if dasm[MNEMONIC] == "CALR":
                self.subroutine(address)
                return " " + self.getLabelName(address)
            elif dasm[MNEMONIC] == "JRL":
                if self.condition == "T":
                   self.unconditional_jump(address)
                elif self.condition != "F":
                   self.conditional_branch(address)
                return " " + self.getLabelName(address)
            else:
                return " 0x%06x" % (address)

        elif operand == "O_F":
            return " F"

        elif operand == "O_I3":
            return " %d" % (v & 0x07)

        elif operand == "O_I8":
            imm = self.fetch()
            return ", 0x%02x" % imm

        elif operand == "O_I16":
            imm = self.fetch()
            imm = imm | (self.fetch() << 8)
            address = imm
            if dasm[MNEMONIC] == "CALL":
                self.subroutine(address)
                return " " + self.getLabelName(address)
            elif dasm[MNEMONIC] == "JP":
                self.unconditional_jump(address)
                return " " + self.getLabelName(address)
            else:
                return ", 0x%04x" % imm

        elif operand == "O_I24":
            imm = self.fetch()
            imm = imm | (self.fetch() << 8)
            imm = imm | (self.fetch() << 16)
            address = imm
            if dasm[MNEMONIC] in ["CALL"]:
                self.subroutine(address)
                return " " + self.getLabelName(address)
            else:
                return ", 0x%06x" % imm

        elif operand == "O_I32":
            imm = self.fetch()
            imm = imm | (self.fetch() << 8)
            imm = imm | (self.fetch() << 16)
            imm = imm | (self.fetch() << 24)
            return ", 0x%08x" % imm

        elif operand == "O_M":
            if dasm[MNEMONIC] == "CALL" and self.condition != "F":
                if isinstance(value, int):
                    self.subroutine(value)
                    return " " + self.getLabelName(value)
                else:
                    if self.PC not in self.jump_table_from:
                        self.count_warns += 1
                        print(f"WARNING at {self.PC:08X}:  CALL {value}")
                    return f" {value}"
            if dasm[MNEMONIC] == "JP":
                if isinstance(value, int):
                    if self.condition == "T":
                       self.unconditional_jump(value)
                    elif self.condition != "F":
                       self.conditional_branch(value)
                    return " " + self.getLabelName(value)
                else:
                    if self.PC not in self.jump_table_from:
                        self.count_warns += 1
                        print(f"WARNING at {self.PC:08X}:  JP {self.condition} {value}")
                    #self.restart_from_another_entry_point()
                    self.return_from_subroutine()
                    return f" {value}"
            elif dasm[MNEMONIC] == "LDA":
                return " %s" % getVariableName(value)
            else:
                return " (%s)" % getVariableName(value)

        elif operand == "O_M8":
            imm = self.fetch()
            return " (%s)" % getVariableName(imm)

        elif operand == "O_M16":
            imm = self.fetch()
            imm = imm | (self.fetch() << 8)
            return " (%s)" % getVariableName(imm)

        elif operand == "O_R":
            return " %s" % value

        elif operand == "O_SR":
            return " SR"

        else:
            return " <? %s>" % operand



    def disasm_instruction(self, opcode):
        buf = "bug"
        v = opcode
        dasm = instructions[opcode]

        # Check for extended addressing modes
        if dasm[MNEMONIC] == "M_80":
            buf = reg32[opcode & 0x07]
            v = self.fetch()
            dasm = mnemonic_80[v]


        elif dasm[MNEMONIC] == "M_88":
            imm = self.fetch()
            buf = "%s + 0x%02x" % (reg32[opcode & 0x07], imm)
            v = self.fetch()
            dasm = mnemonic_88[v]


        elif dasm[MNEMONIC] == "M_90":
            buf = reg32[opcode & 0x07]
            v = self.fetch()
            dasm = mnemonic_90[v]


        elif dasm[MNEMONIC] == "M_98":
            imm = self.fetch()
            buf = "%s + 0x%02x" % (reg32[opcode & 0x07], imm)
            v = self.fetch()
            dasm = mnemonic_98[v]


        elif dasm[MNEMONIC] == "M_A0":
            buf = reg32[opcode & 0x07]
            v = self.fetch()
            dasm = mnemonic_a0[v]


        elif dasm[MNEMONIC] == "M_A8":
            imm = self.fetch()
            buf = "%s + 0x%02x" % (reg32[opcode & 0x07], imm)
            v = self.fetch()
            dasm = mnemonic_a0[v]


        elif dasm[MNEMONIC] == "M_B0":
            buf = reg32[opcode & 0x07]
            v = self.fetch()
            dasm = mnemonic_b0[v]


        elif dasm[MNEMONIC] == "M_B8":
            imm = self.fetch()
            buf = "%s + 0x%02x" % (reg32[opcode & 0x07], imm)
            v = self.fetch()
            dasm = mnemonic_b8[v]


        elif dasm[MNEMONIC] == "M_C0":

            if opcode & 0x07 == 0x00:  # 0xC0
                imm = self.fetch()
                buf = imm

            elif opcode & 0x07 == 0x01:  # 0xC1
                imm = self.fetch()
                imm = imm | (self.fetch() << 8)
                buf = imm

            elif opcode & 0x07 == 0x02:  # 0xC2
                imm = self.fetch()
                imm = imm | (self.fetch() << 8)
                imm = imm | (self.fetch() << 16)
                buf = imm

            elif opcode & 0x07 == 0x03:  # 0xC3
                imm = self.fetch()
                if imm & 0x03 == 0x00:
                    buf = allreg32[imm]

                elif imm & 0x03 == 0x01:
                    op = imm
                    imm = self.fetch()
                    imm = imm | (self.fetch() << 8)
                    buf = "%s + 0x%04x" % (allreg32[op], imm)

                elif imm & 0x03 == 0x02:
                    buf = "unknown"

                elif imm & 0x03 == 0x03:
                    if imm == 0x3:
                        op = self.fetch()
                        op1 = self.fetch()
                        buf = "%s + %s" % (allreg32[op], allreg8[op1])

                    elif imm == 0x07:
                        op = self.fetch()
                        op1 = self.fetch()
                        buf = "%s + %s" % (allreg32[op], allreg16[op1])

                    elif imm == 0x13:
                        imm = self.fetch()
                        imm = imm | (self.fetch() << 8)
                        buf = self.PC + int(imm)

            elif opcode & 0x07 == 0x04:  # 0xC4
                imm = self.fetch()
                buf = "-%s" % allreg32[imm]

            elif opcode & 0x07 == 0x05:  # 0xC5
                imm = self.fetch()
                buf = "%s+" % allreg32[imm]

            else:
                self.illegal_instruction(opcode)
                return "; BAD '0xC?' instruction parsing! (? = 0x%02X)" % (opcode & 0x07)

            v = self.fetch()
            dasm = mnemonic_c0[v]


        elif dasm[MNEMONIC] == "oC8":
            if opcode & 0x08:
                buf = reg8[opcode & 0x07]
            else:
                imm = self.fetch()
                buf = allreg8[imm]

            v = self.fetch()
            dasm = mnemonic_c8[v]


        elif dasm[MNEMONIC] == "M_D0":

            if opcode & 0x07 == 0x00:  # 0xD0
                imm = self.fetch()
                buf = imm

            elif opcode & 0x07 == 0x01:  # 0xD1
                imm = self.fetch()
                imm = imm | (self.fetch() << 8)
                buf = imm

            elif opcode & 0x07 == 0x02:  # 0xD2
                imm = self.fetch()
                imm = imm | (self.fetch() << 8)
                imm = imm | (self.fetch() << 16)
                buf = imm

            elif opcode & 0x07 == 0x03:  # 0xD3
                imm = self.fetch()
                if imm & 0x03 == 0x00:
                    buf = allreg32[imm]

                elif imm & 0x03 == 0x01:
                    op = imm
                    imm = self.fetch()
                    imm = imm | (self.fetch() << 8)
                    buf = "%s + 0x%04x" % (allreg32[op], imm)

                elif imm & 0x03 == 0x02:
                    buf = "unknown"

                elif imm & 0x03 == 0x03:
                    if imm == 0x3:
                        op = self.fetch()
                        op1 = self.fetch()
                        buf = "%s + %s" % (allreg32[op], allreg8[op1])

                    elif imm == 0x07:
                        op = self.fetch()
                        op1 = self.fetch()
                        buf = "%s + %s" % (allreg32[op], allreg16[op1])

                    elif imm == 0x13:
                        imm = self.fetch()
                        imm = imm | (self.fetch() << 8)
                        buf = self.PC + int(imm)

            elif opcode & 0x07 == 0x04:  # 0xD4
                imm = self.fetch()
                buf = "-%s" % allreg8[imm]

            elif opcode & 0x07 == 0x05:  # 0xD5
                imm = self.fetch()
                buf = "%s+" % allreg8[imm]

            else:
                self.illegal_instruction(opcode)
                return "; BAD '0xD?' instruction parsing! (? = 0x%02X)" % (opcode & 0x07)

            v = self.fetch()
            dasm = mnemonic_d0[v]


        elif dasm[MNEMONIC] == "oD8":
            if opcode & 0x08:
                buf = reg16[opcode & 0x07]
            else:
                imm = self.fetch()
                buf = allreg16[imm]

            v = self.fetch()
            dasm = mnemonic_d8[v]


        elif dasm[MNEMONIC] == "M_E0":

            if opcode & 0x07 == 0x00:  # 0xE0
                imm = self.fetch()
                buf = imm

            elif opcode & 0x07 == 0x01:  # 0xE1
                imm = self.fetch()
                imm = imm | (self.fetch() << 8)
                buf = imm

            elif opcode & 0x07 == 0x02:  # 0xE2
                imm = self.fetch()
                imm = imm | (self.fetch() << 8)
                imm = imm | (self.fetch() << 16)
                buf = imm

            elif opcode & 0x07 == 0x03:  # 0xE3
                imm = self.fetch()
                if imm & 0x03 == 0x00:
                    buf = allreg32[imm]

                elif imm & 0x03 == 0x01:
                    op = imm
                    imm = self.fetch()
                    imm = imm | (self.fetch() << 8)
                    buf = "%s + 0x%04x" % (allreg32[op], imm)

                elif imm & 0x03 == 0x02:
                    buf = "unknown"

                elif imm & 0x03 == 0x03:
                    if imm == 0x3:
                        op = self.fetch()
                        op1 = self.fetch()
                        buf = "%s + %s" % (allreg32[op], allreg8[op1])

                    elif imm == 0x07:
                        op = self.fetch()
                        op1 = self.fetch()
                        buf = "%s + %s" % (allreg32[op], allreg16[op1])

                    elif imm == 0x13:
                        imm = self.fetch()
                        imm = imm | (self.fetch() << 8)
                        buf = self.PC + int(imm)

            elif opcode & 0x07 == 0x04:  # 0xE4
                imm = self.fetch()
                buf = "-%s" % allreg32[imm]

            elif opcode & 0x07 == 0x05:  # 0xE5
                imm = self.fetch()
                buf = "%s+" % allreg32[imm]

            else:
                self.illegal_instruction(opcode)
                return "; BAD '0xE?' instruction parsing! (? = 0x%02X)" % (opcode & 0x07)

            v = self.fetch()
            dasm = mnemonic_e0[v]


        elif dasm[MNEMONIC] == "M_E8":
            if opcode & 0x08:
                buf = reg32[opcode & 0x07]
            else:
                imm = self.fetch()
                buf = allreg32[imm]

            v = self.fetch()
            dasm = mnemonic_e8[v]


        elif dasm[MNEMONIC] == "M_F0":

            if opcode & 0x07 == 0x00:  # 0xF0
                imm = self.fetch()
                buf = imm

            elif opcode & 0x07 == 0x01:  # 0xF1
                imm = self.fetch()
                imm = imm | (self.fetch() << 8)
                buf = imm

            elif opcode & 0x07 == 0x02:  # 0xF2
                imm = self.fetch()
                imm = imm | (self.fetch() << 8)
                imm = imm | (self.fetch() << 16)
                buf = imm

            elif opcode & 0x07 == 0x03:  # 0xF3
                imm = self.fetch()
                if imm & 0x03 == 0x00:
                    buf = allreg32[imm]

                elif imm & 0x03 == 0x01:
                    op = imm
                    imm = self.fetch()
                    imm = imm | (self.fetch() << 8)
                    buf = "%s + 0x%04x" % (allreg32[op], imm)

                elif imm & 0x03 == 0x02:
                    buf = "unknown"

                elif imm & 0x03 == 0x03:
                    if imm == 0x3:
                        op = self.fetch()
                        op1 = self.fetch()
                        buf = "%s + %s" % (allreg32[op], allreg8[op1])

                    elif imm == 0x07:
                        op = self.fetch()
                        op1 = self.fetch()
                        buf = "%s + %s" % (allreg32[op], allreg16[op1])

                    elif imm == 0x13:
                        imm = self.fetch()
                        imm = imm | (self.fetch() << 8)
                        buf = self.PC + int(imm)

            elif opcode & 0x07 == 0x04:  # 0xF4
                imm = self.fetch()
                buf = "-%s" % allreg32[imm]

            elif opcode & 0x07 == 0x05:  # 0xF5
                imm = self.fetch()
                buf = "%s+" % allreg32[imm]

            else:
                self.illegal_instruction(opcode)
                return "; BAD '0xF?' instruction parsing! (? = 0x%02X)" % (opcode & 0x07)

            v = self.fetch()
            dasm = mnemonic_f0[v]


        # FIXME: here we probably want to take our last chance to see if a numeric value
        #        corresponds to a label or a known variable
        dasm_string = dasm[MNEMONIC]

        op1 = self.format_operand(opcode, dasm[OPERAND_1], dasm, buf, v)
        dasm_string += format_hex_value(op1)

        op2 = self.format_operand(opcode, dasm[OPERAND_2], dasm, buf, v)
        dasm_string += format_hex_value(op2)

        # print(f"next: {hex(self.PC)}\t{dasm_string}")
        if dasm[MNEMONIC] in ["RET", "RETI", "HALT"] and dasm[OPERAND_1] == None: # ignore conditional ret
            self.return_from_subroutine()

        # TODO: How should we deal with these instructions?
        #       I am not yet familiar with their meaning / typical usage.
        #       - RETD
        #       - NORMAL
        #       - SWI
        #       - LINK
        #       - UNLK
        return dasm_string


if not (len(sys.argv) == 2):
    sys.exit(f"usage: {sys.argv[0]} <rom_file>")


rom_file = sys.argv[1]
disasm_dir = f"output"
LABELED_CINEMATIC_ENTRIES = {}
KNOWN_LABELS = {}
POSSIBLY_UNUSED_CODEBLOCKS = {}

RELOCATION_BLOCKS = (
    # physical,  logical, length 
    (0x000000,  0xe00000, 0x200000),
)

entry_points = []
rom = open(rom_file, "rb")
jump_table_from = []
def read_jump_table(called_from, base_addr, num_entries):
    global entry_points
    global jump_tables
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


def ignore_jump_table(called_from):
    if called_from not in jump_table_from:
        jump_table_from.append(called_from)


def register_jump_table_addresses(called_from, addresses):
    global entry_points
    global jump_tables
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


ignore_jump_table(called_from=0xFC44EC)

# Sorted by base_addr:
read_jump_table(called_from=0xFCD4ED, base_addr=0xEE10D0, num_entries=8)
read_jump_table(called_from=0xFDA068, base_addr=0xEE304C, num_entries=192)
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
read_jump_table(called_from=0xFC44CA, base_addr=0xFC4489, num_entries=11)
read_jump_table(called_from=0xFCADA0, base_addr=0xFCADA3, num_entries=8)  # Note: fcb40b, fcadc3, fcb001, fcadd4, fcb44e
read_jump_table(called_from=0xFCB6F9, base_addr=0xFCB6F9, num_entries=4)
read_jump_table(called_from=0xFCF760, base_addr=0xFCF761, num_entries=8)
read_jump_table(called_from=0xFD058A, base_addr=0xFD175E, num_entries=192)

# Sorted by offsets_addr:
read_jump_table_16bit_offsets(called_from=0xEF4784, base_addr=0xEF4784, offsets_addr=0xE00178, num_entries=8)
read_jump_table_16bit_offsets(called_from=0xF46524, base_addr=0xF46524, offsets_addr=0xE44A42, num_entries=8)
read_jump_table_16bit_offsets(called_from=0xF4677E, base_addr=0xF4677E, offsets_addr=0xE44A52, num_entries=11)
read_jump_table_16bit_offsets(called_from=0xF4670F, base_addr=0xF4670F, offsets_addr=0xE44A6A, num_entries=15)
read_jump_table_16bit_offsets(called_from=0xFE137D, base_addr=0xFE137D, offsets_addr=0xEE8F06, num_entries=14)
read_jump_table_16bit_offsets(called_from=0xFEEB06, base_addr=0xFEEB06, offsets_addr=0xEED3C6, num_entries=6)
read_jump_table_16bit_offsets(called_from=0xFEEB97, base_addr=0xFEEB97, offsets_addr=0xEED3D2, num_entries=6)






# TODO: Move this to the TLCS900_Trace class, as a load_interrupt_vector method.
vector = 0x1FFF00
int_num = 0
while vector <= 0x1FFFB0:
    rom.seek(vector)
    address = ord(rom.read(1))
    address = ord(rom.read(1)) << 8 | address
    address = ord(rom.read(1)) << 16 | address
    address = ord(rom.read(1)) << 24 | address
    if address not in entry_points:
        entry_points.append(address)
        # print(f"{int_num}: {address:08x}")
    int_num += 1
    vector += 4
rom.close()


# TODO: use jump_table_from on the ExecTrace class
#       to nor report jump tables that were already documented

trace = TLCS900H_Trace(rom_file,
                       relocation_blocks=RELOCATION_BLOCKS,
                       subroutines=POSSIBLY_UNUSED_CODEBLOCKS.copy(),
                       labels=KNOWN_LABELS.copy(),
                       loglevel=0)
trace.jump_table_from = jump_table_from
trace.count_warns = 0
trace.run(entry_points)
for ep in entry_points:
    trace.register_label(ep)
#trace.print_ranges()
#trace.print_grouped_ranges()

print(f"Emitted {trace.count_warns} warnings.")
trace.save_disassembly_listing(f"{rom_file}.asm")

