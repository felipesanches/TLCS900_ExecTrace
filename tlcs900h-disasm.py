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


def getVariableName(value):
    if value in SPECIAL_PURPOSE_VARS.keys():
        return SPECIAL_PURPOSE_VARS[value]
    else:
        return "0x%04X" % value

FOO_instructions = [
    "ADC", "ADD", "AND", "ANDCF", "BIT", "BS1B",
    "BS1F", "CALL", "CALR", "CCF", "CHG", "CP",
    "CPD", "CPDW", "CPDR", "CPDRW", "CPI", "CPIR",
    "CPIRW", "CPIW", "CPL", "DAA", "DB", "DEC",
    "DECF", "DECW", "DIV", "DIVS", "DJNZ", "EI",
    "EX", "EXTS", "EXTZ", "HALT", "INC", "INCF",
    "INCW", "JP", "JR", "JRL", "LD", "LDA",
    "LDC", "LDCF", "LDD", "LDDR", "LDDRW", "LDDW",
    "LDF", "LDI", "LDIR", "LDIRW", "LDIW", "LDW",
    "LDX", "LINK", "MAX", "MDEC1", "MDEC2", "MDEC4",
    "MINC1", "MINC2", "MINC4", "MIRR", "MUL", "MULA",
    "MULS", "NEG", "NOP", "NORMAL", "OR", "ORCF",
    "PAA", "POP", "POPW", "PUSH", "PUSHW", "RCF",
    "RES", "RET", "RETD", "RETI", "RL", "RLC",
    "RLCW", "RLD", "RLW", "RR", "RRC", "RRCW",
    "RRD", "RRW", "SBC", "SCC", "SCF", "SET",
    "SLA", "SLAW", "SLL", "SLLW", "SRA", "SRAW",
    "SRL", "SRLW", "STCF", "SUB", "SWI", "TSET",
    "UNLK", "XOR", "XORCF", "ZCF",
    "M_80", "M_88", "M_90", "M_98", "M_A0", "M_A8", "M_B0", "M_B8",
    "M_C0", "oC8", "M_D0", "oD8", "M_E0", "M_E8", "M_F0"
]

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

