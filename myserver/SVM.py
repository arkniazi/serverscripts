from sklearn.svm import LinearSVC
import csv
import pickle
def update_list(list,size,x):
	while(size!=0):
		list.append(x)
		size = size-1
	return list

def load_data():
	inputData = []
	number = 0
	packageName = ""
	with open("/home/capk/FYP/server/myserver/Data/permission-data.txt") as fileBenign:
		for line in csv.reader(fileBenign,delimiter=','):
			if(number == 0):
				number = number+1
				packageName = line
				print packageName
			elif number==1:
				number = number+1
			else:
				line = [x for x in line if x]
				list = [int(i) for i in line]
				inputData.append(list)
	return packageName,inputData
def retrieve_model():
	file = open("/home/capk/FYP/Data/SVMTrainModel.pickle")
	mymodel = pickle.load(file)
	return mymodel

def predict_one(mymodel,data):
	result = mymodel.predict(data)
	print result
	return result
def svm():
	file = open('/home/capk/FYP/server/myserver/Data/svm-result.txt','w')
	packageName, inputData = load_data()
	packageName=" ".join(packageName)
	mymodel = retrieve_model()
#	print inputData
#	print len(inputData[0])
	file.write(packageName)
	file.write("\n")
	if(inputData!=[]):
		result = predict_one(mymodel,inputData)
		file.write("".join(str(x) for x in result))
		file.write("\n")




if __name__ == '__main__':
	svm()
