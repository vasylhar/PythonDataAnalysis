# --- Import necessary libraries
import operator
import numpy
import pylab
import matplotlib.pyplot as plt
from operator import itemgetter, attrgetter
import itertools
from collections import Counter


# --- Read the original data file 
with open("C:/sample_data.txt") as f:
    data = f.read()
	
# --- Parse data into manageable list and remove the header  	
data= data.split('\r')
data= [x.split('\t') for x in data]
del data[0]


#----------------------------
#-- MAKING SENSE OF DATA HERE
#----------------------------

#----------------------------
#-- 1) Parse "Year Funded" field, remove empty elements and transform into integers for a linear graph 
#      representing number of companies funded grouped by year, overlayed with NASDAQ price chart. Export file to txt to
#      load on Excel and produce the graph in Excel
#----------------------------

yearfunded = [int(x[3]) for x in data if x[3]!='']

d = {}
for i in yearfunded:
    d[i] = yearfunded.count(i)

yearfundedinfo = d.items()
yearfundedinfo = sorted(yearfundedinfo)
   
     #-- Getting rid of outliers earlier than 1975
yearfundedinfo = [str(x) for x in yearfundedinfo if x[0]>=1975]
	# -- writing the data into CSV for output with Excel Charts & Photoshop combination later
s = '\n'.join(yearfundedinfo)
s = s.replace(')','')
s = s.replace('(','')
f = open("D:/yearfunded.txt", "w"))
f.write(s)
f.close()
	
# ---------------------------
#-- 2) Parse "Company HQ" field, remove empty elements, and remove /"/ symbol.
#      Group countries by combined total funding     
#----------------------------

CompanyHQ = [x[2].replace('"', "") for x in data if x[2]!='']
       #-- Split into city and country
CompanyHQ = [x.split(',') for x in CompanyHQ]
       #-- Number of startups per country
Countries = [x[1].strip() for x in CompanyHQ]
d = {}
for i in Countries:
	d[i] = Countries.count(i)
Countries_Combined = d.items()
Countries_Combined = sorted(Countries_Combined, key=itemgetter(1),reverse=True)
Countries_Combined_List = [list(x) for x in Countries_Combined]

	    #-- Getting City+Country Data
UniqueCountries = list(set(Countries))
		 #-- Getting TotalFunding Data	
TotalFunding = [(x[6]) for x in data ]
		 #-- Assigning zeros for missing TotalFunding Data
for x in xrange(len(TotalFunding)):
	if TotalFunding[x]!='':
		TotalFunding[x] =int(TotalFunding[x])
	else:
		TotalFunding[x]=0
		
		 #-- Zipping Country and TotalFunding into one list
CountryFunding = range(len(UniqueCountries))
for x in xrange(len(UniqueCountries)):
	for y in xrange(len(Countries)):
		if UniqueCountries[x] == Countries[y]:
			CountryFunding[x] = CountryFunding[x] + TotalFunding[y]
			
CountryFundingFull = zip(UniqueCountries, CountryFunding)		 
CountryFundingFull = sorted(CountryFundingFull, key=itemgetter(1),reverse=True)

#----------------------------
#-- 3) Finding most common n=grams and aggregating their total funding levels
#      Print and copy/paste to to a tag cloud generator
#----------------------------
    Ngrams = [x[9].split(';') for x in data ]
	NgramsFlat = [x for sublist in Ngrams for x in sublist]
    BestNgrams = Counter(NgramsFlat)
	BestNgramsList = BestNgrams.items()
	BestNgramsList = sorted(BestNgramsList, key=itemgetter(1),reverse=True)
		 #-- year of founding based on N-gram ( mean average year) which have at least 2 different occurances
	totalfunding = [x[6] for x in data]
		 #-- 	
	NgramFunding=range(len(BestNgramsList))
for x in xrange(len(BestNgramsList)):
	if BestNgramsList[x][1] >=4:
		for y in range(len(Ngrams)):
			if BestNgramsList[x][0] in Ngrams[y]:
				if totalfunding[y]!='':
						NgramFunding[x] = NgramFunding[x] + int(totalfunding[y])
						
