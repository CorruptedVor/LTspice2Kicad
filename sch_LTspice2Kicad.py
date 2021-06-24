#! usr/bin/python
# -*- coding: ISO-8859-1 -*-

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

#  Written by : Laurent CHARRIER
#  last change: 2017, Oct 30.
#
#  To be done : - position of the name and reference
#               - hierarchical design
#               - pins of hierarchical design
#

import sys,re,os,time

# function to find locaion of each space character in each line
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

in_file = sys.argv[1]
indir = in_file.split("/")
out_file = "LTspice_" + indir[len(indir)-1]

indir = os.getcwd().split("/")
LTspice_lib = ["LTspice_"+indir[len(indir)-1],"LTspice_sym","LTspice_Comparators","LTSpice_devices","LTspice_Digital","LTspice_FilterProducts","LTspice_Misc","LTspice_Opamps","LTspice_Optos","LTspice_PowerProducts","LTspice_References","LTspice_SpecialFunctions"]
Kicad_lib = ["power","device","switches","relays","motors","transistors","conn","linear","regul","74xx","cmos4000","adc-dac","memory","xilinx","microcontrollers","dsp","microchip","analog_switches","motorola","texas","intel","audio","interface","digital-audio","philips","display","cypress","siliconi","opto","atmel","contrib","valves"]

#  .pro  export file
out_file1 = out_file.replace(".asc",".pro")
outfl = open(out_file1,"w");
outfl.write("update="+time.strftime('%d/%m/%y %H:%M',time.localtime())+"\n")
outfl.write("version=1\nlast_client=eeschema\n[general]\nversion=1\nRootSch=\nBoardNm=\n[pcbnew]\nversion=1\nLastNetListRead=\nUseCmpFile=1\nPadDrill=0.60\nPadDrillOvalY=0.60\nPadSizeH=1.50\nPadSizeV=1.50\nPcbTextSizeV=1.50\nPcbTextSizeH=1.50\nPcbTextThickness=0.30\nModuleTextSizeV=1.00\nModuleTextSizeH=1.00\nModuleTextSizeThickness=0.15\nSolderMaskClearance=0.00\nSolderMaskMinWidth=0.00\nDrawSegmentWidth=0.20\nBoardOutlineThickness=0.10\nModuleOutlineThickness=0.15\n[cvpcb]\nversion=1\nNetIExt=net\n[eeschema]\nversion=1\nLibDir=\n[eeschema/libraries]\n")
for i in range(0,len(LTspice_lib)):
	outfl.write("LibName"+str(i+1)+"="+LTspice_lib[i]+"\n")
for j in range(0,len(Kicad_lib)):
	outfl.write("LibName"+str(j+i+2)+"="+Kicad_lib[j]+"\n")
outfl.write("\n")
outfl.close()

#  .sch  export file
out_file = out_file.replace(".asc",".sch")
outfl = open(out_file,"w");
outfl.write("EESchema Schematic File Version 2\n")
for i in range(0,len(LTspice_lib)):
	outfl.write("LIBS:"+LTspice_lib[i]+"\n")
for i in range(0,len(Kicad_lib)):
	outfl.write("LIBS:"+Kicad_lib[i]+"\n")
outfl.write("EELAYER 25 0\nEELAYER END\n")

infl = open(in_file,"r",encoding="latin-1", errors="ignore");
lines = infl.readlines()
infl.close()

wireX1 = []
wireY1 = []
wireX2 = []
wireY2 = []
conn_X = []
conn_Y = []
flag_text = []
flag_X = []
flag_Y = []
text_text = []
text_orient = []
text_X = []
text_Y = []
rectangleX1 = []
rectangleY1 = []
rectangleX2 = []
rectangleY2 = []
sym_sym = []
sym_X = []
sym_Y = []
sym_orient = []
sym_name = []
sym_value = []
sym_spice = []
sym_i = 0
sname = 0
svalue = 0
sspice = 0

