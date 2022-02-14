from TexGen.Core import *
import math
import cmath
path = "/gpfs01/home/emxghs/IAA3DWeaveProject"


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
	# assume rectangular cross section
	filamentArea = math.pi * ((0.0026)**2)
	#numberFilamentsWarp = 12000
	warpYarnArea = (filamentArea*numberFilamentsWarp)/0.9
	radius = math.sqrt(warpYarnArea/math.pi)
	warpWidth = 2*radius
	warpHeight = 0.5*radius
	#warpWidth = math.sqrt(warpYarnArea/2)
	#warpHeight = math.sqrt(2* warpYarnArea )

	#numberFilamentsWeft = 12000
	weftYarnArea = (filamentArea*numberFilamentsWeft)/0.9
	radius = math.sqrt(warpYarnArea/math.pi)
	weftWidth = 2*radius
	weftHeight = 0.5*radius
	#weftWidth = math.sqrt(weftYarnArea/2)
	#weftHeight = math.sqrt(2* weftYarnArea )

	#numberFilamentsBinder = 12000
	binderYarnArea = (filamentArea*numberFilamentsBinder)/0.9
	radius = math.sqrt(binderYarnArea/math.pi)
	binderWidth = 2*radius
	binderHeight = 0.5*radius
	#binderWidth = math.sqrt(binderYarnArea/2)
	#binderHeight = math.sqrt(2* binderYarnArea)
	
	
	cellWidth = weftWidth
	cellLength = warpWidth
	
	cellVolume = cellWidth  * cellLength * thickness
	cellFibreVolume = vf * cellVolume
	
	yarnfvf = (filamentArea * numberFilamentsWarp) / warpYarnArea
	#print("yarnfvf ", yarnfvf)
	
	cellYarnVolume = cellVolume * vf / yarnfvf
	#print("cellVolume ", cellVolume)
	#print("cellYarnVolume ", cellYarnVolume)
	#
	#calculate the yarn volume in each layer (both warp and weft)
	cellLayerVolume = (warpHeight + weftHeight)*cellLength*cellWidth
	#print("cellLayerVolume is ", cellLayerVolume)
	
	weftlayerVolume = weftHeight*cellLength*cellWidth
	
	numLayers = int(cellYarnVolume / cellLayerVolume)
	#print("numLayers = ", numLayers)
	




	#max number of possible layers with binder and additional weft layer accounted for - George check this is Kosher
	numWarpLayers = int((cellVolume) / cellLayerVolume) 
	#numWarpLayers = int(Volume / layerVolume)
	numWeftLayers = numWarpLayers + 1
	numLayers = numWarpLayers + numWeftLayers
	#print("numLayers = ", numLayers)
	
	#max binder volume given by numWarpLayers
	maxBinderVolume = (numWeftLayers)* binderHeight * cellWidth * cellLength
	maxnumBinderLayers = numWeftLayers 
		
	#maxSpacing - change this when you have worked out how to do this
	
	binderVolume=6*binderYarnArea*weftWidth
	
	minSpacing = binderHeight + weftWidth
	#upper = ((2*cellYarnVolume*yarnfvf + (binderVolume+cellYarnVolume)*yarnfvf)/(vf-tol*vf)) - cellVolume
	X = (1.5*cellYarnVolume*yarnfvf + (binderVolume)*yarnfvf)/0.8
	#print("X ", X)

	ans2 = (X)/(warpWidth*thickness) - weftWidth
	
	#print(ans2)
	maxSpacing = ans2
	
	#For now
	maxSpacing = minSpacing
	#print("maxSpacing ", maxSpacing)
	#print("minVolume ", 2*cellVolume)
	#print("actVolume ", (maxSpacing)*thickness*warpWidth + cellVolume)

	
	return numWeftLayers, numWarpLayers, maxnumBinderLayers, maxSpacing, warpHeight, warpWidth, weftHeight, weftWidth, binderHeight, binderWidth 
	
	
	
tol = 0.05
vf=0.6
thickness = 2
numberFilamentsWarp = 12000
numberFilamentsWeft = 12000
numberFilamentsBinder = 6000

numWeftLayers, numWarpLayers, maxnumBinderLayers, maxSpacing, warpHeight, warpWidth, weftHeight, weftWidth, binderHeight, binderWidth  = GenerateDesignSpace(path, vf, tol, thickness, numberFilamentsWarp, numberFilamentsWeft, numberFilamentsBinder)
	#pass numlayers from here into Matlab and have matlab generate the binder pattern + spacings that will set the unit cell size
modelName = "weave"
file = open(path + modelName +  "DesignSpace.txt", "a")
file.write(str(numWeftLayers) + ", " + str(maxnumBinderLayers)+ ", " + str(maxSpacing) + ", " + str(warpHeight) + ", " + str(warpWidth) + ", " + str(weftHeight) + ", " + str(weftWidth) + ", " + str(binderHeight) + ", " + str(binderWidth) + "\n")
file.close()