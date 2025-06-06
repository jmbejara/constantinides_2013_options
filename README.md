# Portfolio Returns Reproduction based on Constantinides, George M., Jens Carsten Jackwerth, and Alexi Savov. “The puzzle of index option returns.” Review of Asset Pricing Studies 3, no. 2 (2013): 229-257.


## Getting Started 
* Be sure to have a WRDS account: [Wharton Research Data Services](https://wrds-www.wharton.upenn.edu/)
* Clone this repository using your favorite flavor of Git. Set this as your working directory: 
	* [https://github.com/harrypandas/finm-32900_final_project.git](https://github.com/harrypandas/finm-32900_final_project.git)
	```
	cd User/*/*/finm-32900_final_project
	```
	
* Create a python environment and install packages using pip:
	```
	conda create --name puzzle python==3.12

	conda activate puzzle

	pip install -r requirements.txt 
	```

 * Alternatively, if you prefer using conda (or run into dependency issues with pip) run this from the directory where the environment.yml file is located:
	```
 	conda env create -f environment.yml

 	conda activate puzzle

 	# verify the packages installed
 	conda list
	```
 	*Note that with the approach above, you may have to manually install packages that are not available via conda (e.g. wrds via pip install wrds).*
 
* Optional Action: Set up .env file 
	* Copy env.example to .env
	* In this file you may set the directories that the data and output files will be saved to. Please note, that the final latex report will be saved under ./reports.
		```
		DATA_DIR="data"
		OUTPUT_DIR="output"
		```
	* In .env you may provide your WRDS user name, if you do not do this, you will be prompted for username and password twice as the data is loaded. 
		```
		WRDS_USERNAME=""
		```
	* In this file you may also set the two date ranges you'd like to see. The defaults are:
		```
		START_DATE_01="1996-01-01"
		END_DATE_01="2012-01-31"
		START_DATE_02="2012-02-01"
		END_DATE_02="2019-12-31"
		```
	  
* In the */finm-32900_final_project working directory run: 
	```
	doit
	```
