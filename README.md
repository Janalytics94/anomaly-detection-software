# Anomaly Detection for Software Vulnerabilities 
## An approach to evaluate a data set if it represents normal behaviour

The digital companion to the Master Thesis.
In the master branch you'll find a detailed analysis in Jupyter Notebooks.
In the branch *develop* you'll find a ready to use pipeline which can be extended.

## Summary 


## Data 

We used the Leipzig Intrusion Detection Data Set - Version 2021 (LID-DS). It consists of different scenarios. Each scenario represents a real vulnerability. The focous in our research was on the following scenarios and the designated resource statistics cpu usage and memory consumption gathered in the .res files. 

* CVE-2012-2122
* CVE-2014-0160
* CVE-2017-7529
* CVE-2017-12635_6
* CVE-2018-3760
* CVE-2019-5418
* CVE-2020-9484
* CVE-2020-13942
* CVE-2020-23839
* CWE-89-SQL-injection


For more information please refer to data/raw/LID-DS-2021-Readme.md 


## Project Structure

    ├── README.md                                             # this readme file
    │    
    ├── requirements.txt                                      # this file may be used to create an environment
    │
    ├── dvc.yaml                                              # config. file for pipeline
    │
    ├── src                                                  
    │   ├── ingest                                            # module to load the data 
    │   ├── model                                             # module to call the prediction models
    │   ├── visualize                                         # visualize results                                      
    │
    |__ sut                                                   # dummy to recod mjs sceanrio with LIDS  
    │
    ├── data
        ├──raw                                                 # contains each scenario of the LID-DS which was considered
        ├──interim                                             # will contain the data in the desired format
        ├── model                                              # saved models in pickle format 
        ├── predictions                                        # results of the algorithms and performance 
        |__ gridsearch                                         # gridsearch results
                                       


## Adding Data 

* Due to the large amount of data you need to download the data for the scenarios here: https://github.com/LID-DS/LID-DS
* Further you can use the provided framework to record your own sceanrio and analyze it with this project. 
* After downloading the  data please copy it to data/raw

## Run full DVC Pipeline

Please run the following command in your terminal in order to run the full pipeline

'''
dvc repro
'''

## Do Gridsearch 

If you want to perform a grdisearch for each algorithm and scenario please run the following commands in your terminal

'''
-  ./src/model/gridsearch.py data/interim data/gridsearch CVE-2012-2122 IForest 10
-  ./src/model/gridsearch.py data/interim data/gridsearch CVE-2012-2122 LOF 10
-  ./src/model/gridsearch.py data/interim data/gridsearch CVE-2012-2122 VAE 10
-  ./src/model/gridsearch.py data/interim data/gridsearch CVE-2020-9484 IForest 10
-  ./src/model/gridsearch.py data/interim data/gridsearch CVE-2020-9484 LOF 10
-  ./src/model/gridsearch.py data/interim data/gridsearch CVE-2020-9484 VAE 10 
'''

## Contact

* Jana Vihs, jvihs@yahoo.com or vihsjana@student.hu-berlin.de