together2=zip(BestNgramsList, NgramFunding)
together2 = sorted(together2, key=itemgetter(1),reverse=True)
together2 =[(x[0][0], x[1]) for x in together2]
Top25MostFundedNgrams =together2[0:25]

#----------------------------
#-- 4) Finding most common Categories and aggregating their total funding levels. Writing data to a file for excel/tag cloud output					
#----------------------------					
					
Category = [x[1].split(';') for x in data ]
CategoryFlat = [x for sublist in Category for x in sublist]
BestCategory = Counter(CategoryFlat)
BestCategoryList = BestCategory.items()
BestCategoryList = sorted(BestCategoryList, key=itemgetter(1),reverse=True)
totalfunding = [x[6] for x in data]
	
CategoryFunding=range(len(BestCategoryList))
for x in xrange(len(BestCategoryList)):
	if BestCategoryList[x][1] >=4:
		for y in range(len(Category)):
			if BestCategoryList[x][0] in Category[y]:
				if totalfunding[y]!='':
						CategoryFunding[x] = CategoryFunding[x] + int(totalfunding[y])

together=zip(BestCategoryList, CategoryFunding)
together = sorted(together, key=itemgetter(1),reverse=True)
together =[(x[0][0], str(x[1])) for x in together]
together=[','.join(x) for x in together]
together='\n,'.join(together)
f = open("D:/categoryfunded.txt", "w")
f.write(together)
f.close()

#----------------------------	
#-- 5) Showing Categories of founded companies in spans of 5 years since 1975 based on the previous plot output. Output to screen.
#----------------------------	
YearlyCategoryList = range(8)

for i in range(8):
	YearlyCategoryList[i] = [list(x) for x in list(Counter([x[1] for x in data if x[3]!='' and int(x[3])>=(1975+i*5) and int(x[3])<=(1980+i*5)]).items())]
	for y in xrange(len(data)):
		for u in range(len(YearlyCategoryList[i])):
			if data[y][3]!='':	
				if data[y][1]==YearlyCategoryList[i][u][0] and int(data[y][3])>=(1975+i*5) and int(data[y][3])<=(1980+i*5):
					if data[y][6]!='' and data[y][6]!='0':
						YearlyCategoryList[i][u][1] =YearlyCategoryList[i][u][1]+int(data[y][6])
		YearlyCategoryList[i] = sorted(YearlyCategoryList[i], key=itemgetter(1),reverse=True)
		
		
#----------------------------		
#-- 6) Finding out correlation betweeen number of investors and total investments made (removing inadequate data)
#----------------------------

totalfunding = [x[6] for x in data]
numberinvestors =[x[8] for x in data]
together = [list(x) for x in zip (totalfunding,numberinvestors)]
filtered = [x for x in together if x[1]!='' and x[1]!='0' and x[0]!='' and x[0]!='0']
x = [int(x[0]) for x in filtered]
y = [int(zz[1]) for zz in filtered]
numpy.corrcoef(x,y)


#----------------------------
#-- 7) Finding most popular categories by funding from above and mapping them with placemarkers on google maps using long and lat
       #by exporting CVS file
#----------------------------
	 #-- socially related startups 	
	 
social =['Social Networking', 'Social Gaming','Online Social Interaction']
sociallist =[(x[4],x[5]) for x in data if x[1] in social]
sociallist=[','.join(x) for x in sociallist]
sociallist='\n'.join(sociallist)
f = open("D:/socialmap.csv", "w")
f.write(sociallist)
f.close()

	#-- not creating a class as there are only 2 output cases, hence just copy/paste
	
mobile=['Mobile Hardware and Software']
mobilelist =[(x[4],x[5]) for x in data if x[1] in mobile]
mobilelist=[','.join(x) for x in mobilelist]
mobilelist='\n'.join(mobilelist)
f = open("D:/mobilemap.csv", "w")
f.write(mobilelist)
f.close()
