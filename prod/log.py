import datetime

log = []

def getTimestamp():
	return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
def getDate():
	return datetime.datetime.now().strftime("%Y-%m-%d")
def getTime():
	return datetime.datetime.now().strftime("%H:%M:%S")

def append(detectionType): #detectionType = [cam|mic]
	global log

	log.append((getDate(),getTime(),detectionType))

def dump(filename='log.csv'):
	logfile = open(filename, 'a')

	logfile.write('Detection_date,Detection_time,Detection_type\n')

	logfile.write("\n".join(map(lambda line: ",".join(line), log)) + '\n')
	print('Finished writing ' + str(len(log)) + ' records to ' + filename)





