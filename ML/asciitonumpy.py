import numpy as np
import codecs
from math import ceil
import csv


def toarray():
	array = np.array(np.loadtxt('global_2003_5min.asc'))
	return array

def creategeonumpy(xll,yll,cellsize,array,ncols,nrows,lonrange,latrange):
	newArr = []
	arrlist = array.tolist()
	
	c=0
	while c < ncols:
		for r in range(nrows):
			#print [c,r]
			if ( lonrange[0] < xll + (cellsize *(c-1)) < lonrange[1]):
				if (latrange[0] < yll + (cellsize * (nrows-r)) < latrange[1]): # slice
					newArr.append({'location-long':xll + cellsize *(c-1),'location-lat':yll + cellsize * (nrows-r),'htype':arrlist[r][c]}) #ref 2
		c += 1
	
	return newArr

def writetocsv(listofdicts,fieldnames):
	with open ('habitcsv.csv','w') as csvfd:
		wr = csv.DictWriter(csvfd,fieldnames=fieldnames)
		wr.writeheader()
		for row in listofdicts:
			wr.writerow(row)


def main():
	xll = -180.0
	yll = -64.0
	nrows = 1776
	ncols = 4320
	cellsize = 0.083


	array = toarray()
	
	habitatcsv = creategeonumpy(xll,yll,cellsize,array,ncols,nrows,(-6.022,-5.628),(38.946,39.085))
	writetocsv(habitatcsv,['location-long','location-lat','htype'])

main()

#ref1 http://www.software-matters.co.uk/importing-esri-into-access-database.html
#ref2 rs!x = xll + cs * (currcol - 1) ' origin of coordinate + size of cell * number of cells
       #rs!y = yll + cs * (nrows - currrow) ' origin of coordinate + size of cell * (number of rows between the bottom of the raster and the current row)
#ref3 http://www.landcover.org/data/lc/

