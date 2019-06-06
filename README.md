## Prerequisites
* Create the etl/data directory
* Install docker from https://docs.docker.com/install/
* Install the python 3.7 image `docker pull python:3.7`
* Download the tax roll file called Duval County 2018 Certified Tax Roll - Text File - Pipe Delimited from http://www.coj.net/departments/property-appraiser/property-appraiser-online-forms
* Unzip the file and place the files in the et\/data directory

## Running the ETL
The ETL process generates a file called a case table.  The case table is the file that is used to train a model.  To run the ETL process do the following.
* Change working directory to the src directory `cd src`
* Run the etl script `shell_scripts\etl.bat` (if on Windows) `bash shell_scripts/etl.sh` (if on Linux or Mac)