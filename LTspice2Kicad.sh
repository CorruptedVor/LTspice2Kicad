#!/bin/sh

echo creating KiCAD compatible LTspice libraries

python lib_LTspice2Kicad.py "."
python lib_LTspice2Kicad.py "~/Documents/LTspiceXVII/lib/sym"
python lib_LTspice2Kicad.py "~/Documents/LTspiceXVII/lib/sym/Comparators"
#python lib_LTspice2Kicad.py "~/Documents/LTspiceXVII/lib/sym/devices" it doesn't exist??
python lib_LTspice2Kicad.py "~/Documents/LTspiceXVII/lib/sym/Digital"
python lib_LTspice2Kicad.py "~/Documents/LTspiceXVII/lib/sym/FilterProducts"
python lib_LTspice2Kicad.py "~/Documents/LTspiceXVII/lib/sym/Misc"
python lib_LTspice2Kicad.py "~/Documents/LTspiceXVII/lib/sym/OpAmps"
python lib_LTspice2Kicad.py "~/Documents/LTspiceXVII/lib/sym/Optos"
python lib_LTspice2Kicad.py "~/Documents/LTspiceXVII/lib/sym/PowerProducts"
python lib_LTspice2Kicad.py "~/Documents/LTspiceXVII/lib/sym/References"
python lib_LTspice2Kicad.py "~/Documents/LTspiceXVII/lib/sym/SpecialFunctions"
