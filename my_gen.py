from nltk.tree import *
import random
import sys

def deal_with_or(t):
	count=0
	prev_node = None
	or_node = False
	factor = 5

	for child in t:
		str_child = str(child)
		if type(child) is str and child == "OR":
			if prev_node != None:
				or_node = True
		else:
			if or_node == True:
				count += 1
				random_num = random.randint(0,10)
				if count > 0:
					factor = 5
				if count > 5:
					factor = 7 #when count > 5, favor prev_node, since it will have more chances of being kicked out
				elif count > 10:
					factor = 9
				if random_num > factor:
					t.remove(prev_node)
					prev_node = child
					if type(child) is not str:
						deal_with_or(child)
				else:
					t.remove(child)
			else:
				prev_node = child
				if type(child) is not str:
					deal_with_or(child)
##########################

def generate(t): 
	#to generate a sentence, we change the tree
	#first pass: whenever two nodes are between "OR", choose one and delete the other based on random number
	#second pass: when a node has a question mark, half the time skip and move to the right,
	#the other half the time, leave it
	#third pass: generate sentence left-to-right, including children


	deal_with_or(t)
	temp =  traverse(t)
	temp = format(temp)
	return temp
			
#################################################
def format(temp):
	
	temp=temp.replace("(@", "")
	temp=temp.replace("(","")
	temp=temp.replace(")", "")
	temp=temp.replace("S","")
	temp=temp.replace("OR","")
	temp=temp.replace("\n","")
	new_s = ""
	temp = temp.split(' ')
	for word in temp:
		if len(word)>0:
			new_s += word+' '

	return new_s

##################################################
def traverse(t):
   string = ""
   parents = []
   nextone = False

   
 
   for child in t:
	if str(child).find("@") > -1:
		random_num = random.randint(0,10)
		if random_num > 5:
			string += traverse(child)
	else:
		string += str(child)+" "

   return string

#################################################
################################
def main(n=1000):
	Rules = {}
	trees = []

	public_rule = ""
	input_f = ""
	output_f = ""

	args = sys.argv
	if len(args) !=4:
		print "Error: Type 'python my_gen.py [grammar file] [number of sentences] [output file]'\nFor example, 'python my_gen.py grammar.bnf 100 output.txt'"
		exit()
	else:
		input_f = args[1]
		n = int(args[2])
		output_f = args[3]

	read_f = open(input_f)
	for line in read_f:
		tag, rule = line.split(' = ')
		if tag == "<START>":
			public_rule = tag
		rule = rule.replace('[', '(@')
		rule = rule.replace(']', ')')
		rule = rule.replace('|', 'OR')
		rule = rule.replace(';', '')
		rule = "(S "+rule+")"
		Rules[tag] = rule


	for tag in Rules.keys():
		if Rules[public_rule].find(tag) > -1:
			Rules[public_rule] = Rules[public_rule].replace(tag, Rules[tag])
			
	for i in range(n):
		trees.append(Tree(Rules[public_rule]))
	
	results = []
	for i in range(n):
		results.append(generate(trees[i]))

	write_f = open(output_f, "a")
	for result in results:
		write_f.write(result)
		write_f.write("\n")

	write_f.close()
####################
if __name__ == "__main__":
	main()
