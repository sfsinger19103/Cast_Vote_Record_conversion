#!/usr/bin/python
""" Developed by Stephanie Singer for Multnomah County pilot audit, 
with funding from Verified Voting (verifiedvoting.org).   MIT License (https://opensource.org/licenses/MIT)
Takes ClearBallot CSV export and munges it
into a format that Free & Fair's Colorado RLA can accept (Dominion format 
from Colorado 2017).

"""
import numpy as np
import hashlib
import time
import sys


print('Run this from the directory where your file (filename.csv) resides. UsageFrom the command line:\n python clearballot_to_dominion.py filename.csv\nBeware of commas, quotes and apostrophes inside fields in filename.csv! If they weren\'t all removed you might have trouble.')
def write_cb_data(infile,outfile,election_info):
    with open(infile,'r') as f:
        with open(outfile,'w') as out_f:

### prepare second output line
            lines = f.readlines()

# first need to parse the choices into contest, choice, party.

headers = (lines[0].rstrip()).split(",")
data_rows = lines[1:]
ballot_info = headers[:9]
choices = headers[10:]

###### HOW MANY CHOICES? ########
row_length = len(choices) + 6

## initialize lists for three-row choice headers in Dominion format
#### note assumption that "vote for" number is only one didgit!

contest = ['']*6
rule =  ['']*6
cand =  ['']*6
party =  []

for choice in choices:
    cc = choice.split(":")
    contest.append(cc[1]+' (Vote For=')
    rule.append(cc[2][-1:]+')')
    cand.append(cc[3])
    party.append(cc[4])

### write first line
out_line = election_info + ','*(row_length-1)+'\r\n'
out_f.write(out_line) 


### write contests to second line of file

out_contests = np.core.defchararray.add(contest,rule)
out_line = ','.join(out_contests)+'\r\n'
out_f.write(out_line)

### write candidate names to third line
out_line =  ','.join(cand) + '\r\n'
out_f.write(out_line)


### write Dominion-style headers and parties  to fourth line
out_line = 'CvrNumber,TabulatorNum,BatchId,RecordId,ImprintedId,BallotType,' + ','.join(party) + '\r\n'
out_f.write(out_line)

### write data 

for row in data_rows:
    row = row.split(',')
    cvr_number = row[0]
    tabulator_number = row[7].replace('multnomahscan','')
    batch_id = row[1].replace('AB-','')
    record_id = row[2]
    imprinted_id = row[3]
    ballot_type = row[6]
    out_list = [cvr_number, tabulator_number, batch_id, record_id,imprinted_id,ballot_type] 
    out_list.extend( row[10:]) # note that row has '\r\n' at end
    out_line = ','.join(out_list)
    out_f.write( out_line)

#### cleanup files

f.close()
out_f.close()

### hash the output file and store the filename, hash and timestamp 

try:
    hash_file = open('hashes.txt','x')
except Exception:
    hash_file = open('hashes.txt','a')

BLOCKSIZE = 65536
hasher = hashlib.sha256()
with open(outfile, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)
out_line = hasher.hexdigest()+ '\t'+ outfile + '.csv' + '\t' + time.ctime(time.time())+'\n'


hash_file.write(out_line)
