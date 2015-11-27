import pandas as pd
import numpy as np

y = np.random.randn(100)
x = np.random.randint(0,5,100)
z = np.random.randn(100)+3
data = pd.DataFrame(zip(y,x,z))
data.columns = ['y','x','z']

def get_dummies_deviation(df):
	"""
	get_dummies_deviation(df)
	Input: 
		df: dataframe containing only categorical variables
	Output:
		Dummified-dataframe using deviation encoding instead of base encoding 
			(base encoding makes the normalizing factor, deviation encoding
				seperates the entire group's effects away from the intercept)
	Requires:
		pandas imported as pd
		numpy imported as np
	---------
	Status: in progress
	Author: Thomas Roderick, thomas.roderick@gmail.com
	"""
	dum_ind = pd.get_dummies(df,columns=df.columns)
	base = dum_ind.columns[0]
	return dum_ind.sub(dum_ind[base],axis=0).drop(base,axis=1)

def ssw(A):
	# Returns the Samuel Stanley Wilks determinant (det of (I+A)**-1)
	return np.linalg.det(np.eye(len(A))+A)**(-1)

def pb(A):
	# Returns the Pillai-M.S.Bartlett trace (trace of (I+A)**-1)
	return np.trace(np.eye(len(A))+A)**(-1)

def lh(A):
	#Returns the Lawley-Hotelling trace (tr(A))
	return np.trace(A)

def rgr(A):
	#Returns Roy's greatest root, max_p (|\lambda_p|) = ||A||_{\infty}
	return max(abs(np.linalg.eig(A)[0]))

def groupby_demean(df,keys):
	"""
	groupby_deman(df,keys)
	Input: 
		df: dataframe containing only continuous variables and groupby variable keys (independent of index)
	Output:
		dataframe with continuous variables demeaned by the implicit multi-index defined by the categorical variables in the "keys" input
	Requires:
		pandas imported as pd
		numpy imported as np
	---------
	Status: in progress
	Author: Thomas Roderick, thomas.roderick@gmail.com
	"""
	q = df - df.groupby(keys).transform('mean')
	return q.drop(keys,axis=1)

def ancova(dependent,independent,covariates):
	"""
	ancova(dependent, independent, covariates)
	See Analysis of Covariances writeup (esp. formulation) at https://en.wikipedia.org/wiki/Analysis_of_covariance
	Inputs:
		dependent: Nx1 dataframe of an depedent variable
		independent: Nxk dataframe of categorical variables
		covariates: Continues independent variables. Will be demeaned grouped by the implicit multi-index 
			that the independent set defines 
	Outputs: 
		None

	Other: 
		prints the regression results of Pandas.stats.api.ols
	Relies on:
		groupby_demean
		get_dummies_deviaion
	------
	Status: In progress
	By: Thomas Roderick, thomas.roderick@gmail.com


	"""
	dum_ind = get_dummies_deviation(independent)
	covariates_dm = groupby_demean(pd.concat([covariates,independent],axis=1),list(independent.columns))
	i_ind = pd.concat([
			dum_ind,
			dependent,
			covariates_dm],axis=1)
	print pd.stats.api.ols(y=i_ind[list(dependent.columns)[0]],
		x=i_ind[list(covariates.columns)+list(dum_ind.columns)])

ancova(dependent=data[['y']],independent=data[['x']], covariates=data[['z']])
