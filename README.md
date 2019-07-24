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

## Start the IPython Jupyter Notebook
The process of training the model will occur in a Jupyter notebook.  To start the Jupyter notebook do the following.
* Change working directory to the src directory `cd src`
* Run the start script `shell_scripts\start_notebook.bat` (if on Windows) `bash shell_scripts/start_notebook.sh` (if on Linux or Mac)
* Once the notebook is started you will see a message similar to `[I 01:48:58.493 NotebookApp] http://(c47a03698188 or 127.0.0.1):8888/?token=37d5e7c9798cad30db8d0ff23081e7a1ca76b103d7bc`
* Copy the link into the browser address bar eliminating the sha in the url; for example cop the value http://127.0.0.1:8888/?token=37d5e7c9798cad30db8d0ff23081e7a1ca76b103d7bc given the example above
* Click on the work folder in the browser then click on the codeonthebeach2019.ipynb file
* Congratulations, your IPython notebook should be loaded