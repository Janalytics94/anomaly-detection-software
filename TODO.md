# TODO:


- setting up chossing scenario model dynmaically, 
- set up docker container for running pipeline and monitoring data, 
- set up experiements with contamination rate and feature importance
- plots: CMS, ROC

MASTER THESIS

- [ ] Make sure that the other features were not important in the data points.
- [ ] Check Feature importance! Justify 
- [ ] Regression Model, Confidence 
- [ ] Print the contamination rate of Isolation Forest after running, get_params, what happens? 
- [ ] Check pyod 0 are outliers and 1 are normal points
- [ ] Contamiation rate „auto“, heads up, printing parameters
- [ ] Heads up: Isolation Forest if you run it for several times the results won’t be exact the same. 

Viraj
- Work considers only 2 features but the labels will be dependent on all features. Taking only 2 features will introduce duplicates to 
- Possible way to justify it would be to show feature importance or feature effect
- IF algorithm will produce some different outliers in each iteration

To DOS aus Meetings
- [ ] Präsentation Ergebnisse sowohl FOKUS als auch Lessmann
- [ ] Aggregierten Gesamtergebnisse in Tabelle
- [x] Correlation Plots und Treshold Tabelle und Boxplots  einfügen und beschreiben (Boxplots mit no outliers fehlt noch)
- [ ] Anmerkungen von den Leuten, die es drüber gelesen haben mit rein nehmen 
- [ ] Ggf. noch Tabelle für LR review machen
- [ ] DRÜBER LESEN UND GLATT ZIEHEN.
- [ ] MEHR BESSERE PAPER SUCHEN
- [x] Eigenständigkeitserklärung einfügen!!
- [ ] Formatierung!
- [ ] Add Contamination rate Table
- [ ] Einheiten von cpu usage und memory consumption hinzufügen
- [ ] Bibliography bereinigen
- [ ] Plagiat und Rechtschreibung Überprüfen
- [ ] Wegen Zero GPT nochmal alles gegen checken
- [ ] Hyperparaemter config in appendix 
- [ ] Refs 1 sieht komisch aus
- [ ] Forschungsfragen Verknüpfung besser herstellen
- [ ] Concluson kürzen und ggf. auto encoder und so noch erklären
- [ ] Ergebnisse mit ins Abstract


Fragen:
  - Interpretation False and True Positives, konkrete situation welche Daten Punkte
- Martins Kommentare ander Methods 1.3

Lessmann 20.12.2022

- Abbildungen aus anderen Quellen z.b im LR oder Theoretical Background?
- Konkrete Fragen zum Experimental Design, Results and Discussion, Aufbau - Ausreichend wie es aktuell ist? 
- Abbildungen konkret in den Appendix oder alles in den Hauptteil?
- Sollte Explorative Data Analysis mit rein?
- Wann darf ich inoffiziell abgeben?

 -  Experimental design chapter für Daten anzureißen , Qualitätssmessung Unsupervised Learning,
- Erklärung warum unsupervised Learning, Klare Position zu supervised und unsupervised, 
- Ergebnisse müssen stark mit Ergebnissen korrelieren, guter Link
- KLASSISCHER ANHANG. NUR DIE DINGE DIE AUCH IN ARBEIT ANGESPROCHEN WIRD - GIT REPO 
- WIN, TIE, LOSS, AGGREAGIEREN SZENRAIO, Algorithmen, 
- Towards Data Science KEINE GEWÜNSCHTE Quelle - Primärliteratur! 
- Vor Ende Januar nicht abgeben 
- LR Table ist gewünscht/Willkommen 

Nützliche Blogbeiträge Master

PyOD :https://medium.com/dataman-in-ai/anomaly-detection-with-pyod-b523fc47db9
https://github.com/yzhao062/pyod
https://conferences.oreilly.com/artificial-intelligence/ai-ny-2018/public/schedule/detail/64889.html
https://medium.com/@mab-datasc/isolation-forest-a-tree-based-algorithm-for-anomaly-detection-4a1669f9b782 
https://towardsdatascience.com/approaching-anomaly-detection-in-transactional-data-744d132d524e
https://towardsdatascience.com/unsupervised-anomaly-detection-on-time-series-9bcee10ab473
https://www.linkedin.com/pulse/anomaly-detection-aiops-vimal-raj/
https://github.com/datamllab/tods
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0152173#sec008    
https://github.com/Deffro/Data-Science-Portfolio/blob/master/Notebooks/Outlier%20Detection/Outlier%20Detection%20-%20Theory%2C%20Visualizations%20and%20Code.ipynb
https://www.infoq.com/articles/system-behaviour-time-series-ml/
https://ieeexplore.ieee.org/abstract/document/9685157
https://arxiv.org/abs/2112.08442
https://ieeexplore.ieee.org/abstract/document/4622868
https://towardsdatascience.com/approaching-anomaly-detection-in-transactional-data-744d132d524e

XAI - Paper
https://ieeexplore.ieee.org/abstract/document/9763241
https://arxiv.org/abs/2112.08442
https://ieeexplore.ieee.org/abstract/document/8430788
https://dl.acm.org/doi/abs/10.1145/3447548.3470794?casa_token=pNkBhEGvnlsAAAAA:-z5JjBuGVr5MSo9xaL0SX19AFjJGR8sJ8NpazmFtdYByFPa3VI5sQ4Rmt0zXBggMc-lZAicb_Z8N
https://ieeexplore.ieee.org/abstract/document/8637456
https://ieeexplore.ieee.org/abstract/document/8913901
https://dl.acm.org/doi/pdf/10.1145/3465480.3468292

VAE-Paper

Variational Autoencoder Based Anomaly Detection Using Reconstruction Probability" by Ankit A. Rakshit et al
Deep Autoencoding Gaussian Mixture Model for Unsupervised Anomaly Detection" by Zong Wei et al.

* Anomaly detection in software systems
* Outlier detection in software systems
* CPU usage and memory consumption as features for anomaly detection
* Evaluating normal behavior in software systems
* Software vulnerabilities and their impact on normal behavior
* Machine learning and deep learning techniques for anomaly detection in software systems
* Anomaly detection in software systems using run-time parameters
* Real-world case studies of anomaly detection in software systems
* Anomaly detection in software systems for security purposes
* Anomaly detection in software systems for performance evaluation
