#!/usr/bin/python
""" Input is directory containing ES&S CSV exports -- if starting from .xlsx, remove commas, quotes 
and save as .csv. Program creates file dictionaries.txt with dictionaries of choices and rules by contest.


"""
import os
import sys
from sets import Set




def list_csv_files(input_dir):
    file_list = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            file_list.append(filename)
            continue
        else:
            continue
            print 'List of csv files:\n\t', '\n\t'.join(file_list)   
    return(file_list)

def check_headers(input_dir,file_list):
    ## check that header lines in file_list are the same, return header line if so.
    header_lines = Set([])
    for filename in file_list:
        file_path=os.path.join(input_dir,filename)
        with open(file_path,'rU') as current_file:
            header = current_file.readline()
            header_lines.add(header)
    if len(header_lines) !=  1:
        print 'Header lines of csv files don\'t all match.'
        print header_lines
        return('Header lines didn\'t match')
    else:
        print "Header lines of all csv files match."
        for header_line in header_lines: ## there's only one
            return(header_line)

def make_dictionaries(input_dir,file_list):
    header_line = check_headers(input_dir,file_list)
    if header_line == 'Header lines didn\'t match':
        sys.exit()
    headers = ((header_line.rstrip()).replace('$','')).split(",")
    print headers
    if headers[3]=='':
        print 'First contest name is blank; program ending.'
        sys.exit()
    contests_no_dupe = headers[3:]


    #Make  dictionary rule_by_contest giving the number of votes each voter may cast in the contest 
    current_contest = 'Null Contest'
    rule_by_contest = {} 
    for i in range(len(contests_no_dupe)):
        if contests_no_dupe[i] == '':
            rule_by_contest[current_contest]+=1 # will break if first current_contest name is ''
        else:
            current_contest = contests_no_dupe[i]
            rule_by_contest[current_contest]=1

    #Make dictionary choices_by_contest giving all choices as a function of the contest, based on info in the CVR file
    choices_by_contest = {} 
    current_contest = 'Null Contest'
    i_contest = 0 # index of contest, even if vote for >1, 
    row_length = 6  # initialized to match 6 columns of ballot info in Dominion 
    for i in range(len(contests_no_dupe)):
        if contests_no_dupe[i] != '':
            print 'For ',contests_no_dupe[i_contest],'choices are: ' 
            current_contest = contests_no_dupe[i]
            choices = []
            i_contest = i

        for file_name in file_list:
            with open(os.path.join(input_dir,file_name),'rU') as choice_f:
                next(choice_f) # skip header row
                for row in choice_f:
                    row = (row.rstrip()).split(",")
                    if (row[i+3] <> '' and row[i+3] <> 'undervote' and  row[i+3] <> 'overvote' and row[i+3] not in choices):    # offset for ballot info
                        choices.append(row[i+3])
                    row_length = row_length +  len(choices)
        choices_by_contest[contests_no_dupe[i_contest]] = choices
        if 0 == i - i_contest - rule_by_contest[contests_no_dupe[i_contest]] +1:
            print choices
    for contest in contests_no_dupe:
        if contest <> '':
            choice_list = choices_by_contest[contest]
            if choice_list == []:  ### edge case: if there are no votes for a particular contest
                choice_list = ['Null choice']
            choice_num = len(choice_list)



    return(choices_by_contest,rule_by_contest)


if __name__ == "__main__":
              print 'Beware of commas and quote marks inside fields! If they weren\'t all removed you might have trouble. )'
              input_dir = sys.argv[1]
              out_file = 'dictionaries.txt'
              file_list=list_csv_files(input_dir)
              print 'output of list_csv_files(',input_dir,') is:\n',file_list
              [choices,rule]=make_dictionaries(input_dir,file_list)
              with open(os.path.join(input_dir,out_file),'w') as o_f:
#                  out_line = str(choices)+'\n'+str(rule)+ '\n'
                  out_line = str( [choices,rule])
                  o_f.write(out_line)
              


