"""
# Copyright (c) Jesse Lund and Thomas Roderick.  All rights reserved
#
# Disclaimer
#
# This software is provided "as-is".  There are no expressed or implied
# warranties of any kind, including, but not limited to, the warranties
# of merchantability and fitness for a given application.  In no event
# shall Gary Strangman be liable for any direct, indirect, incidental,
# special, exemplary or consequential damages (including, but not limited
# to, loss of use, data or profits, or business interruption) however
# caused and on any theory of liability, whether in contract, strict
# liability or tort (including negligence or otherwise) arising in any way
# out of the use of this software, even if advised of the possibility of
# such damage.
# 
# 
# Disclaimers:  The function list is obviously incomplete and, worse, the
# functions are not optimized.  All functions have been tested (some more
# so than others), but they are far from bulletproof.  Thus, as with any
# free software, no warranty or guarantee is expressed or implied. :-)  A
# few extra functions that don't appear in the list below can be found by
# interested treasure-hunters.  These functions don't necessarily have
# both list and array versions but were deemed useful.
"""
 


from pandas import crosstab
from math import sqrt
from numpy import unique


def crosstabulate(in1,in2):
	"""
	Compute Cramer's V statistic for two Pandas series

	Parameters:
	----------
	var1, var2: two lists with any type of level

	Returns:
	--------
	freq : 2D array 
		A 2D array of size (I,J) for frequency counts 
		where I is the number of unqiue elements of 
		list var1 and J for var2

	perc : 2D array 
		A 2D array of size (I,J) for percent of all counts 
		where I is the number of unqiue elements of 
		list var1 and J for var2

		A 2D array of size (I,J) for column percentages 
		where I is the number of unqiue elements of 
		list var1 and J for var2

	rowp : 2D array 
		A 2D array of size (I,J) for row percentages 
		where I is the number of unqiue elements of 
		list var1 and J for var2

	Status:
	-------	
	Basic testing

	Author:
	-------
	Tom Roderick, thomas.roderick@gmail.com
	9/14/2015
	"""
	_, ind1 = unique(in1,return_index=True)
	unq1 = [in1[i] for i in ind1]
	_, ind2 = unique(in2,return_index=True)
	unq2 = [in2[i] for i in ind2]
	unq1 = sorted(unq1)
	unq2 = sorted(unq2)
	I = len(unq1)
	J = len(unq2)
	freq = [[0.0 for x in range(J)] for y in range(I)]
	perc = [[0.0 for x in range(J)] for y in range(I)]
	rowp = [[0.0 for x in range(J)] for y in range(I)]
	colp = [[0.0 for x in range(J)] for y in range(I)]
	n = 0
	for k in zip(in1,in2):
		n+= 1
		k0 = unq1.index(k[0])
		k1 = unq2.index(k[1])
		freq[k0][k1]+=1
	rowsum = [sum(k) for k in freq]
	colsum = [sum(k) for k in zip(*freq)]
	for i in range(I):
		for j in range(J):
			colp[i][j] = freq[i][j] / rowsum[i]
			rowp[i][j] = freq[i][j] / colsum[j]
			perc[i][j] = freq[i][j] / n
	return freq,perc,colp,rowp


def Cramer(var1, var2):
	"""
	Compute Cramer's V statistic for two Pandas series

	Parameters:
	----------
	var1, var2: Pandas series

	Returns:
	--------
	v : float
		The Cramer's V statistic of two categorical-variable Pandas series

	Status:
	-------	
	Cramer's V Implementation
	Author: Jesse Lund, jesselund86@gmail.com
	Date: 9/12/2015

	##Round 1##
	Comments & Edits: Thomas Roderick, thomas.roderick@gmail.com
	Date: 9/13/2015

	##Round 2##
	Edits: Thomas Roderick, thomas.roderick@gmail.com
	Date 9/14/2015
	**adapted from initial code from Jesse Lund

	"""
	table = crosstab(var1,var2)
	l,w = table.shape
	colsum, rowsum = table.sum(0), table.sum(1)
	df = min(l-1, w-1)
	n = sum(rowsum)
	score = 0
	for i in range(0,table.shape[0]):
		for j in range(0,table.shape[1]):
			observed = table.iloc[i][j]
			expected = (rowsum[i]/float(n))*colsum[j]
			score+=((observed-expected)**2)/expected
	return sqrt(float(score)/(n*df))

def CMHtest():
	"""
	In progress
	"""
	return None