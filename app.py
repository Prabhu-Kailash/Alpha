import eel
import os.path
from pathlib import Path
import json
from datetime import datetime
from pyModules import Testing as Rabit
import os


class AlphaMale:
    def __init__(self):
        self.home = str(Path.home())
        self.pwd = self.home + "/Desktop"
        self.ReworkProd = self.pwd + "/Builds/Reworks/Prod"
        self.ReworkPP = self.pwd + "/Builds/Reworks/PreProd"
        self.outputpp = self.pwd + "/Builds/Output/PreProd"
        self.output = self.pwd + "/Builds/Output/Prod"
        self.Routputpp = self.pwd + "/Builds/Output/Rework/PreProd"
        self.Routput = self.pwd + "/Builds/Output/Rework/Prod"
        Path(self.Routputpp).mkdir(parents=True, exist_ok=True)
        Path(self.Routput).mkdir(parents=True, exist_ok=True)
        Path(self.ReworkProd).mkdir(parents=True, exist_ok=True)
        Path(self.ReworkPP).mkdir(parents=True, exist_ok=True)
        Path(self.outputpp).mkdir(parents=True, exist_ok=True)
        Path(self.output).mkdir(parents=True, exist_ok=True)

    def clearance(self, path):
        outputfiles = glob.glob(path + "/*.json")
        for file in outputfiles:
            os.remove(l)

    @eel.expose
    def validation(dataObj, env):
        home = str(Path.home())
        pwd = home + "/Desktop"
        ReworkProd = pwd + "/Builds/Reworks/Prod"
        ReworkPP = pwd + "/Builds/Reworks/PreProd"
        if (env == "Prod"):
            if(os.path.isfile("\\\\VA1PZCNAS01.us.ad.lfg.com\\sfg_preprod_build\\YAML_Current\\prod\\%s.yaml" % dataObj["MainProducer"])):
                search = open("\\\\VA1PZCNAS01.us.ad.lfg.com\\sfg_preprod_build\\YAML_Current\\prod\\%s.yaml" %
                              dataObj["MainProducer"], "r").read().find(dataObj["MainConsumer"])
                if search < 0:
                    return "Consumer doesn't exist under the producer YAML"
                else:
                    with open(ReworkProd + "/%s%s_%s.json" % (dataObj["MainProducer"], dataObj["MainConsumer"], datetime.now().strftime('%Hh%Mm%Ss')), "w") as json_file:
                        json.dump(dataObj, json_file)
                    return "Success. Output JSON file generated at ../Desktop/Builds/Reworks folder"
            else:
                return "Producer doesn't exist at Prod area, kindly validate"
        else:
            if(os.path.isfile("\\\\VA1PZCNAS01.us.ad.lfg.com\\sfg_preprod_build\\YAML_Current\\nonprod\\%s.yaml" % dataObj["MainProducer"])):
                search = open("\\\\VA1PZCNAS01.us.ad.lfg.com\\sfg_preprod_build\\YAML_Current\\nonprod\\%s.yaml" %
                              dataObj["MainProducer"], "r").read().find(dataObj["MainConsumer"])
                if search < 0:
                    return "Consumer doesn't exist under the producer YAML"
                else:
                    with open(ReworkPP + "/%s%s_%s.json" % (dataObj["MainProducer"], dataObj["MainConsumer"], datetime.now().strftime('%Hh%Mm%Ss')), "w") as json_file:
                        json.dump(dataObj, json_file)
                    return "Success. Output JSON file generated at ../Desktop/Builds/Reworks folder"
            else:
                return "Producer doesn't exist at PreProd area, kindly validate"

    @eel.expose
    def chromeController():
        print("I am in")
        hop = Rabit.RoadRunner(
            path="C:\\Users\\kavpr6\\Pictures").aplhaBooster()
        return hop


if __name__ == "__main__":
    eel.init('Web')

    eel.start('index.html', size=(450, 452))
