import json
from pathlib import Path
import os.path


class Yaml:

    def __init__(self, path, filename, env):
        self.home = str(Path.home())
        self.pwd = self.home + "/Desktop"
        self.repo = self.pwd + "/Builds/PathToLocalRepo_DonotDelete.txt"
        self.output = self.pwd + "/Builds/Output"
        self.jsonData = self.loadJson(path, filename)
        self.yamlData = self.yamlRecon(env, self.jsonData["MainProducer"])
        self.producer = self.producer(self.jsonData)
        self.findConsumer = self.index_containing_substring(self.yamlData, self.jsonData["MainConsumer"])
        self.findRoutingChannel = self.index_containing_substring(self.yamlData, self.producer + ":" + self.jsonData["MainConsumer"])
        self.findProducer = self.index_containing_substring(self.yamlData, self.jsonData["MainProducer"])
        self.protocol = self.protocolCustom(self.jsonData, self.yamlData, self.findConsumer)
        self.customProtocol = str()
        
    def protocolCustom(self, json, yamlData, consumerPos):
        protocol = dict()
        if json["HoldSetup"] == "False":
            details = (yamlData[consumerPos + 44]
                            [35:len(yamlData[consumerPos + 44]) - 2]).split(",")
            for eachDetail in details:
                values = eachDetail.split(":")
                protocol[values[0]] = values[1]
        return protocol

    def index_containing_substring(self, the_list, substring):
        for i, s in enumerate(the_list):
            if substring in s:
                return i
        return -1
    
    def producer(self, json):
        if json["SecondaryProducer"] == "":
            producer = json["MainProducer"]
        else:
            producer = self.jsonData["SecondaryProducer"]
        return producer

    def loadJson(self, path, fileName):
        with open(path + "\\" + fileName, "r") as file:
            data = json.load(file)
            return data

    def yamlRecon(self, env, producerName):
        try:
            if env == "nonprod": env = "PreProd"
            with open("%s\\%s\\%s.yaml" % (self.output, env, producerName), 'r') as yaml_in:
                yaml_object = yaml_in.readlines()
                return yaml_object
        except FileNotFoundError:
            if env == "PreProd": env = "nonprod"
            with open(self.repo, 'r') as repoPath:
                localRepo = (repoPath.readline()).strip()
            with open("%s\\%s\\%s.yaml" % (localRepo, env, producerName), 'r') as yaml_in:
                yaml_object = yaml_in.readlines()
                return yaml_object