mnemonic_f0 = [
    # 00 - 1F
    ["LD", "O_M", "O_I8"], ["DB", None, None], ["LD", "O_M", "O_I16"], ["DB", None, None],

# TODO:
#	{ M_POP, O_M, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_POPW, O_M, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_LD, O_M, O_M16 }, { M_DB, O_NONE, O_NONE }, { M_LDW, O_M, O_M16 }, { M_DB, O_NONE, O_NONE },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#
#	/* 20 - 3F */
#	{ M_LDA, O_C16, O_M }, { M_LDA, O_C16, O_M }, { M_LDA, O_C16, O_M }, { M_LDA, O_C16, O_M },
#	{ M_LDA, O_C16, O_M }, { M_LDA, O_C16, O_M }, { M_LDA, O_C16, O_M }, { M_LDA, O_C16, O_M },
#	{ M_ANDCF, O_A, O_M }, { M_ORCF, O_A, O_M }, { M_XORCF, O_A, O_M }, { M_LDCF, O_A, O_M },
#	{ M_STCF, O_A, O_M }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_LDA, O_C32, O_M }, { M_LDA, O_C32, O_M }, { M_LDA, O_C32, O_M }, { M_LDA, O_C32, O_M },
#	{ M_LDA, O_C32, O_M }, { M_LDA, O_C32, O_M }, { M_LDA, O_C32, O_M }, { M_LDA, O_C32, O_M },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#
#	/* 40 - 5F */
#	{ M_LD, O_M, O_C8 }, { M_LD, O_M, O_C8 }, { M_LD, O_M, O_C8 }, { M_LD, O_M, O_C8 },
#	{ M_LD, O_M, O_C8 }, { M_LD, O_M, O_C8 }, { M_LD, O_M, O_C8 }, { M_LD, O_M, O_C8 },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_LD, O_M, O_C16 }, { M_LD, O_M, O_C16 }, { M_LD, O_M, O_C16 }, { M_LD, O_M, O_C16 },
#	{ M_LD, O_M, O_C16 }, { M_LD, O_M, O_C16 }, { M_LD, O_M, O_C16 }, { M_LD, O_M, O_C16 },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#
#	/* 60 - 7F */
#	{ M_LD, O_M, O_C32 }, { M_LD, O_M, O_C32 }, { M_LD, O_M, O_C32 }, { M_LD, O_M, O_C32 },
#	{ M_LD, O_M, O_C32 }, { M_LD, O_M, O_C32 }, { M_LD, O_M, O_C32 }, { M_LD, O_M, O_C32 },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#
#	/* 80 - 9F */
#	{ M_ANDCF, O_I3, O_M }, { M_ANDCF, O_I3, O_M }, { M_ANDCF, O_I3, O_M }, { M_ANDCF, O_I3, O_M },
#	{ M_ANDCF, O_I3, O_M }, { M_ANDCF, O_I3, O_M }, { M_ANDCF, O_I3, O_M }, { M_ANDCF, O_I3, O_M },
#	{ M_ORCF, O_I3, O_M }, { M_ORCF, O_I3, O_M }, { M_ORCF, O_I3, O_M }, { M_ORCF, O_I3, O_M },
#	{ M_ORCF, O_I3, O_M }, { M_ORCF, O_I3, O_M }, { M_ORCF, O_I3, O_M }, { M_ORCF, O_I3, O_M },
#	{ M_XORCF, O_I3, O_M }, { M_XORCF, O_I3, O_M }, { M_XORCF, O_I3, O_M }, { M_XORCF, O_I3, O_M },
#	{ M_XORCF, O_I3, O_M }, { M_XORCF, O_I3, O_M }, { M_XORCF, O_I3, O_M }, { M_XORCF, O_I3, O_M },
#	{ M_LDCF, O_I3, O_M }, { M_LDCF, O_I3, O_M }, { M_LDCF, O_I3, O_M }, { M_LDCF, O_I3, O_M },
#	{ M_LDCF, O_I3, O_M }, { M_LDCF, O_I3, O_M }, { M_LDCF, O_I3, O_M }, { M_LDCF, O_I3, O_M },
#
#	/* A0 - BF */
#	{ M_STCF, O_I3, O_M }, { M_STCF, O_I3, O_M }, { M_STCF, O_I3, O_M }, { M_STCF, O_I3, O_M },
#	{ M_STCF, O_I3, O_M }, { M_STCF, O_I3, O_M }, { M_STCF, O_I3, O_M }, { M_STCF, O_I3, O_M },
#	{ M_TSET, O_I3, O_M }, { M_TSET, O_I3, O_M }, { M_TSET, O_I3, O_M }, { M_TSET, O_I3, O_M },
#	{ M_TSET, O_I3, O_M }, { M_TSET, O_I3, O_M }, { M_TSET, O_I3, O_M }, { M_TSET, O_I3, O_M },
#	{ M_RES, O_I3, O_M }, { M_RES, O_I3, O_M }, { M_RES, O_I3, O_M }, { M_RES, O_I3, O_M },
#	{ M_RES, O_I3, O_M }, { M_RES, O_I3, O_M }, { M_RES, O_I3, O_M }, { M_RES, O_I3, O_M },
#	{ M_SET, O_I3, O_M }, { M_SET, O_I3, O_M }, { M_SET, O_I3, O_M }, { M_SET, O_I3, O_M },
#	{ M_SET, O_I3, O_M }, { M_SET, O_I3, O_M }, { M_SET, O_I3, O_M }, { M_SET, O_I3, O_M },
#
#	/* C0 - DF */
#	{ M_CHG, O_I3, O_M }, { M_CHG, O_I3, O_M }, { M_CHG, O_I3, O_M }, { M_CHG, O_I3, O_M },
#	{ M_CHG, O_I3, O_M }, { M_CHG, O_I3, O_M }, { M_CHG, O_I3, O_M }, { M_CHG, O_I3, O_M },
#	{ M_BIT, O_I3, O_M }, { M_BIT, O_I3, O_M }, { M_BIT, O_I3, O_M }, { M_BIT, O_I3, O_M },
#	{ M_BIT, O_I3, O_M }, { M_BIT, O_I3, O_M }, { M_BIT, O_I3, O_M }, { M_BIT, O_I3, O_M },
#	{ M_JP, O_CC, O_M }, { M_JP, O_CC, O_M }, { M_JP, O_CC, O_M }, { M_JP, O_CC, O_M },
#	{ M_JP, O_CC, O_M }, { M_JP, O_CC, O_M }, { M_JP, O_CC, O_M }, { M_JP, O_CC, O_M },
#	{ M_JP, O_CC, O_M }, { M_JP, O_CC, O_M }, { M_JP, O_CC, O_M }, { M_JP, O_CC, O_M },
#	{ M_JP, O_CC, O_M }, { M_JP, O_CC, O_M }, { M_JP, O_CC, O_M }, { M_JP, O_CC, O_M },
#
#	/* E0 - FF */
#	{ M_CALL, O_CC, O_M }, { M_CALL, O_CC, O_M }, { M_CALL, O_CC, O_M }, { M_CALL, O_CC, O_M },
#	{ M_CALL, O_CC, O_M }, { M_CALL, O_CC, O_M }, { M_CALL, O_CC, O_M }, { M_CALL, O_CC, O_M },
#	{ M_CALL, O_CC, O_M }, { M_CALL, O_CC, O_M }, { M_CALL, O_CC, O_M }, { M_CALL, O_CC, O_M },
#	{ M_CALL, O_CC, O_M }, { M_CALL, O_CC, O_M }, { M_CALL, O_CC, O_M }, { M_CALL, O_CC, O_M },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE },
#	{ M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }, { M_DB, O_NONE, O_NONE }
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

    def format_operand(self, operand, dasm, value):
        if operand == None:
            return ""
        elif operand == "O_M":
            if dasm[MNEMONIC] in ["CALL", "JP", "LDA"]:
                return f" {value}"
            else:
                return f" ({value})"
        elif operand == "O_I8":
            imm = self.fetch()
            return ", 0x%02x" % imm
        else:
            return "?"


    def disasm_instruction(self, opcode):
        buf = "bug"
        dasm = instructions[opcode]

        # Check for extended addressing modes
        if dasm[MNEMONIC] == "M_F0":
            if opcode & 0x07 == 0x01:  # 0xF1
                buf = self.fetch()
                buf = buf | (self.fetch() << 8)
                buf = getVariableName(buf)
            else:
                self.illegal_instruction(opcode)
                return "; BAD '0xF?' instruction parsing! (? = 0x%02X)" % (opcode & 0x07)

            dasm = mnemonic_f0[self.fetch()]

        dasm_string = dasm[MNEMONIC]
        dasm_string += self.format_operand(dasm[OPERAND_1], dasm, buf)
        dasm_string += self.format_operand(dasm[OPERAND_2], dasm, buf)

        return dasm_string

    def OLD_CODE_disasm_instruction(self, opcode):

        if opcode == 0x01: # mov
            dstVar = getVariableName(self.fetch())
            srcVar = getVariableName(self.fetch())
            return "mov [%s], [%s]" % (dstVar, srcVar)

        elif opcode == 0x02: # add
            dstVar = getVariableName(self.fetch())
            srcVar = getVariableName(self.fetch())
            return "add [%s], [%s]" % (dstVar, srcVar)

        elif opcode == 0x04: # call
            address = self.fetch()
            address = (address << 8) | self.fetch()
            self.subroutine(address)
            return "call %s" % self.getLabelName(address)

        elif opcode == 0x05: # ret
            self.return_from_subroutine()
            return "ret"

        elif opcode == 0x07: # jmp
            address = self.fetch()
            address = (address << 8) | self.fetch()
            self.unconditional_jump(address)
            return "jmp %s" % self.getLabelName(address)

        elif opcode == 0x09: # djnz = Decrement and Jump if Not Zero
            var = self.fetch();
            offset = self.fetch()
            offset = (offset << 8) | self.fetch()
            varName = getVariableName(var)
            self.conditional_branch(offset)
            return "djnz [%s], %s" % (varName, self.getLabelName(offset))


if not (len(sys.argv) == 2):
    sys.exit(f"usage: {sys.argv[0]} <rom_file>")

entry_points = [0xef03c6]
rom_file = sys.argv[1]
disasm_dir = f"output"
LABELED_CINEMATIC_ENTRIES = {}
KNOWN_LABELS = {}
POSSIBLY_UNUSED_CODEBLOCKS = {}

RELOCATION_BLOCKS = (
    # physical,  logical, length 
    (0x000000,  0xe00000, 0x200000),
)
trace = TLCS900H_Trace(rom_file,
                       relocation_blocks=RELOCATION_BLOCKS,
                       subroutines=POSSIBLY_UNUSED_CODEBLOCKS.copy(),
                       labels=KNOWN_LABELS.copy(),
                       loglevel=0)
trace.run(entry_points)
#trace.print_ranges()
#trace.print_grouped_ranges()

trace.save_disassembly_listing(f"{rom_file}.asm")