lnn = 0
# read the LTspice library line by line :
for line1 in lines:
	lnn = lnn + 1
	line1 = line1.rstrip('\n')	
	line1 = line1.rstrip('\r')
	# print(line1)
	spc = list(find_all(line1," "))  # find all space locations to split the variables of the line
	
	if re.match(r"^WIRE *", line1) is not None:
		wireX1.append(int(3.125*int(line1[spc[0]:spc[1]])))
		wireY1.append(int(3.125*int(line1[spc[1]:spc[2]])))
		wireX2.append(int(3.125*int(line1[spc[2]:spc[3]])))
		wireY2.append(int(3.125*int(line1[spc[3]:])))
	
	if re.match(r"^FLAG *", line1) is not None:
		flag_text.append(line1[spc[2]+1:])
		flag_X.append(int(3.125*int(line1[spc[0]:spc[1]])))
		flag_Y.append(int(3.125*int(line1[spc[1]:spc[2]])))
	
	if re.match(r"^TEXT *", line1) is not None:
		text_text.append(line1[spc[4]+2:])
		text_orient.append(line1[spc[2]+1:spc[3]])
		text_X.append(int(3.125*int(line1[spc[0]:spc[1]])))
		text_Y.append(int(3.125*int(line1[spc[1]:spc[2]])))

	if re.match(r"^RECTANGLE *", line1) is not None:
		rectangleX1.append(int(3.125*int(line1[spc[1]:spc[2]])))
		rectangleY1.append(int(3.125*int(line1[spc[2]:spc[3]])))
		rectangleX2.append(int(3.125*int(line1[spc[3]:spc[4]])))
		if len(spc) == 5 :
			rectangleY2.append(int(3.125*int(line1[spc[4]:])))
		else :
			rectangleY2.append(int(3.125*int(line1[spc[4]:spc[5]])))

	if re.match(r"^SYMBOL *", line1) is not None:
		if sname < sym_i :
			sym_name.append(sym_sym[sym_i-1])
			sname = sname+1
		if svalue < sym_i :
			sym_value.append(sym_sym[sym_i-1])
			svalue = svalue+1
		if sspice < sym_i :
			sym_spice.append(" ")
			sspice = sspice+1
		sym_i = sym_i + 1
		sym_sym.append(line1[spc[0]+1:spc[1]])
		sym_X.append(int(3.125*int(line1[spc[1]:spc[2]])))
		sym_Y.append(int(3.125*int(line1[spc[2]:spc[3]])))
		sym_orient.append(line1[spc[3]+1:])
	if re.match(r"^SYMATTR InstName *", line1) is not None:
		sname = sname + 1
		sym_name.append(line1[spc[1]+1:])
		print(str(lnn) + " : sym_name : "+sym_name[sname-1])
	if re.match(r"^SYMATTR Value *", line1) is not None:
		svalue = svalue + 1
		sym_value.append(line1[spc[1]+1:])
	if re.match(r"^SYMATTR SpiceLine *", line1) is not None:
		sspice = sspice + 1
		sym_spice.append(line1[spc[1]+1:])
		
if sname < sym_i :
	sym_name.append(sym_sym[sym_i-1])
	sname = sname+1
	print("add sname")
if svalue < sym_i :
	sym_value.append(sym_sym[sym_i-1])
	svalue = svalue+1
if sspice < sym_i :
	sym_spice.append(" ")
	sspice = sspice+1

outfl.write("$Descr A4 11693 8268\n")
outfl.write("encoding utf-8\nSheet 1 1\nTitle \""+out_file.replace(".sch","")+"\"\nDate \""+time.strftime('%d/%m/%y %H:%M',time.localtime())+"\"\nRev \"1.0\"\nComp \"\"\nComment1 \"Converted from LTspice\"\nComment2 \"\"\nComment3 \"\"\nComment4 \"\"\n$EndDescr\n")

