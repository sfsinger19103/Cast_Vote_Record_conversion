# CVR_reformating
Thanks to [Verified Voting](https://www.verifiedvoting.org/) for supporting this project.

Python scripts to reformat Cast Vote Record files are in the "scripts" folder.

There are two: 
- **clearballot_to_coloradoRLA.py** takes as input a single CVR export file from ClearBallot system (v1.4.3). For example, from the folder containing ```clearballot_sample_CVR.csv``` running
```python clearballot_to_coloradoRLA.py clearballot_sample_CVR.csv```
creates  (in the current folder) the file
```RLAclearballot_sample_CVR.csv``` suitable for upload to the ColoradoRLA
and creates (or updates) the file
```hashes.txt```
where the sha256 hash of the output file is stored.

- **ess_dir_to_coloradoRLA.py** takes as input a directory containing one or more CVR files exported from the ES&S system in use in Rhode Island in 2018. Every file in the directory with extension ```.csv```  will be processed. 
Running
```python ess_dir_to_coloradoRLA.py dirpath```
creates (in the directory *dirpath*) a file ```RLA.input``` suitable for upload to the ColoradoRLA 
and creates (or updates) the file
```hashes.txt```
where the sha256 hash of the output file is stored.

    
In both cases the input CVR files must be scrubbed of any commas, quotes and apostrophes.



