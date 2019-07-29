#!/usr/bin/python3
import os, socket, sys, subprocess, re
file_path = input ("Please enter the complete path of your json batch file:\n")
opening_line = "[\n"   # opening line of the jason file
ending_line = "]\n"	# closing line of the jason file
opening_char = r'\[' 	# opening char for search purpose
ending_char = r'\]' # closing char for search purpose
init_char = "A2345678910JQK"
final_char = "CHSD"
entries_list = {} # Creating a dictionary to store entry attribute where key range from 2 to 53 and each value is a list of [init char; final char; rank; suit; color]
metric_sum = 0 # this sum = waste metric

# This function checks whether the given path is a valid file; if it's not, print out warning then exit.
def checkFileExist(path):
	if not os.path.isfile(path):
		print ("file path does not exist")
		sys.exit()

def updateOutputFiles(message):
	isvalid = open("is-invalid-batch.json", "w")
	isvalid.write(opening_line)
	isvalid.write("\"" + message + "\"" + "\n")
	isvalid.write(ending_line)
	isvalid.close()
	isvalid = open("waste-metric.json", "w")
	isvalid.write(opening_line)
	isvalid.write("\"" + "No waste meric available due to " +message + "\"" + "\n")
	isvalid.write(ending_line)
	isvalid.close()
	isvalid = open("one-swap-recommendation.json", "w")
	isvalid.write(opening_line)
	isvalid.write("\"" + "No one-swap-recommendation available due to " + message + "\"" + "\n")
	isvalid.write(ending_line)
	isvalid.close()
	isvalid = open("two-swap-recommendation.json", "w")
	isvalid.write(opening_line)
	isvalid.write("\"" + "No two-swap-recommendation available due to " + message + "\"" + "\n")
	isvalid.write(ending_line)
	isvalid.close()

def updateOneFiles(output_path, message):
        isvalid = open(output_path, "w")
        isvalid.write(opening_line)
        isvalid.write("\"" + message + "\"" + "\n")
        isvalid.write(ending_line)
        isvalid.close()

# This function validates whether the file has 54 lines.  If not, alert the customer and update relevant files accordingly. 
def check52entries():
	count = len(open(file_path).readlines(  ))
	if count != 54:
		print ("This is an invalid batch file: invalid file length")
		updateOutputFiles("invalid file length")
		sys.exit()

# This function validates the first and last character match the defined pattern; If not, alert the customer and update relevant files accordingly.
def checkValidEntries():
	with open(file_path) as entries:
		line_counter = 1
		for line in entries:
			line = line.strip()
			if line_counter == 1:
				if not re.match(opening_char, line):
					print ("Batch invalid as missing opening [")
					updateOutputFiles("Batch invalid as missing opening [")
					sys.exit()
			elif line_counter == 54:
                                if not re.match(ending_char, line):
                                        print ("Batch invalid as missing closing ]")
                                        updateOutputFiles("Batch invalid as missing closing ]")
                                        sys.exit()
			else:
				line= line.replace('"', "")
				line = line.replace(',', "")
				if len(line) == 3:
					first_char = "10"
					second_char = line[2]
				else:	
					first_char = line[0]
					second_char = line[1]
				entries_list [ line_counter] = [first_char, second_char]	
				first_char = r"(.*)" + first_char + r"(.*)"
				second_char = r"(.*)" + second_char + r"(.*)"
				if not re.match(first_char, init_char):
					print ("Batch invalid as initial character out of range")
					updateOutputFiles("Batch invalid as initial character out of range")
					sys.exit()
				if not re.match(second_char, final_char):
                                        print ("Batch invalid as final character out of range")
                                        updateOutputFiles("Batch invalid as final character out of range")
                                        sys.exit()
			line_counter += 1