class customExtensions(Yaml):

    def __init__(self, path, filename, env):
        self.path = path
        self.filename = filename
        self.env = env
        super().__init__(self.path, self.filename, self.env)

    def addEmail(self, initialList, addDataField):
        consolidatedEmail = str()
        newEmail = self.jsonData[addDataField].split(" ")
        EmailToBeAdded = initialList
        caseSensitive = [mail.casefold() for mail in EmailToBeAdded]
        EmailToBeAdded.extend(
            x for x in newEmail if x.casefold() not in caseSensitive)
        for instance in EmailToBeAdded:
            consolidatedEmail = consolidatedEmail + instance + " "
        consolidatedEmail = consolidatedEmail.strip()
        return consolidatedEmail

    def removeEmail(self, initialList, rmDataField):
        consolidatedEmail = str()
        removeEmail = self.jsonData[rmDataField].split(" ")
        EmailToBeAdded = initialList
        caseSensitive = [mail.casefold() for mail in EmailToBeAdded]
        for email in removeEmail:
            if email.casefold() in caseSensitive:
                index = caseSensitive.index(email.casefold())
                del EmailToBeAdded[index]
        for instance in EmailToBeAdded:
            consolidatedEmail = consolidatedEmail + instance + " "
        consolidatedEmail = consolidatedEmail.strip()
        return consolidatedEmail

    def logic(self):

        if self.jsonData["RemoveConsumer"] != "":
            if self.findConsumer >= 0:
                self.yamlData[self.findConsumer + 1] = "    ensure                      : 'absent'\n"

            if self.findRoutingChannel >= 0:
                self.yamlData[self.findRoutingChannel + 1] = "    ensure            : 'absent'\n"

        if self.jsonData["UpdateRC"] != "":
            if self.findRoutingChannel >= 0:
                self.yamlData[self.findRoutingChannel + 2] = "    template_name     : '%s'\n" % self.jsonData["UpdateRC"]

        if self.jsonData["RemoveProducer"] != "":
            if self.findProducer >= 0:
                self.yamlData[self.findProducer + 1] = "    ensure                      : 'absent'\n"

        if self.jsonData["RemovePGPEncrypt"] != "":
            if self.findConsumer >= 0:
                self.yamlData[self.findConsumer + 30] = "    public_key_id               : ~\n"
                self.yamlData[self.findConsumer + 19] = "    does_require_encrypted_data : false\n"

        if self.jsonData["UpdatePGPEncrypt"] != "":
            if self.findConsumer >= 0:
                self.yamlData[self.findConsumer + 30] = "    public_key_id               : '%s'\n" % self.jsonData["UpdatePGPEncrypt"]
                self.yamlData[self.findConsumer + 19] = "    does_require_encrypted_data : true\n"

        if self.jsonData["UpdatePGPSign"] != "":
            if self.findConsumer >= 0:
                self.yamlData[self.findConsumer + 20] = "    does_require_signed_data    : true\n"

        if self.jsonData["RemovePGPSign"] != "":
            if self.findConsumer >= 0:
                self.yamlData[self.findConsumer + 20] = "    does_require_signed_data    : false\n"

        if self.jsonData["RemovePGPSign"] != "" and self.jsonData["RemovePGPEncrypt"] != "":
            if self.findConsumer >= 0:
                self.yamlData[self.findConsumer + 20] = "    does_require_signed_data    : false\n"
                self.yamlData[self.findConsumer + 30] = "    public_key_id               : ~\n"
                self.yamlData[self.findConsumer + 19] = "    does_require_encrypted_data : false\n"
                self.yamlData[self.findConsumer + 18] = "    does_require_compressed_data: false\n"

        if self.jsonData["UpdateSSHAuth"] != "" and self.jsonData["HoldSetup"] == "False" and self.jsonData["UpdateSSHAuth"] != "Remove":
            if self.findProducer >= 0:
                self.yamlData[self.findProducer + 21] = "    does_use_ssh                : true\n"
                self.yamlData[self.findProducer + 42] = "    authorized_user_key_name    : '%s'\n" % self.jsonData["UpdateSSHAuth"]
        elif self.jsonData["UpdateSSHAuth"] != "" and self.jsonData["HoldSetup"] == "True" and self.jsonData["UpdateSSHAuth"] != "Remove":
            if self.findConsumer >= 0:
                self.yamlData[self.findConsumer + 21] = "    does_use_ssh                : true\n"
                self.yamlData[self.findConsumer + 42] = "    authorized_user_key_name    : '%s'\n" % self.jsonData["UpdateSSHAuth"]
        elif self.jsonData["UpdateSSHAuth"] == "Remove" and self.jsonData["HoldSetup"] == "False":
            if self.findProducer >= 0:
                self.yamlData[self.findProducer + 21] = "    does_use_ssh                : false\n"
                self.yamlData[self.findProducer + 42] = "    authorized_user_key_name    : ~\n"
        elif self.jsonData["UpdateSSHAuth"] == "Remove" and self.jsonData["HoldSetup"] == "True":
            if self.findConsumer >= 0:
                self.yamlData[self.findConsumer + 21] = "    does_use_ssh                : false\n"
                self.yamlData[self.findConsumer + 42] = "    authorized_user_key_name    : ~\n"

        if self.jsonData["RemoveFailEmail"] != "" and self.jsonData["HoldSetup"] == "False":
            if self.findConsumer >= 0:
                try:
                    failEmails = self.protocol['LFGSFTPDelivery_SFTPFailEmailId'].split(" ")
                except KeyError:
                    self.protocol['LFGSFTPDelivery_SFTPFailEmailId'] = ""
                    failEmails = []
                outEmail = self.removeEmail(failEmails, "RemoveFailEmail")
                self.protocol['LFGSFTPDelivery_SFTPFailEmailId'] = outEmail

        if self.jsonData["AddFailEmail"] != "" and self.jsonData["HoldSetup"] == "False":
            if self.findConsumer >= 0:
                try:
                    failEmails = self.protocol['LFGSFTPDelivery_SFTPFailEmailId'].split(" ")
                except KeyError:
                    self.protocol['LFGSFTPDelivery_SFTPFailEmailId'] = ""
                    failEmails = []
                outEmail = self.addEmail(failEmails, "AddFailEmail")
                self.protocol['LFGSFTPDelivery_SFTPFailEmailId'] = outEmail

        if self.jsonData["AddDetailEmail"] != "" and self.jsonData["HoldSetup"] == "False":
            if self.findConsumer >= 0:
                try:
                    detailEmails = self.protocol['LFGSFTPDelivery_SFTPEmailId'].split(" ")
                except KeyError:
                    self.protocol['LFGSFTPDelivery_SFTPEmailId'] = ""
                    detailEmails = []
                outEmail = self.addEmail(detailEmails, "AddDetailEmail")
                self.protocol['LFGSFTPDelivery_SFTPEmailId'] = outEmail

        if self.jsonData["RemoveDetailEmail"] != "" and self.jsonData["HoldSetup"] == "False":
            if self.findConsumer >= 0:
                try:
                    detailEmails = self.protocol['LFGSFTPDelivery_SFTPEmailId'].split(" ")
                except KeyError:
                    self.protocol['LFGSFTPDelivery_SFTPEmailId'] = ""
                    detailEmails = []
                outEmail = self.removeEmail(detailEmails, "RemoveDetailEmail")
                self.protocol['LFGSFTPDelivery_SFTPEmailId'] = outEmail

        if self.jsonData["AddSuccessEmail"] != "" and self.jsonData["HoldSetup"] == "False":
            if self.findConsumer >= 0:
                try:
                    successEmails = self.protocol['LFGSFTPDelivery_SFTPEmailIdSh'].split(" ")
                except KeyError:
                    self.protocol['LFGSFTPDelivery_SFTPEmailIdSh'] = ""
                    successEmails = []
                outEmail = self.addEmail(successEmails, "AddSuccessEmail")
                self.protocol['LFGSFTPDelivery_SFTPEmailIdSh'] = outEmail

        if self.jsonData["RemoveSuccessEmail"] != "" and self.jsonData["HoldSetup"] == "False":
            if self.findConsumer >= 0:
                try:
                    successEmails = self.protocol['LFGSFTPDelivery_SFTPEmailIdSh'].split(" ")
                except KeyError:
                    self.protocol['LFGSFTPDelivery_SFTPEmailIdSh'] = ""
                    successEmails = []
                outEmail = self.removeEmail(successEmails, "RemoveSuccessEmail")
                self.protocol['LFGSFTPDelivery_SFTPEmailIdSh'] = outEmail

        if self.jsonData["UpdateFileRename"] != "" and self.jsonData["UpdateFileRename"] != "Remove" and self.jsonData["HoldSetup"] == "False":
            if self.findConsumer >= 0:
                self.protocol['LFGSFTPDelivery_SFTPNewName'] = self.jsonData["UpdateFileRename"]
        elif self.jsonData["UpdateFileRename"] == "Remove" and self.jsonData["HoldSetup"] == "False":
            if self.findConsumer >= 0:
                self.protocol['LFGSFTPDelivery_SFTPNewName'] = ""

        if self.jsonData["UpdateDir"] != "" and self.jsonData["HoldSetup"] == "False":
            if self.findConsumer >= 0:
                self.protocol['LFGSFTPDelivery_SFTPDir'] = self.jsonData["UpdateDir"]

        if self.jsonData["UpdateSSH"] != "" and self.jsonData["HoldSetup"] == "False":
            if self.findConsumer >= 0:
                self.protocol['LFGSFTPDelivery_SFTPProfileId'] = self.jsonData["UpdateSSH"]

        if self.jsonData["HoldSetup"] == "False":
            for k, v in self.protocol.items():
                self.customProtocol += k + ":" + v + ","
            self.yamlData[self.findConsumer + 44] = "    custom_protocol_extensions  : '%s'\n" % self.customProtocol[:-1]
        
        return [self.yamlData, self.jsonData["MainProducer"]]

