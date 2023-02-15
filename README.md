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
    ├── src                                                   # module to load the data 
    │   ├── ingest
    │   ├── model                                             # module to call the prediction models
    │   ├── notebooks                                         # notebooks with detailed explanation of the procedure
    │   └── plots
    │
    ├── data
        ├──raw                                                 # contains each scenario of the LID-DS which was considered
        ├── interim                                            # will contain the data in the desired format


## Adding Data 

* Due to the large amount of data you need to download the data for the scenarios here: https://github.com/LID-DS/LID-DS
* Further you can use the provided framework to record your own sceanrio and analyze it with this project. 
* After downloading the  data please copy it to data/raw

### Usage

In order to load the designated data please run *dvc repro -f* in your terminal

## Contact

* Jana Vihs, jvihs@yahoo.com or vihsjana@student.hu-berlin.de