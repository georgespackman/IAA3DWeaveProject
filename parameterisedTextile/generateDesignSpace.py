from TexGen.Core import *
import math
import cmath
path = "c:\\users\\emxghs\\desktop\\IAA3DWeaveProject\\parameterisedTextile\\"


def GenerateDesignSpace(path, vf, tol, thickness, numberFilamentsWarp, numberFilamentsWeft, numberFilamentsBinder):
	"""
	Function to set the design space based on user input. Takes the target volume fraction, volume fraction tolerance
	and thickness and returns the number of layers, actual volume fraction and spacings.
	
	Binder pattern and other geometrical values then generated by optimisation
	
	Args:
		path (file path) : File path
		vf (float) : Target fibre volume fraction of composite
		tol (float) : Acceptable tolerance for volume fraction
		thickness (float) : Target textile thickness
		numberFilamentsWarp (int) : Filament count of warp yarn
		numberFilamentsWeft (int) : Filament count of warp yarn
		numberFilamentsBinder (int) : Filament count of warp yarn
		
	Returns:
		numWeftLayers, numWarpLayers, maxnumBinderLayers, maxSpacing, warpHeight, warpWidth, weftHeight, weftWidth, binderHeight, binderWidth
	
	"""
	#size of single cell dependent on the yarn type
	#Assume for now the yarn type is fized at 12k
	#yarn size could be parameter, initally assuming all single type of yarn, below is Hexcel IM7 tow, max packing fraction of 0.9
	filamentArea = math.pi * ((0.0026)**2)
	#numberFilamentsWarp = 12000
	warpYarnArea = (filamentArea*numberFilamentsWarp)/0.9
	radius = math.sqrt(warpYarnArea/math.pi)
	warpWidth = 4*radius
	warpHeight = 1*radius

	#numberFilamentsWeft = 12000
	weftYarnArea = (filamentArea*numberFilamentsWeft)/0.9
	radius = math.sqrt(warpYarnArea/math.pi)
	weftWidth = 4*radius
	weftHeight = 1*radius

	#numberFilamentsBinder = 12000
	binderYarnArea = (filamentArea*numberFilamentsBinder)/0.9
	radius = math.sqrt(warpYarnArea/math.pi)
	binderWidth = 4*radius
	binderHeight = 1*radius
	
	
	cellWidth = weftWidth
	cellLength = warpWidth
	
	cellVolume = cellWidth  * cellLength * thickness
	cellFibreVolume = vf * cellVolume
	
	yarnfvf = (filamentArea * numberFilamentsWarp) / warpYarnArea
	print("yarnfvf ", yarnfvf)
	
	cellYarnVolume = cellVolume * vf / yarnfvf
	print("cellVolume ", cellVolume)
	print("cellYarnVolume ", cellYarnVolume)
	
	#calculate the yarn volume in each layer (both warp and weft)
	cellLayerVolume = (warpHeight + weftHeight)*cellLength*cellWidth
	print("cellLayerVolume is ", cellLayerVolume)
	
	weftlayerVolume = weftHeight*cellLength*cellWidth
	
	numLayers = int(cellYarnVolume / cellLayerVolume)
	print("numLayers = ", numLayers)
	




	#max number of possible layers with binder and additional weft layer accounted for - George check this is Kosher
	numWarpLayers = int((cellVolume) / cellLayerVolume) 
	#numWarpLayers = int(Volume / layerVolume)
	numWeftLayers = numWarpLayers + 1
	numLayers = numWarpLayers + numWeftLayers
	print("numLayers = ", numLayers)
	
	#max binder volume given by numWarpLayers
	maxBinderVolume = (numWeftLayers)* binderHeight * cellWidth * cellLength
	maxnumBinderLayers = numWeftLayers 
		
	#maxSpacing - change this when you have worked out how to do this
	
	binderVolume=binderYarnArea*weftWidth
	
	minSpacing = binderHeight
	#upper = ((2*cellYarnVolume*yarnfvf + (binderVolume+cellYarnVolume)*yarnfvf)/(vf-tol*vf)) - cellVolume
	X = (1.5*cellYarnVolume*yarnfvf + (binderVolume)*yarnfvf)/0.8
	print("X ", X)
	#X = (2*(weftWidth))/0.6
	# a=1
	# b=4*weftWidth
	# c= (X/thickness) - 4*(weftWidth)**2
	
	
		
	# # calculating  the discriminant
	# dis = (b**2) - (4 * a*c)
	# print(dis)
	  
	# # find two results
	# ans1 = (-b-cmath.sqrt(dis))/(2 * a)
	# ans2 = (-b + cmath.sqrt(dis))/(2 * a)
	
	ans2 = (X)/(warpWidth*thickness) - weftWidth
	
	print(ans2)
	maxSpacing = ans2
	print("maxSpacing ", maxSpacing)
	print("minVolume ", 2*cellVolume)
	print("actVolume ", (maxSpacing)*thickness*warpWidth + cellVolume)

	
	return numWeftLayers, numWarpLayers, maxnumBinderLayers, maxSpacing, warpHeight, warpWidth, weftHeight, weftWidth, binderHeight, binderWidth 
	
	
	
tol = 0.05
vf=0.6
thickness = 4
numberFilamentsWarp = 12000
numberFilamentsWeft = 12000
numberFilamentsBinder = 12000

numWeftLayers, numWarpLayers, maxnumBinderLayers, maxSpacing, warpHeight, warpWidth, weftHeight, weftWidth, binderHeight, binderWidth  = GenerateDesignSpace(path, vf, tol, thickness, numberFilamentsWarp, numberFilamentsWeft, numberFilamentsBinder)
	#pass numlayers from here into Matlab and have matlab generate the binder pattern + spacings that will set the unit cell size
modelName = "weave"
file = open(path + modelName +  "DesignSpace.txt", "a")
file.write(str(numWeftLayers) + ", " + str(maxnumBinderLayers)+ ", " + str(maxSpacing) + ", " + str(warpHeight) + ", " + str(warpWidth) + ", " + str(weftHeight) + ", " + str(weftWidth) + ", " + str(binderHeight) + ", " + str(binderWidth) + "\n")
file.close()