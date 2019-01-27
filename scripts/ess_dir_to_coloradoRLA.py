#!/usr/bin/python
""" Take directory containing ES&S CSV exports and munge them
into a format that Free & Fair's Colorado RLA can accept (Dominion format 
from Colorado 2017). Requires that no quotes, apostrophes or commas are in the csv fields.

"""
import numpy as np
import hashlib
import time
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
    if headers[3]=='':
        print 'First contest name is blank; program ending.'
        sys.exit()
    contests_no_dupe = headers[3:] # contains some blanks, indicating vote for more than one
    current_contest = 'Null Contest'
    rule_by_contest = {} 
    choices_by_contest = {} 
    i_contest = 0 # index of contest, even if vote for >1, 
    for i in range(len(contests_no_dupe)):
        if contests_no_dupe[i] == '':
            rule_by_contest[current_contest]+=1
    for i in range(len(contests_no_dupe)):
        if contests_no_dupe[i] == '':
            rule_by_contest[current_contest]+=1 # will break if first current_contest name is ''
        else:
            current_contest = contests_no_dupe[i]
            rule_by_contest[current_contest]=1
            print 'For ',contests_no_dupe[i_contest],'choices are: ' 
            current_contest = contests_no_dupe[i]
            choices = []
            i_contest = i

    


def start_dom_file(input_dir,file_list,election_info,header_line,out_file):
    headers = ((header_line.rstrip()).replace('$','')).split(",")
    ballot_info = headers[:3]
    ### note: headers contain some blanks, indicating vote for more than one
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
    row_length = 6  # initialized to match 6 columns of ballot info in Dominion format
    for i in range(len(contests_no_dupe)):
        if contests_no_dupe[i] != '':
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
    dom_row_two = ['']*6
    dom_row_three = ['']*6
    dom_row_four =  ['CvrNumber','TabulatorNum','BatchId','RecordId','ImprintedId','BallotType']
    for contest in contests_no_dupe:
        if contest <> '':
            choice_list = choices_by_contest[contest]
            if choice_list == []:  ### edge case: if there are no votes for a particular contest
                choice_list = ['Null choice']
            choice_num = len(choice_list)
            dom_row_two = dom_row_two + [contest+' (Vote For='+ str(rule_by_contest[contest]) +')']*choice_num
            dom_row_three = dom_row_three + choice_list
            dom_row_four = dom_row_four + ['']*choice_num

    ### write results to out_file
    with open(os.path.join(input_dir,out_file),'w') as out_f:
              ### write first line
              out_line = election_info + ','*len(dom_row_three)+'\r\n'
              out_f.write(out_line) 
              ### write  second line of file
              out_line =','.join(dom_row_two) + '\r\n'
              out_f.write(out_line)
              ### write third line of file
              out_line =','.join(dom_row_three) + '\r\n'
              out_f.write(out_line)
              ### write fourth line of file
              out_line =','.join(dom_row_four) + '\r\n'
              out_f.write(out_line)
    return(dom_row_two,dom_row_three,contests_no_dupe)

def write_ess_data(input_dir,file_list,dom_row_two,dom_row_three,contests_no_dupe,out_file):
    print 'Starting to write data'
    with open(os.path.join(input_dir,out_file),'a') as out_f: # 'a' for append
        for file_name in file_list:
            print 'Processing '+file_name
            with open(os.path.join(input_dir,file_name),'rU') as data_f:
                next(data_f) #skip header row
                for row in data_f:
                    o_list = ['']*len(dom_row_two)
                    row = row.split(',')
                    o_list[:6]=[row[0]]*5+[row[2]]
 
                    data_items = row[3:]  ## note indexing matches contests_no_dupe
                    current_contest = 'Null contest'
                    for i in range(len(data_items)): # loop through input fields in row
                        if contests_no_dupe[i] != '':
                            current_contest = contests_no_dupe[i]
                        for j in range(len(dom_row_two)-6): # loop though (contest,choice) pairs
                            if dom_row_two[j+6].startswith(current_contest):
                                if dom_row_three[j+6] == data_items[i]:
                                    o_list[j+6] = '1'
                                elif data_items[i]<>'' and o_list[j+6]!= '1':
                                    o_list[j+6] = '0'

                    out_line = ','.join(o_list)
                    out_f.write(out_line+'\r\n')

def hash(input_dir,file_name):
    try:
        hash_file = open(os.path.join(input_dir,'hashes.txt'),'x')
    except Exception:
        hash_file = open(os.path.join(input_dir,'hashes.txt'),'a')

        BLOCKSIZE = 65536
        hasher = hashlib.sha256()
        with open(os.path.join(input_dir,file_name), 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        out_line = hasher.hexdigest()+ '\t'+ out_file  + '\t' + time.ctime(time.time())+'\n'
        print out_line
        hash_file.write(out_line)



if __name__ == "__main__":
              print 'Beware of commas and quote marks inside fields! If they weren\'t all removed you might have trouble. Also beware of spaces in ballot identification fields (e.g., precinct name)'
              input_dir = sys.argv[1]
              election_info='testing_RI'
              file_list=list_csv_files(input_dir)
              print 'output of list_csv_files(',input_dir,') is:\n',file_list
              header_line = check_headers(input_dir,file_list)
              if header_line == 'Header lines didn\'t match':
                  sys.exit()
              out_file = 'RLA.input'
              [dom_row_two,dom_row_three,contests_no_dupe] = start_dom_file(input_dir,file_list,election_info,header_line,out_file)
              write_ess_data(input_dir,file_list,dom_row_two,dom_row_three,contests_no_dupe,out_file)
              hash(input_dir,out_file)


