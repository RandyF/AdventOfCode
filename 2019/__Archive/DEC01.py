from math import floor
print("Advent of Code 2019 - Day 1")


lModules = [99711, 136867, 97107, 108257, 57509, 129721, 139889, 91988, 54465, 129229, 59122, 97391, 57509, 70687, 72733, 137687, 123889, 53484, 71869, 144816, 83856, 131570, 68905, 66648, 124392, 59964, 80553, 93881, 56253, 76282, 127377, 110425, 59914, 76294, 81888, 88986, 132544, 70423, 124018, 122121, 53231, 148042, 108810, 75092, 60185, 94065, 130221, 121319, 87502, 90029, 86186, 113956, 143744, 133441, 142914, 112218, 66629, 144965, 135476, 111537, 51709, 125198, 72098, 79625, 105068, 119597, 71611, 122186, 95752, 51967, 117725, 52696, 100411, 70222, 66330, 119579, 116075, 91228, 68982, 114698, 125333, 139219, 148789, 101768, 97593, 100820, 75959, 128572, 99469, 102120, 76462, 128313, 123442, 83860, 76163, 142707, 66275, 70837, 137203, 71123]
#lModules = [14, 1969, 100756]


def CalcModuleFuel( iMass = 0 ):
	
	print("Calculating fuel requred for Mass %d... " % iMass )

	tReq = floor( iMass / 3 ) - 2
	
	print("  This mass requres %d fuel." % tReq )
	
	if tReq > 0:
		print("   But this fuel needs fuel!")
		tReq += CalcModuleFuel( tReq )
	else:
		print("    No More Fuel Requred!")
		tReq = 0
		
	return tReq


print("Calculating fuel for %d Modules" % len(lModules) )

iFuelRequired = 0

for iMod in lModules:

	iFuelRequired += CalcModuleFuel( iMod )
	
print("Total Fuel Required is %d" % iFuelRequired)