def check_shuffled():
	init_char = "A23456789JQK"
	shuffle_found = False
	init_len = len(init_char)
	final_len = len(final_char)
	spec_char = "10"
	for init in range (0, init_len):
		for final in range (0, final_len):
			entry = init_char[init] + final_char[final]
			shuffle_found = False
			with open(file_path) as entries:
				for line in entries:
					line = line.strip()
					line= line.replace('"', "")
					line = line.replace(',', "")
					if re.match(entry, line):
						shuffle_found = True
						break
			if not shuffle_found:
				message = "Batch invalid as it does not contain one of the possible shuffled entry " + entry
				print (message)
				updateOutputFiles(message)
				sys.exit()
	for final2 in range (0, final_len):
		entry2 = spec_char + final_char[final2]
		with open(file_path) as entries:
			for line in entries:
				line = line.strip()
				line= line.replace('"', "")
				line = line.replace(',', "")
				if re.match(entry2, line):
					shuffle_found = True
					break
		if not shuffle_found:
			message = "Batch invalid as it does not contain one of the possible shuffled entry" + entry
			print (message)
			updateOutputFiles(message)
			sys.exit()

# This function will caculate the rank, suit and color for each entry, then store them to the dictionary
def entry_property():
	for keys in range(2,54):
		entry =  entries_list[keys]
		#print (entry)
		first_char = entry [0]
		second_char = entry [1]
		rank1 = "23456789"
		rank2 = "10JQK"
		#print ("first char is: " + first_char + "2nd char is " + second_char)
		if first_char == "A":
			rank = 1
		else:
			first_match = r"(.*)" + first_char + r"(.*)"
			if re.match(first_match, rank1):
				rank = int(first_char)
			else:
				rank = 10
		if second_char == "C":
			suit = "Club"
		if second_char == "H":
                        suit = "Heart"
		if second_char == "S":
                        suit = "Spade"
		if second_char == "D":
                        suit = "Diamond"
		if suit == "Club" or suit == "Spade":
			color = "Black"
		if suit == "Heart" or suit == "Diamond":
			color = "Red"
		#print ("suit is: " + suit + " color is: " + color)
		entry = [first_char,  second_char, rank, suit, color]
		entries_list[keys] = entry

#This function will calculate the waste metric for a give batch, and return the metric as an integer
def waste_metric(dict):
	metric_sum = 0
	for keys in range(2,53):
		this_rank =  dict[keys][2]
		this_suit = dict[keys][3]
		this_color = dict[keys][4]
		next_rank =  dict[keys+1][2]
		next_suit = dict[keys+1][3]
		next_color = dict[keys+1][4]
		#print ("current rank/suit/color")
		#print (str(this_rank) + str(this_suit) + str(this_color))
		#print ("next rank/suit/color")
		#print (str(next_rank) + str(next_suit) + str(next_color))		
		if this_suit == next_suit:
			metric_sum += abs(this_rank - next_rank)
		elif this_color == next_color:
			diff = 2 * abs(this_rank - next_rank)
			metric_sum += diff
		else:
			diff = 3 * abs(this_rank - next_rank)
			metric_sum += diff
		#print ("sum is: " + str( metric_sum))
	return metric_sum

# This function gets the waste metric for the master batch and update the output file
def update_waste_metric_file():
	total_sum = waste_metric(entries_list)
	sum_mess = "The waste metric is: " + str(total_sum)
	print (sum_mess)
	updateOneFiles("waste-metric.json", sum_mess)

# This function calculate the one-swap for original batch, then update the output file accordingly.
def one_swap():
	original_sum = waste_metric(entries_list)
	best_sum = original_sum
	new_dict = entries_list.copy()
	line1 = 0
	line2 = 0
	orig_entry = ""
	swap_entry = ""
	swapped = False
	for key1 in range(2,53):
		key3 = key1 + 1
		for key2 in range(key3, 54):
			#print ("key1 is " + str(key1) + " key2 is " + str(key2))
			#new_dict = entries_list
			old_key1 = new_dict[key1]
			new_dict[key1] = new_dict[key2]
			new_dict[key2] = old_key1
			new_sum = waste_metric(new_dict)
			#print ("new sum is " + str(new_sum) + " Old sum is :" + str(best_sum))
			if best_sum > new_sum:
				#print ("new sum is " + str(new_sum) + " Old sum is :" + str(best_sum))
				swapped = True
				best_sum = new_sum
				line1 = key1
				line2 = key2
				orig_entry = new_dict[key2][0] +  new_dict[key2][1]
				swap_entry = new_dict[key1][0] +  new_dict[key1][1]		
				#print ("swap line " + str(line1) + ", entry " + orig_entry + " with line " + str(line2) + ", entry "+ swap_entry) 
			new_dict = entries_list.copy() 
	if not swapped:
		sum_mess = "No swap needed, you already have the best waste metric of " + str(original_sum)
		print (sum_mess)
		updateOneFiles("one-swap-recommendation.json", sum_mess)
	else:
		sum_mess = ("By swapping line " + str(line1) + ", entry " + orig_entry + " with line " + str(line2) + ", entry " + swap_entry + ", you could reduce waste metric from " + str(original_sum) + " to " + str(best_sum))
		print (sum_mess)
		updateOneFiles("one-swap-recommendation.json", sum_mess)

