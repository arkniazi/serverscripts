import MySQLdb
hostname = 'localhost'
username = 'root'
password = '4205'
database = 'dagon'
filename = '/home/capk/FYP/server/myserver/Data/hashes.txt'
class mysql:
	def main():
        	conn = MySQLdb.connect(hostname,username,password,database)
        	cursor = conn.cursor()
        	with open(filename) as f:
                	data = f.readlines()
        	for d in data:
                	d = d.strip()
                	query= "SELECT PackageName from DexSignatures where ClassOneHash = '"+d+"'"
                	cursor.execute(query)
                	result = cursor.fetchone()
                	print result 
        	conn.close()

	if __name__=='__main__':
	        main()

