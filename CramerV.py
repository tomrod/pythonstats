"""
Cramer's V Implementation
Author: Jesse Lund, jesselund86@gmail.com
Date: 9/12/2015

Comments: Thomas Roderick, thomas.roderick@gmail.com

"""


from pandas import crosstab 
from math import sqrt
from numpy import outer, tile
from numpy import sum as sm

def Cramer(var1, var2):
	table = crosstab(var1,var2) #For Pandas: must have an index, can't just feed in two lists. This could be a sticking point. Might be better to do a check or roll our own crosstab implementation
	l,w = table.shape #save on a (small) function call here--reads in both outputs 
	df = min(l-1, w-1)
	colsum, rowsum = table.sum(0), table.sum(1) 
	n = float(l*w)
	expectmat = outer(rowsum,colsum)/n
	outmat = outer(table.sum(0),table.sum(1))/n #this works if same size
	return  sqrt((((table - expectmat)**2)/(expectmat*n*df)).sum().sum())
