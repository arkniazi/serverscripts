import fnmatch
import re
def exist(per,data):
	data = data.split(",")

	for d in data:
		if d==per:
			return True
		if re.search(d+"*",per):
			return True
	return False
	pass

def generate():
	datafile = open("/home/capk/FYP/server/myserver/Data/permission-data.txt","w")

	with open("/home/capk/FYP/server/myserver/Data/permission.txt") as f:
		filedata = f.readlines()

	with open('/home/capk/FYP/Data/android_permission_list') as f:
		permissions = f.readlines()
	c = 0
	packageName= ""
	for d in filedata:
		if c==0:
			c = c+1
			packageName = d
		else:
			data = []
			for p in permissions:
				if exist(p,d):
					data.append("1,")
				else:
					data.append("0,")
			datafile.write(packageName+"\n")
			datafile.write(''.join(data))
			datafile.write("\n")

if __name__ == '__main__':
	generate()
