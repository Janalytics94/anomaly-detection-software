# Leipzig Intrusion Detection Data Set - Version 2021
## Overview
-   LID-DS is a modern host based intrusion detection system (HIDS) data set.    
-   It is recorded on a modern operating system (Ubuntu 18.04).    
-   It consists of different scenarios. Each scenario represents a real vulnerability.    
-   We recorded system calls with their metadata like parameters, return values, user ids, process/thread ids, file system handles, timestamps, and io buffers (truncated).    
-   Additionally we recorded the network traffic of the victim and system statis like cpu, hdd and net usage.
-   With this new version of the host based intrusion detection system data set you can re-evaluate and compare old HIDS, develop and compare new approaches using system call and network data.    
-   Additionally to the dataset we implemented the complete ids process starting with loading, feature extraction, anomaly detection to evaluation as python lib. (see https://github.com/LID-DS/LID-DS)

## Usage
Each folder represents a scenario. The data is split into training, validation and test data.  Each recording is given as a zip file containing a json, a pcap, a res and a sc file. The LID-DS dataloader is capable of loading this data.
- The json file gives information about the recording. Like: runtime, involved containers, used exploid.
- The pcap file contains the network traffic fo the victim.
- The res file contains system statistics recorded every second.
- The sc file contains the system calls.

## Literature and Sources
For a more detailed description of the data set, the recording process and the frameworks used, please refer to the following publications, thesises and github repositories:
- LID-DS-2021:
  - Martin Grimmer; Tim Kaelble; Felix Nirsberger; Emmely Schulze; Toni Rucks; Jörn Hoffmann; and Erhard Rahm: "Dataset Report: LID-DS 2021", (submitted) , 2022
  - Toni Rucks: "Verbesserung des LID-DS unter Verwendung einer Multi-Container-Docker-Umgebung zum Erfassen von Daten für host- und netzwerkbasierte Angriffserkennung" Bachelor thesis, Leipzig University, 2021
- LID-DS-2019:
  -   Martin Grimmer; Martin Max Röhling; Dennis Kreusel; Simon Ganz, "A Modern and Sophisticated Host Based Intrusion Detection Data Set", 16. Deutscher IT-Sicherheitskongress, 2019
  -   Martin Max Röhling; Martin Grimmer; Dennis Kreußel; Jörn Hoffmann; Bogdan Franczyk, "Standardized container virtualization approach for collecting host intrusion detection data", FedCSIS, 2019
  -   Dennis Kreußel. "Simulation and analysis of system call traces for adversial anomaly detection.”. Bachelor thesis, Leipzig University, 2019
  -   Simon Ganz. “Ein moderner Host Intrusion Detection Datensatz”. Master thesis, Leipzig University, 2019
  -   https://github.com/LID-DS/LID-DS: A lightweight intrusion detection data simulation framework.
    
## List of all Scenarios of LID-DS-2021
| type   | Name                 | link to description |
|--------|----------------------|---------------------|
| simple | Bruteforce_CWE-307   | [link](https://github.com/LID-DS/LID-DS/tree/master/scenarios/Bruteforce_CWE-307#readme)                    |
| simple | CVE-2012-2122        | [link](https://github.com/LID-DS/LID-DS/tree/master/scenarios/CVE-2012-2122)                    |
| simple | CVE-2014-0160        | [link](https://github.com/LID-DS/LID-DS/tree/master/scenarios/CVE-2014-0160)                    |
| simple | CWE-89-SQL-injection | [link](https://github.com/LID-DS/LID-DS/tree/master/scenarios/CWE-89-SQL-injection)                    |
| simple | EPS_CWE-434          | [link](https://github.com/LID-DS/LID-DS/tree/master/scenarios/EPS_CWE-434)                    |
| simple | PHP_CWE-434          | [link](https://github.com/LID-DS/LID-DS/tree/master/scenarios/PHP_CWE-434)                    |
| simple | ZipSlip              | [link](https://github.com/LID-DS/LID-DS/tree/master/scenarios/ZipSlip)                    |
| multi  | CVE-2017-12635_6     | [link](https://github.com/LID-DS/LID-DS/tree/master/scenarios/CVE-2017-12635_6)                    |
| simple | CVE-2019-5418        | [link](https://github.com/LID-DS/LID-DS/tree/master/scenarios/CVE-2019-5418)                    |
| simple | CVE-2017-7529        | [link](https://github.com/LID-DS/LID-DS/tree/master/scenarios/CVE-2017-7529)                    |
| simple | CVE-2018-3760        | [link](https://github.com/LID-DS/LID-DS/tree/master/scenarios/CVE-2018-3760)                    |
| simple | CVE-2020-9484        | [link](https://github.com/LID-DS/LID-DS/tree/master/scenarios/CVE-2020-9484)                    |                   
| multi  | CVE-2020-23839       | [link](https://github.com/LID-DS/LID-DS/tree/master/scenarios/CVE-2020-23839)                    |
| multi  | Juiceshop            | [link](https://github.com/LID-DS/LID-DS/tree/master/scenarios/Juice-Shop)                    |
| multi  | CVE-2020-13942       | [link](https://github.com/LID-DS/LID-DS/tree/master/scenarios/CVE-2020-13942)                    |                

### type: 
- simple: the attack is one single step like uploading a malicious file and running it
- multi: the attack consists of multiple steps like: port scanning, brute force, privilege escalation and remote code execution


## Contact regarding LID-DS-2021
Leipzig University, Martin Grimmer (grimmer@informatik.uni-leipzig.de) 