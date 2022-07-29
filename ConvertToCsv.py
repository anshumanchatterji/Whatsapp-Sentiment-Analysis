import re
import pandas as pd


class Message:
	def __init__(self, date, fromUser, msg):
		self.date = date
		self.fromUser = fromUser
		self.msg = msg

	def to_dict(self):
		return {
    	    'date': self.date,
    	    'fromUser': self.fromUser,
    	    'msg': self.msg
		}




dateRegex = re.compile(r'(\[\d+\/\d+\/\d+, \d+:\d+:\d+ ..\])')

with open('_chat.txt', 'r', encoding='utf-8') as f:
	#Skip reading first 3 lines
	f.readline()
	f.readline()
	f.readline()

	allMessages = []

	while True:
		line = f.readline()
		if not line:
			break

		#Check if line contains date
		dateGroup = dateRegex.search(line)
		if(dateGroup == None):
			#Date was not found. This means that this is a continuation of above text
			
			#lets append this to the last Message
			allMessages[-1].msg += line

		else:
			date = dateGroup.group()
			userAndMsg = line[23:]
			fromUser = userAndMsg.split(':')[0].strip()
			msg = userAndMsg[len(fromUser)+2:].strip()
			allMessages.append(Message(date, fromUser, msg))

	#for itm in allMessages:
		#print(itm.date, itm.fromUser, itm.msg)

	df = pd.DataFrame.from_records([s.to_dict() for s in allMessages])
	print(df)

