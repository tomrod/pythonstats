
## VECTORIZED VERSION
def Cramer(in1, in2):
	import math
	import numpy
	# Get the list of unique values for each input
	_, ind1 = unique(in1,return_index=True)
	unq1 = [in1[i] for i in sorted(ind1)]
	_, ind2 = unique(in2,return_index=True)
	unq2 = [in2[i] for i in sorted(ind2)]
	# Get the dimensions of the cross tab
	J = len(unq1)
	I = len(unq2)
	
	n = float(len(in1))
	# Create an array of zeros to fill with our frequency counts
	freq = numpy.zeros((I,J))
	#Get column and row sums to calculate expected values
	colsum = [0.0]*J
	rowsum = [0.0]*I

	for i in in1: colsum[unq1.index(i)] += 1
	for j in in2: rowsum[unq2.index(j)] += 1

	#Fill in the Frequency matrix
	for i in range(0, len(unq2)):
		slc = np.array(in2)==unq2[i]
		for j in range(0,len(unq1)):
			freq[i][j] = sum(numpy.array(in1)[slc]==unq1[j])
	df = min(J-1, I-1)

	#Calculated Expected values
	expected =  (matrix(rowsum).getT()*matrix(colsum))/float(n)

	#Calculate Cramer's V
	numerator = np.square(freq-expected)
	score = divide(numerator,expected)
	total = sum(score.sum(0))
	V = math.sqrt(float(total)/(n*df))
	return V
