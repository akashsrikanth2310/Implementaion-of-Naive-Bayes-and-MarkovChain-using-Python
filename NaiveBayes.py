from math import pi
from csv import reader
from math import exp
from math import sqrt
import sys	
train_filename = sys.argv[1]	
test_filename = sys.argv[2]	
modelfile=sys.argv[3]	
resultfile=sys.argv[4]

def getthecsv(nameofthefilegiven):
	datavalss = list()
	with open(nameofthefilegiven, 'r') as file:
		readingvalesfromcsv = reader(file)
		for startvals in readingvalesfromcsv:
			if not startvals:
				continue
			datavalss.append(startvals)
	return datavalss

def classseperation(datavalss):
	diffrentiated = dict()
	for j in range(len(datavalss)):
		arayvalues = datavalss[j]
		valuesfortheclass = arayvalues[-1]
		if (valuesfortheclass not in diffrentiated):
			diffrentiated[valuesfortheclass] = list()
		diffrentiated[valuesfortheclass].append(arayvalues)
	return diffrentiated

def mean(valuesss):
	return sum(valuesss)/float(len(valuesss))

def stdev(valuesss):
	average = mean(valuesss)
	sqrtstdev = sum([(x-average)**2 for x in valuesss]) / float(len(valuesss)-1)
	return sqrt(sqrtstdev)

def finaldata(datavalss):
	finalvals = [(mean(column), stdev(column), len(column)) for column in zip(*datavalss)]
	del(finalvals[-1])
	return finalvals

def classfinall(datavalss):
	diffrentiated = classseperation(datavalss)
	finalvals = dict()
	for valuesfortheclass, rows in diffrentiated.items():
		finalvals[valuesfortheclass] = finaldata(rows)
	return finalvals

def probcalculations(x, mean, stdev):
    if stdev > 0:
        ex = exp(-((x-mean)**2 / (2 * stdev**2 )))
        return (1 / (sqrt(2 * pi) * stdev)) * ex
    return 1


def classprobcalculations(finalvals, startvals):
	countrows = sum([finalvals[label][0][2] for label in finalvals])
	probs = dict()
	for valuesfortheclass, class_summaries in finalvals.items():
		probs[valuesfortheclass] = finalvals[valuesfortheclass][0][2]/float(countrows)
		for j in range(len(class_summaries)):
			mean, stdev, _ = class_summaries[j]
			probs[valuesfortheclass] *= probcalculations(startvals[j], mean, stdev)
	return probs


def measure(finalvals, startvals):
	probs = classprobcalculations(finalvals, startvals)
	label_vals, high_pr = None, -1
	for valuesfortheclass, probability in probs.items():
		if label_vals is None or probability > high_pr:
			high_pr = probability
			label_vals = valuesfortheclass
	return label_vals

def classifernaive(train, test):
	finallss = classfinall(train)
	expectations = list()
	for startvals in test:
		given = measure(finallss, startvals)
		expectations.append([given - 1, startvals[-1] - 1])
	return(expectations)


datavalss = getthecsv(train_filename)
datafortrain = datavalss[1:]

datavalss = getthecsv(test_filename)
datafortest = datavalss[1:]

for startvals in range(len(datafortrain)):
    for col in range(len(datafortrain[startvals])):
        datafortrain[startvals][col] = int(datafortrain[startvals][col]) + 1
        
for startvals in range(len(datafortest)):
    for col in range(len(datafortest[startvals])):
        datafortest[startvals][col] = int(datafortest[startvals][col]) + 1
        
train_class_separated = classseperation(datafortrain)

modfile= open(modelfile, "a")	
class_summaries = classfinall(datafortrain)
class_probabilities = []	
for train_data in datafortrain:	
    class_probabilities.append(classprobcalculations(class_summaries,train_data))	
modfile.write("\nThe classwise probabilties are:\n")

new_class_probailties = []	
for i in range(len(class_probabilities)):	
    for j in class_probabilities[i]:	
        new_class_probailties.append({j-1 : class_probabilities[i][j] })	
modfile.write(str(new_class_probailties))	
resfile= open(resultfile, "a")



expectations = classifernaive(datafortrain, datafortest)
resfile.write("\nThe elements of [Predicted value, Actual Value]:\n")	
resfile.write(str(expectations))

matrixforconfusion = [[0, 0],[0, 0]]

for prediction_row_wise in expectations:
    if(prediction_row_wise[0] == prediction_row_wise[1]):
        if(prediction_row_wise[0] == 0):
            matrixforconfusion[0][0] += 1
        if(prediction_row_wise[0] == 1):
            matrixforconfusion[1][1] += 1
        
    if(prediction_row_wise[0] != prediction_row_wise[1]):
        if(prediction_row_wise[0] == 0):
            matrixforconfusion[0][1] += 1
        if(prediction_row_wise[0] == 1):
            matrixforconfusion[1][0] += 1

resfile.write("\nConfusion Matrix: (1 is -ve and 0 is +ve )\n")	
resfile.write(str(matrixforconfusion))	
modfile.close()	
resfile.close()