# This function calculate the one-swap for a given batch dictionary, skipping the first two swapped entries, and return with a list for the 2nd set of swap entries as well as the best waste metric
def one_swap_for_two_swaps(two_dict, oldkey1, oldkey2):
	original_sum = waste_metric(two_dict)
	new_dict = two_dict.copy()
	best_sum = original_sum
	line1 = 0
	line2 = 0
	orig_entry = ""
	swap_entry = ""
	swapped = False
	for key1 in range(2,53):
		key3 = key1 + 1
		if key1 == oldkey1 or key1 == oldkey2:
			#print ("key1 matches given key")
			continue
		for key2 in range(key3, 54):
			if key2 == oldkey1 or key2 == oldkey2:
				#print ("key2 matches given key")
				continue
			#print ("New key 1 " + str(key1) + " new key2 " + str(key2))
			old_key1 = new_dict[key1]
			new_dict[key1] = new_dict[key2]
			new_dict[key2] = old_key1
			new_sum = waste_metric(new_dict)
			if best_sum > new_sum:
				swapped = True
				best_sum = new_sum
				line1 = key1
				line2 = key2
				orig_entry = new_dict[key2][0] +  new_dict[key2][1]
				swap_entry = new_dict[key1][0] +  new_dict[key1][1]
			new_dict = two_dict.copy()
	return (line1, line2, orig_entry, swap_entry, best_sum)

# This function will interate through the batch, swap two entries at a time, then pass the new batch to function above to look for the next swap entry set as well as best values 
def two_swaps():
	original_sum = waste_metric(entries_list)
	best_sum = original_sum
	line1 = 0
	line2 = 0
	second_line1 = 0
	second_line2 = 0 
	swapped = False
	new_dict = entries_list.copy()
	for key1 in range(2,53):
		key3 = key1 + 1
		for key2 in range(key3, 54):
			old_key1 = new_dict[key1]
			new_dict[key1] = new_dict[key2]
			new_dict[key2] = old_key1
			#print ("key1 is " + str(key1) + " key2 is " + str(key2))
			list = one_swap_for_two_swaps(new_dict, key1, key2)
			#print (list)
			if best_sum > list[4]:
				best_sum = list[4]
				swapped = True
				line1 = key1
				line2 = key2
				second_line1 = list[0]
				second_line2 = list[1]
				orig_entry1 = new_dict[key2][0] +  new_dict[key2][1]
				swap_entry1 = new_dict[key1][0] +  new_dict[key1][1]
				orig_entry2 = list[2]
				swap_entry2 = list[3]
			new_dict = entries_list.copy()
	if not swapped:
		sum_mess = "No swap needed, you already have the best waste metric of " + str(original_sum)
		print (sum_mess)
		updateOneFiles("two-swap-recommendation.json", sum_mess)
	else:
		sum_mess = ("By swapping line " + str(line1) + ", entry " + orig_entry1 + " with line " + str(line2) + ", entry " + swap_entry1)
		sum_mess = sum_mess + ", then swapping line " + str(second_line1) + ", entry " + orig_entry2 + " with line " + str(second_line2) + ", entry " + swap_entry2
		sum_mess = sum_mess + ", you could reduce waste metric from " + str(original_sum) + " to " + str(best_sum)
		print (sum_mess)
		updateOneFiles("two-swap-recommendation.json", sum_mess)		
			
checkFileExist(file_path)
check52entries()
checkValidEntries()
check_shuffled()
print ("This is a valid batch")
updateOneFiles("is-invalid-batch.json", "This is a valid batch")
entry_property()
update_waste_metric_file()
one_swap()
two_swaps()

