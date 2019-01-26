# CVR_reformating
Python scripts to reformat Cast Vote Record files are in the "scripts" folder.

There are two: 
    clearballot_to_dominion.py takes as input a single CVR export file from a ClearBallot system (specifically, the one in use in Multnomah County, OR in 2018) 
    ess_dir_to_dominion.py takes as input a directory containing one or more CVR files exported from the ES&S system in use in Rhode Island in 2018.
    
In both cases, the input CVR files must be scrubbed of any commas, quotes and apostrophes.
In both cases  the output is a single file suitable for upload to the ColoradoRLA tool (https://github.com/FreeAndFair/ColoradoRLA)




