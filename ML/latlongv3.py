# to build dataset master sheet
# wirtes into a 

import os
import pandas as pd 
import sys
import numpy as np 
import math
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import multiprocessing
import csv
import time

def get_sample(df):
		df2 = df.sample(frac=0.01)
		#print df2[location-long],df2[location-lat]
		df2.to_csv('Continental black-tailed godwits.csv')
		return df2

def writetocsv(listofdicts,fieldnames):
	with open ('cummulative.csv','w') as csvfd:
		wr = csv.DictWriter(csvfd,fieldnames=fieldnames)
		wr.writeheader()
		for row in listofdicts:
			wr.writerow(row)

def writefromcsv(csvfile,fieldnames):
	listofrows = []
	with open('cummulative.csv') as csvfd:
		reader = csv.DictReader(csvfd)
		for row in reader:
			#print row
			listofrows.append(row)
	return listofrows

def gencords(lonrange,latrange): #generate 1000 * 1000 lon,lat rect patch
	lons = np.arange(lonrange[0],lonrange[1],0.01).tolist() #converts array to list
	lats = np.arange(latrange[0],latrange[1],0.01).tolist()
	cords={}
	cordslist = []
	for lon in lons:
		for lat in lats:
			#cords[(lon,lat)]={'visible':0} # lon,lat and default visibility, this needs to be extended to show 
			cordslist.append({'location-long':lon,'location-lat':lat,'visible':0,'timestamp':0,'htype':0})
	#return cords # return as np matrix
	writetocsv(cordslist,['location-long','location-lat','visible','timestamp','htype'])
	#return cordslist
	
def fromcsv(filepath, colnames): #returns the lat and long from the file. for example migration file
	df  = pd.read_csv(filepath)
	#df = get_sample(df)
	return df.as_matrix(columns =colnames).tolist() #df ->np array ->list

'''
def nearestnei(cords,arr2): # this is where interpolation can be made. 
	# will multithreading improvise this?
	cordlist = []
	for cord2 in arr2: 
		nearnei = [10,[0,0]] # neinei[0] = distance , nearnei[1] = actual [lon,lat]
		for cord1 in cords.keys():
			dist = math.sqrt(math.pow((cord2[0]-cord1[0]),2) + math.pow((cord2[1]-cord1[1]),2)) # euclidean distance lon2-lon1, lat1-lat1
			#print dist,cord2,cord1
			if dist < nearnei[0] :
				nearnei[0] = dist
				nearnei[1][0],nearnei[1][1] = cord1[0],cord1[1]
		cords[(nearnei[1][0],nearnei[1][1])]['visible'] = 1 # to mark app location where the bird was sighted.
		#print cords[(nearnei[1][0],nearnei[1][1])],(nearnei[1][0],nearnei[1][1])
		cordlist.append((nearnei[1][0],nearnei[1][1]))
	return cordlist
		
	#cumcsv(cords)

	#print cords
'''
def nearestnei(cordslist,arr2): # this is where interpolation can be made. 
	# will multithreading improvise this?
	cordlist = []
	idx = 0
	for cord2 in arr2: 
		nearnei = [10,[0,0],idx] # neinei[0] = distance , nearnei[1] = actual [lon,lat]
		for i in range(len(cordslist)):
			dist = math.sqrt(math.pow((cord2[0]-float(cordslist[i]['location-long'])),2) + math.pow((cord2[1]-float(cordslist[i]['location-lat'])),2)) # euclidean distance lon2-lon1, lat1-lat1
			#print dist,cord2,cord1
			if dist < nearnei[0] :
				nearnei[0] = dist
				nearnei[1][0],nearnei[1][1] = cordslist[i]['location-long'],cordslist[i]['location-lat']
				idx = i
		cordslist[idx]['visible'] = 1 # to mark app location where the bird was sighted.
		cordslist[idx]['timestamp'] = time.strptime(cord2[2][:-4],"%Y-%m-%d %H:%M:%S").tm_mon
		
		#print cords[(nearnei[1][0],nearnei[1][1])],(nearnei[1][0],nearnei[1][1])
		cordlist.append((cordslist[idx]['location-long'],cordslist[idx]['location-lat']))
	writetocsv(cordslist,['location-long','location-lat','visible','timestamp','htype'])
	return cordlist
	
def nearesthab(cordslist,arr3):
    cordlist = []
    idx = 0
    for cord2 in arr3:
        nearhab = [100,[0,0],idx]
        for i in range(len(cordslist)):
            dist = math.sqrt(math.pow((cord2[0]-float(cordslist[i]['location-long'])),2) + math.pow((cord2[1]-float(cordslist[i]['location-lat'])),2))
            if dist < nearhab[0]:
                nearhab[0] = dist
                nearhab[1][0],nearhab[1][1] = cordslist[i]['location-long'],cordslist[i]['location-lat']
                idx = i
        cordslist[idx]['htype']=cord2[2]
        writetocsv(cordslist,['location-long','location-lat','visible','timestamp','htype'])
        
            

def plot_map(arr2): # projecting on a base map (the datapoint is lat,lon)
	numar = np.array(arr2)
	bmap = Basemap(lat_0=0,lon_0=0) #central latitute,central longitude
	bmap.drawcoastlines() #to draw coastlines
	bmap.drawmapboundary() #draw a line around the map region
	blon,blat=bmap(numar[:,0],numar[:,1]) # before using tthe values. they need to be transformed  #ref1
		#numar[:,1] is the first col, #numar[:,2] is the second column of the numpy array
	bmap.plot(blon,blat,marker='o',color='k')
	plt.show()


def main():
    
	filepath2 = os.path.join('~','Desktop','everything nice','Programming','hackathon','SpaceApps2017','submission','samplesubs','blacktailgodwit_short.csv') # species tracks #continentail black-tailed godwits
	
	filepath1 = os.path.join('~','Desktop','everything nice','Programming','hackathon','SpaceApps2017','submission','samplesubs','cummulative.csv') # habitats
	filepath3 = os.path.join('~','Desktop','everything nice','Programming','hackathon','SpaceApps2017','submission','samplesubs','habitcsv.csv') 
	gencords([-6.022,-5.628],[38.946,39.085])
	arr1 = writefromcsv(filepath1,['location-long','location-lat','visible','timestamp','htype'])
	arr2 = fromcsv(filepath2,['location-long','location-lat','timestamp'])
	#print arr2
	arr3 = fromcsv(filepath3,['location-long','location-lat','htype'])
	print "approximating..."
	cordl = nearestnei(arr1,arr2)
	print "habitat..."
	nearesthab(arr1,arr3)
	
	plot_map(arr2)
	#plot_map(cordl)
main()
