#### A very simple negative selection algorithm
#### loosely inspired by the work here: http://johannes-textor.name/negativeselection.html
import random



### text data loader, returns list of strings in data as well as alphabet
def loadTextData(filename):
	with open(filename) as fp:
		fullString = fp.read()

	data = fullString.split("\n")
	for d in data:
		d.replace("\n","")
	alphabet = set()
	for c in fullString:
		if(not c == "\n"):
			alphabet.add(c)

	return data, list(alphabet)

class rchunkDetector:
	### r: length of chunk for matching
	### l: length of strings in training set
	### A: alphabet to generate detector string
	def __init__(self,r,l,A):
		self.r = r
		self.i = random.randint(0, l-r-1)
		self.l = l
		self.detectorString = ""
		for i in range(r):
			self.detectorString += A[random.randint(0,len(A)-1)]

	### tests if the detector string matches s
	def testDetector(self,s):
		if(s[self.i:] == self.detectorString):
			return True
		return False

class rcontigDetector:
	### r: length of substring for matching
	### l: length of strings in training se
	### A: alphabet to generate detector string
	def __init__(self,r,l,A):
		self.r = r
		self.l = l
		self.detectorString = ""
		for i in range(l):
			self.detectorString += A[random.randint(0,len(A)-1)]

	### tests if the detector string matches s
	def testDetector(self,s):
		for i in range(self.l-self.r+1):
			if(self.detectorString[i:self.r+i] in s):
				return True
		return False

#### training (r-chunk)
#### trains a population of detectors
#### input T: A list of training strings
#### input A: an alphabet with which to construct detectors
#### input n: The number of detectors in resulting population
#### input k: The number of strings to sample from T for training
#### input r: The length of the chunk for matching
#### input l: The length of strings in the training set
def trainRChunk(T, A, n, k, r, l, unique=True):
	detectors = set()
	Tlist = T.copy()

	while(len(detectors) < n):
		td = rchunkDetector(r,l,A)
		if(unique):
			while(td in detectors):
				td = rchunkDetector(r,l,A)
		random.shuffle(Tlist)
		goodDetector = True
		for i in range(k):
			if(td.testDetector(Tlist[i])):
				goodDetector = False
				break
		if(goodDetector):
			detectors.add(td)

	return list(detectors)

#### training (r-contiguous)
#### trains a population of detectors
#### input T: A list of training strings
#### input A: an alphabet with which to construct detectors
#### input n: The number of detectors in resulting population
#### input k: The number of strings to sample from T for training
#### input r: The length of the chunk for matching
def trainRContig(T, A, n, k, r, l, unique=True):
	detectors = set()

	while(len(detectors) < n):
		td = rcontigDetector(r,l,A)
		if(unique):
			while(td in detectors):
				td = rcontigDetector(r,l,A)
		random.shuffle(T)
		goodDetector = True
		for i in range(k):
			if(td.testDetector(T[i])):
				goodDetector = False
				break
		if(goodDetector):
			detectors.add(td)

	return list(detectors)