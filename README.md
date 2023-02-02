This is a "smart" disassembler for the TLCS900H CPU, that I wrote so that I can use it to study the firmware of the Technics KN5000 music keyboard and hopefully be able to implement a working emulation driver for it on MAME.

The Neo Geo Pocket scene may also find this tool useful, as it uses the same CPU ;-)

The "smart" thing that this disassembler does is to trace all possible execution paths so that the resulting disassembly listing does not include data decoded as if it was code. There's a caveat, though. Some code use jump-tables. And the disassembler is not so smart. But at least it generates a few warnings to let you know where the jump tables are. And then once can inspect the code and add more entry-points to further improve the disasm output (**hint:** take a look at kn5000-disasm.py to see an example of this kind of usage).

This disassembler uses my own project ExecTrace, available at https://github.com/felipesanches/ExecTrace and also successfully used to disassemble bytecode of othe virtual machine of Eric Chahi's Another World game (See the tools at https://github.com/felipesanches/AnotherWorld_VMTools).

More info at https://forum.fiozera.com.br/t/technics-kn5000-homebrew-development/321

Also please take a look at https://github.com/felipesanches/kn5000_homebrew