# export each components
for i in range(0,len(sym_sym)):
	outfl.write("$Comp\nL "+sym_sym[i]+" "+sym_name[i]+"\n")
	outfl.write("U 1 1 59E9ACCC\n")
	outfl.write("P "+str(sym_X[i])+" "+str(sym_Y[i])+"\n")
	outfl.write("F 0 \""+sym_name[i]+"\" H "+str(sym_X[i]+100)+" "+str(sym_Y[i]-100)+" 50  0000 L CNN\n")
	outfl.write("F 1 \""+sym_value[i]+"\" H "+str(sym_X[i]+100)+" "+str(sym_Y[i]-200)+" 50  0000 L CNN\n")
	outfl.write("	1    "+str(sym_X[i])+" "+str(sym_Y[i])+"\n")
	if sym_orient[i]=="R0"   : outfl.write("	 1    0    0    -1  \n")
	if sym_orient[i]=="R90"  : outfl.write("	 0    1    1     0  \n")
	if sym_orient[i]=="R180" : outfl.write("	-1    0    0     1  \n")
	if sym_orient[i]=="R270" : outfl.write("	 0   -1   -1     0  \n")
	if sym_orient[i]=="M0"   : outfl.write("	-1    0    0    -1  \n")
	if sym_orient[i]=="M90"  : outfl.write("	 0   -1    1     0  \n")
	if sym_orient[i]=="M180" : outfl.write("	 1    0    0     1  \n")
	if sym_orient[i]=="M270" : outfl.write("	 0    1   -1     0  \n")
	outfl.write("$EndComp\n")
# export each wires and calculate connections
for i in range(0,len(wireX1)):
	outfl.write("Wire Wire Line\n	"+str(wireX1[i])+" "+str(wireY1[i])+" "+str(wireX2[i])+" "+str(wireY2[i])+"\n")
# add a connection if at least 3 wires have the same end point
for i in range(0,len(wireX1)-1):
	nb_conn = 0
	conn_rgstr = 0
	for j in range(i+1,len(wireX1)):
		if ((wireX1[i]==wireX1[j] and wireY1[i]==wireY1[j]) or (wireX1[i]==wireX2[j] and wireY1[i]==wireY2[j])) :
			nb_conn = nb_conn + 1
	for j in range(0,len(conn_X)):
		if (wireX1[i]==conn_X[j] and wireY1[i]==conn_Y[j]) :
			conn_rgstr = 1
	if (nb_conn > 1  and  conn_rgstr==0):
		outfl.write("Connection ~ "+str(wireX1[i])+" "+str(wireY1[i])+"\n")
# add a connection if an end of wire is over another wire
# >> idea not needed

# export each wire annotation and pins
for i in range(0,len(flag_text)):
	if flag_text[i]=="0" :
		outfl.write("$Comp\nL GND #PWR?\nU 1 1 59E9AE0E\nP "+str(flag_X[i])+" "+str(flag_Y[i])+"\nF 0 \"#PWR?\" H "+str(flag_X[i])+" "+str(flag_Y[i]-250)+" 50  0001 C CNN\nF 1 \"GND\" H "+str(flag_X[i])+" "+str(flag_Y[i]-150)+" 50  0000 C CNN\n	1    "+str(flag_X[i])+" "+str(flag_Y[i])+"\n	1    0    0    -1\n$EndComp\n")
	else :
		outfl.write("Text Label "+str(flag_X[i])+" "+str(flag_Y[i])+" 0    60   ~ 0\n"+flag_text[i]+"\n")

# export each free text lines
for i in range(0,len(text_text)):
	orient_text = 0
	off_text = 150
	if text_orient[i]=="Right" : 
		orient_text = 2
	if (text_orient[i]=="Top" or text_orient[i]=="Bottom"): 
		off_text = 0
	outfl.write("Text Notes "+str(text_X[i])+" "+str(text_Y[i]+off_text+75*text_text[i].count('\\n'))+" "+str(orient_text)+"   50   ~ 0\n"+text_text[i]+"\n")

# export each free rectangle (no hashed line in Kicad)
for i in range(0,len(rectangleX1)):
	outfl.write("Wire Notes Line\n	"+str(rectangleX1[i])+" "+str(rectangleY1[i])+" "+str(rectangleX2[i])+" "+str(rectangleY1[i])+"\n")
	outfl.write("Wire Notes Line\n	"+str(rectangleX2[i])+" "+str(rectangleY1[i])+" "+str(rectangleX2[i])+" "+str(rectangleY2[i])+"\n")
	outfl.write("Wire Notes Line\n	"+str(rectangleX2[i])+" "+str(rectangleY2[i])+" "+str(rectangleX1[i])+" "+str(rectangleY2[i])+"\n")
	outfl.write("Wire Notes Line\n	"+str(rectangleX1[i])+" "+str(rectangleY2[i])+" "+str(rectangleX1[i])+" "+str(rectangleY1[i])+"\n")

outfl.write("$EndSCHEMATC")
outfl.close()
