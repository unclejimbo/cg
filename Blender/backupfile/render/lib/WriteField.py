f = file('.\\casting_refined_ffield.txt', "w+")

for line in open('.\\casting_refined.ffield').readlines():
	items = line.strip().split(' ')

	for i in range(len(items[2:])):
		f.write(str(items[2:][i]))
		f.write(" ")

	f.write("\n")
	
f.close