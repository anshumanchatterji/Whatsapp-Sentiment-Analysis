# Import libraries
import numpy as np
import re
import pandas as pd
import matplotlib.pyplot as plt
import random


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
			userAndMsg = line[23:].replace("‪", "").replace(" ","").replace("‬","")
			fromUser = "'" + userAndMsg.split(':')[0].strip() + "'"
			msg = userAndMsg[len(fromUser):].strip() #replace('\n'," ")
			
			if(len(msg) > 0): # We don't need to add information when users are added
				allMessages.append(Message(date, fromUser, msg))	
			#print(msg)
			

	#for itm in allMessages:
		#print(itm.date, itm.fromUser, itm.msg)

	df = pd.DataFrame.from_records([s.to_dict() for s in allMessages])
	df = df.dropna()
	

	
	df['Issue'] = df['msg'].str.findall('cam|nimbus|maid|gate|car|parking|lift|basement|leakage|monkey|बंदर|आतंक|bandar|dog|steal|stealing|dg|security|management|mirror|water|dripping|nbh|fan|hot|heat', flags=re.IGNORECASE)
	df['Tower'] = df['msg'].str.findall('I Tower|I-Tower|Tower I|Tower-I|J Tower|J-Tower|Tower J|Tower-J|K Tower|K-Tower|Tower K|Tower-K|L Tower|L-Tower|Tower L|Tower-L|M Tower|M-Tower|Tower M|Tower-M|I1 Tower|I1-Tower|Tower I1|Tower-I1|J1 Tower|J1-Tower|Tower J1|Tower-J1|K1 Tower|K1-Tower|Tower K1|Tower-K1|L1 Tower|L1-Tower|Tower L1|Tower-L1|M1 Tower|M1-Tower|Tower M1|Tower-M1', flags=re.IGNORECASE)
	df['Pleads'] = df['msg'].str.findall('plz|request|please|plz|sir|madam|kudos|good|Done|resolved', flags=re.IGNORECASE)

	df['Issue'] = [', '.join(map(str, l)) for l in df['Issue']]
	df['Tower'] = [', '.join(map(str, l)) for l in df['Tower']]
	df['Pleads'] = [', '.join(map(str, l)) for l in df['Pleads']]

	
	count_issues = df.Issue.str.lower().value_counts()
	count_issues = count_issues[count_issues.index != ''] #Drop chats without any issue
	count_issues = count_issues[count_issues > 10] #Atleast reported by 4 people
	

	count_fromUser = df.fromUser.value_counts()
	count_fromUser = count_fromUser[count_fromUser > 60] #Frequent Users

	print(count_issues)
	print(count_fromUser)

	#count_issues.plot(kind='pie')
	
	# Creating autocpt arguments
	def func(pct, allvalues):
	    absolute = int(pct / 100.*np.sum(allvalues))
	    return absolute

	

	#df.to_csv('chats.csv', index=False)

	#fig = plt.figure(figsize =(10, 7))
	plt.subplot(1, 2, 1)
	plt.title('Most highlighted Keywords')
	plt.pie(count_issues,
		labels = count_issues.index,
		autopct = lambda pct: func(pct, count_issues),
		wedgeprops = { 'linewidth' : 1, 'edgecolor' : "green" },
		shadow = False,
		explode = tuple([random.randint(0,40)/100 for i in range(len(count_issues))])
		)
	#plt.show()

	
	plt.subplot(1, 2, 2)
	plt.title('Active Members')
	plt.pie(count_fromUser,
		labels = count_fromUser.index,
		autopct = lambda pct: func(pct, count_fromUser),
		wedgeprops = { 'linewidth' : 1, 'edgecolor' : "green" },
		shadow = False,
		explode = tuple([random.randint(0,40)/100 for i in range(len(count_fromUser))])
		)
	plt.show()