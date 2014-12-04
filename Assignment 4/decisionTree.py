def predict(example):
	print example
	print example[14] #1
	if str(example[14]) == "0":
		if str(example[13]) == "0":
			if str(example[9]) == "0":
				return "shellfish"
			elif str(example[9]) == "1":
				return "reptile"

		elif str(example[13]) == "1":
			if str(example[4]) == "0":
				return "mammal"
			elif str(example[4]) == "1":
				return "fish"
	elif str(example[14]) == "2":
		if str(example[2]) == "0":
			return "bird"
		elif str(example[2]) == "1":
			return "mammal"

	elif str(example[14]) == "4":
		if str(example[2]) == "0":
			if str(example[7]) == "0":
				return "reptile"
			elif str(example[7]) == "1":
				if str(example[9]) == "0":
					return "shellfish"
				elif str(example[9]) == "1":
					return "amphibian"
		elif str(example[2]) == "1":
			return "mammal"
	elif str(example[14]) == "5":
		return "shellfish"
	elif str(example[14]) == "6":
		if str(example[7]) == "0":
			return "insect"
		elif str(example[7]) == "1":
			return "shellfish"

	elif str(example[14]) == "8":
		return "shellfish"

print predict(['shark',0,0,1,0,0,1,1,1,1,0,0,1,0,1,0,0])
print "hi"