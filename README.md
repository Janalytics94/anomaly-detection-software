# Anomaly Detection for Software Vulnerabilities 
## An approach to evaluate a data set if it represents normal behaviour

The digital companion to the designated Master Thesis


## Summary 

https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0152173#sec008    

https://github.com/Deffro/Data-Science-Portfolio/blob/master/Notebooks/Outlier%20Detection/Outlier%20Detection%20-%20Theory%2C%20Visualizations%20and%20Code.ipynb


https://www.infoq.com/articles/system-behaviour-time-series-ml/

## Data 

We used the Leipzig Intrusion Detection Data Set - Version 2021 (LID-DS). It consists of different scenarios. Each scenario represents a real vulnerability. The focous in our research was on the resource statistics like cpu usage and memory consumption. For more information please refer to data/raw/LID-DS-2021-Readme.md 

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
* After downloading the  data pleasec copy it data/raw

### Usage

In order to load the designated data please run *dvc repro -f* in your terminal

## Contact

* Jana Vihs, jvihs@yahoo.com or vihsjana@student.hu-berlin.de