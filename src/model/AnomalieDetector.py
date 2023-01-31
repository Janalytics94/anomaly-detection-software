
class AnomalyDetector():

    def load_data(path, scenario, train=True, test=True, validation=False):
        #load data 
        TRAIN = {}
        TEST = {}
        VALIDATION = {}

        path = "../../../data/interim/"
        train = "train_"
        test = "test_"
        validation = "validation_"
        #  list of scenarios
        scenarios = [
                'CVE-2012-2122',
                'CVE-2014-0160',
                'CVE-2017-7529',
                'CVE-2017-12635_6',
                'CVE-2018-3760',
                'CVE-2019-5418',
                'CVE-2020-9484',
                'CVE-2020-13942',
                'CVE-2020-23839',
                'CWE-89-SQL-injection'
        ]

        for i in range(0,len(scenarios)):
            TRAIN[scenarios[i]]= pd.read_pickle(path + "/" + train + scenarios[i] + ".pkl")
            TEST[scenarios[i]] = pd.read_pickle(path + "/" + test + scenarios[i] + ".pkl")
            VALIDATION[scenarios[i]] = pd.read_pickle(path + "/" + validation + scenarios[i] + ".pkl")
                    


    def call_model():


    def predict():



    def evaluate():