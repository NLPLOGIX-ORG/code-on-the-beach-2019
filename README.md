## Prerequisites
* Install docker from https://docs.docker.com/install/
* Install the python 3.7 image `docker pull python:3.7`

## Running the ETL
The ETL process generates a file called a case table.  The case table is the file that is used to train a model.  To run the ETL process do the following.
* Change working directory to the src directory `cd src`
* Run the etl script `shell_scripts\etl.bat` (if on Windows) `bash shell_scripts/etl.sh` (if on Linux or Mac)
