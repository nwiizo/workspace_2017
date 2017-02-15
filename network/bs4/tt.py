import csv
	
def bb():
	a = csv.reader(open('user_list.csv', 'rb'), delimiter=' ', quotechar='|')
	for n in a:
		print n

bb()
