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
from numpy import outer, tile
from numpy import sum as sm

def Cramer(var1, var2):
	"""
	Compute Cramer's V statistic for two Pandas series

	Parameters:
	----------
	var1, var2: Pandas series

	Returns:
	--------
	v : float
		The Cramer's V statistic of two categorical-variable series

	Status:
	-------	
	Cramer's V Implementation
	Author: Jesse Lund, jesselund86@gmail.com
	Date: 9/12/2015

	##Round 1##
	Comments: Thomas Roderick, thomas.roderick@gmail.com
	Date: 9/13/2015

	"""

	table = crosstab(var1,var2) #For Pandas: must have an index, can't just feed in two lists. This could be a sticking point. Might be better to do a check or roll our own crosstab implementation
	l,w = table.shape #save on a (small) function call here--reads in both outputs 
	df = min(l-1, w-1)
	colsum, rowsum = table.sum(0), table.sum(1) 
	n = float(l*w)
	expectmat = outer(rowsum,colsum)/n
	outmat = outer(table.sum(0),table.sum(1))/n #this works if same size
	return  sqrt((((table - expectmat)**2)/(expectmat*n*df)).sum().sum())
