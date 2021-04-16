import eel
from pathlib import Path
import json
import glob
from datetime import datetime
from pyModules import MacroLookAlike as Rabit
from pyModules import JSONtoYAML as broom
import os
import os.path
from datetime import datetime, timedelta


class AlphaMale:

    def __init__(self):
        self.home = str(Path.home())
        self.pwd = self.home + "/Desktop"
        self.ReworkProd = self.pwd + "/Builds/Reworks/Prod"
        self.ReworkPP = self.pwd + "/Builds/Reworks/PreProd"
        self.Routputpp = self.pwd + "/Builds/Output/Rework/PreProd"
        self.Routput = self.pwd + "/Builds/Output/Rework/Prod"
        Path(self.Routputpp).mkdir(parents=True, exist_ok=True)
        Path(self.Routput).mkdir(parents=True, exist_ok=True)
        Path(self.ReworkProd).mkdir(parents=True, exist_ok=True)
        Path(self.ReworkPP).mkdir(parents=True, exist_ok=True)

    def clearance(self, path):
        current_time = [int(m) for m in datetime.strftime(
            datetime.now(), '%Y-%m-%d').split("-")]
        files = os.listdir(path)
        os.chdir(path)
        for f in files:
            creation_time = [int(l) for l in (
                str(datetime.fromtimestamp(os.path.getmtime(f))).split(" ")[0]).split("-")]
            if (current_time[2] - creation_time[2]) != 0 or (current_time[1] - creation_time[1]) != 0 or (current_time[0] - creation_time[0]) != 0:
                os.unlink(f)

    @eel.expose
    def validation(dataObj, env):
        home = str(Path.home())
        pwd = home + "/Desktop"
        ReworkProd = pwd + "/Builds/Reworks/Prod"
        ReworkPP = pwd + "/Builds/Reworks/PreProd"
        Routputpp = pwd + "/Builds/Output/Rework/PreProd"
        Routput = pwd + "/Builds/Output/Rework/Prod"
        if (env == "Prod"):
            if(dataObj["MainProducer"] + ".yaml" in os.listdir("\\\\pathto\\sfg_preprod_build\\YAML_Current\\prod")):
                search = open("\\\\pathto\\sfg_preprod_build\\YAML_Current\\prod\\%s.yaml" %
                              dataObj["MainProducer"], "r").read().find(dataObj["MainConsumer"])
                if dataObj["SecondaryProducer"] != "":
                    search1 = open("\\\\pathto\\sfg_preprod_build\\YAML_Current\\prod\\%s.yaml" %
                                dataObj["MainProducer"], "r").read().find(dataObj["SecondaryProducer"])
                    if search1 < 0:
                        return "Secondary Producer doesn't exist under the producer YAML"
                if search < 0:
                    return "Consumer doesn't exist under the producer YAML"
                else:
                    with open(ReworkProd + "/%s%s_%s.json" % (dataObj["MainProducer"], dataObj["MainConsumer"], datetime.now().strftime('%Hh%Mm%Ss')), "w") as json_file:
                        json.dump(dataObj, json_file)
                    with open(Routput + "/%s%s_%s.json" % (dataObj["MainProducer"], dataObj["MainConsumer"], datetime.now().strftime('%Hh%Mm%Ss')), "w") as json_file:
                        json.dump(dataObj, json_file)
                    return "Success. Output JSON file generated at ../Desktop/Builds/Reworks folder"
            else:
                return "Producer doesn't exist at Prod area, kindly validate"
        else:
            if(dataObj["MainProducer"] + ".yaml" in os.listdir("\\\\pathto\\sfg_preprod_build\\YAML_Current\\nonprod")):
                search = open("\\\\pathto\\sfg_preprod_build\\YAML_Current\\nonprod\\%s.yaml" %
                              dataObj["MainProducer"], "r").read().find(dataObj["MainConsumer"])
                if dataObj["SecondaryProducer"] != "":
                    search1 = open("\\\\pathto\\sfg_preprod_build\\YAML_Current\\nonprod\\%s.yaml" %
                                dataObj["MainProducer"], "r").read().find(dataObj["SecondaryProducer"])
                    if search1 < 0:
                        return "Secondary Producer doesn't exist under the producer YAML"
                if search < 0:
                    return "Consumer doesn't exist under the producer YAML"
                else:
                    with open(ReworkPP + "/%s%s_%s.json" % (dataObj["MainProducer"], dataObj["MainConsumer"], datetime.now().strftime('%Hh%Mm%Ss')), "w") as json_file:
                        json.dump(dataObj, json_file)
                    with open(Routputpp + "/%s%s_%s.json" % (dataObj["MainProducer"], dataObj["MainConsumer"], datetime.now().strftime('%Hh%Mm%Ss')), "w") as json_file:
                        json.dump(dataObj, json_file)
                    return "Success. Output JSON file generated at ../Desktop/Builds/Reworks folder"
            else:
                return "Producer doesn't exist at PreProd area, kindly validate"

    @eel.expose
    def chromeController(path, env):
        home = str(Path.home())
        Routput = home + "/Desktop/Builds/Output/Rework/"
        AlphaMale().clearance(r'%s/%s' % (Routput, env))
        hop = Rabit.RoadRunner(r'%s' % path).aplhaBooster(env)
        return hop

    @eel.expose
    def magicWand(path, env):
        home = str(Path.home())
        Routput = home + "/Desktop/Builds/Output/"
        files = [os.path.basename(file) for file in glob.glob(path + "/*.json")]
        for file in files:
            yamlOut = broom.customExtensions(path, file, env).logic()
            if env == "nonprod": env = "PreProd"
            with open("%s/%s/%s.yaml" % (Routput, env, yamlOut[1]), 'w') as result:
                    for m in yamlOut[0]:
                        result.write(m)
        AlphaMale().clearance(r'%s/Rework/%s' % (Routput, env))

if __name__ == "__main__":
    eel.init('Web')

    AlphaMale()

    eel.start('index.html', size=(550, 550))
