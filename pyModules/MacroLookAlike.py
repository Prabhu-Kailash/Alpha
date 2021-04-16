from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import selenium.webdriver.support.ui as ui
import glob
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


class RoadRunner:
    def __init__(self, path):
        self.path = path
        self.__chrome_options = Options()
        self.__Chrome = "\\\\pathto\\GIS\\L1_Team\\Selenium Automation\\chromedriver.exe"
        self.__chrome_options.add_experimental_option(
            "debuggerAddress", "127.0.0.1:9222")
        self._driver = webdriver.Chrome(
            self.__Chrome, options=self.__chrome_options)
        self.wait = ui.WebDriverWait(self._driver, 20)
        self.files = glob.glob(self.path + "/*.json")
        self.dictator = dict()

    def readContents(self, fileName):
        with open(fileName, "r") as file:
            self.fileContent = json.load(file)
            return self.fileContent

    def addingEmails(self, dataField, cssPointer, initialList, removeDataField):

        if self.fileContent[dataField] != "" or self.fileContent[removeDataField] != "":
            self._driver.find_element_by_id(cssPointer).clear()
            consolidatedEmail = ""
            newEmail = self.fileContent[dataField].split(" ")
            removeEmail = self.fileContent[removeDataField].split(" ")
            EmailToBeAdded = initialList
            mails = [mail.casefold() for mail in initialList]
            EmailToBeAdded.extend(
                x for x in newEmail if x.casefold() not in mails and x != "")
            caseSensitive = [mail.casefold() for mail in EmailToBeAdded]
            for email in removeEmail:
                if email.casefold() in caseSensitive and email != "":
                    index = caseSensitive.index(email.casefold())
                    self.dictator[self.fileContent["MainProducer"]][self.fileContent["MainConsumer"]].append(
                        "Removed %s from field %s" % (EmailToBeAdded[index], removeDataField))
                    del EmailToBeAdded[index]
            for instance in EmailToBeAdded:
                consolidatedEmail = consolidatedEmail + instance + " "
            num = list(set([l.casefold()
                            for l in EmailToBeAdded]) - set(mails))
            if len(num) > 0:
                for el in num:
                    self.dictator[self.fileContent["MainProducer"]][self.fileContent["MainConsumer"]].append(
                        "Added %s to field %s" % (el, dataField))
            consolidatedEmail = consolidatedEmail.strip()
            self._driver.find_element_by_id(
                cssPointer).send_keys(consolidatedEmail)

    def mainLogic(self):
        try:
            for file in self.files:
                self.readContents(file)

                if self.fileContent["MainProducer"] != "":
                    if self.fileContent["SecondaryProducer"] == "":
                        self.dictator[self.fileContent["MainProducer"]] = {
                            self.fileContent["MainConsumer"]: []}
                    else:
                        self.dictator[self.fileContent["SecondaryProducer"]] = {
                            self.fileContent["MainConsumer"]: []}

                    if self.fileContent["UpdateSSHAuth"] != "":
                        self._driver.find_element_by_name(
                            "OrganizationName$148l").clear()

                        if(self.fileContent["HoldSetup"] == "True"):
                            self._driver.find_element_by_name("OrganizationName$148l").send_keys(
                                self.fileContent["MainConsumer"])
                        else:
                            self._driver.find_element_by_name("OrganizationName$148l").send_keys(
                                self.fileContent["MainProducer"])

                        self._driver.find_element_by_name(
                            "OrganizationName$148l").send_keys(Keys.ENTER)
                        time.sleep(1)
                        currentTabs = self._driver.window_handles
                        currentHandle = self._driver.current_window_handle

                        if(self.fileContent["HoldSetup"] == "True"):
                            self._driver.find_element_by_xpath(
                                "//div[contains(text(), '%s')]" % self.fileContent["MainConsumer"]).click()
                        else:
                            self._driver.find_element_by_xpath(
                                "//div[contains(text(), '%s')]" % self.fileContent["MainProducer"]).click()

                        time.sleep(1)
                        self._driver.find_elements_by_xpath(
                            "//td[@class='buttonTitle']")[3].click()
                        time.sleep(1)
                        postClick = self._driver.window_handles
                        currentWindow = list(set(currentTabs) ^ set(postClick))
                        self._driver.switch_to.window(currentWindow[0])
                        time.sleep(1)
                        self.wait.until(
                            lambda x: self._driver.find_elements_by_tag_name("a")[2])
                        self._driver.find_elements_by_tag_name("a")[2].click()
                        time.sleep(1)
                        self._driver.find_element_by_link_text("Next").click()
                        time.sleep(1)

                        if self.fileContent["UpdateSSHAuth"] != "" and self.fileContent["UpdateSSHAuth"] != "Remove":
                            self._driver.find_elements_by_css_selector(
                                "input[type='radio'][value='yes']")[0].click()
                            self._driver.find_elements_by_css_selector(
                                "input[type='radio'][value='yes']")[1].click()
                            time.sleep(1)
                            self._driver.find_element_by_link_text(
                                "Next").click()
                            self.wait.until(lambda x: self._driver.find_element_by_id(
                                "tradingPartner.sltAUKey"))
                            sshKey = Select(self._driver.find_element_by_id(
                                "tradingPartner.sltAUKey"))
                            sshKey.select_by_value(
                                self.fileContent["UpdateSSHAuth"])
                            self.dictator[self.fileContent["MainProducer"]][self.fileContent["MainConsumer"]].append(
                                "Updated SSH key to %s" % self.fileContent["UpdateSSHAuth"])

                        if self.fileContent["UpdateSSHAuth"] == "Remove":
                            self._driver.find_elements_by_css_selector(
                                "input[type='radio'][value='no']")[0].click()
                            self.dictator[self.fileContent["MainProducer"]][self.fileContent["MainConsumer"]].append(
                                "Removed SSH key")
                        time.sleep(1)
                        self._driver.find_element_by_link_text("Next").click()
                        time.sleep(1)
                        self._driver.find_element_by_link_text(
                            "Finish").click()
                        self.wait.until(
                            lambda x: self._driver.find_element_by_link_text("Return"))
                        self._driver.close()
                        time.sleep(1)
                        self._driver.switch_to.window(currentHandle)

                    if self.fileContent["UpdateRC"] != "":
                        self._driver.find_element_by_xpath(
                            "//td[@class='menuButton']").click()
                        time.sleep(1)
                        self._driver.find_element_by_xpath(
                            "//div[contains(text(), 'Channels')]").click()
                        time.sleep(1)
                        self.wait.until(expected_conditions.invisibility_of_element_located(
                            (By.XPATH, "//td[contains(text(), 'Finding Records that match your criteria...')]")))
                        self._driver.find_element_by_name("consumerKey").send_keys(
                            self.fileContent["MainConsumer"])

                        if self.fileContent["SecondaryProducer"] == "":
                            self._driver.find_element_by_name("producerKey").send_keys(
                                self.fileContent["MainProducer"])
                        else:
                            self._driver.find_element_by_name("producerKey").send_keys(
                                self.fileContent["SecondaryProducer"])

                        time.sleep(1)
                        self._driver.find_element_by_xpath(
                            "//td[@class='buttonTitle']").click()
                        time.sleep(1)
                        self._driver.find_element_by_xpath(
                            "//div[contains(text(), '%s')]" % self.fileContent["MainConsumer"]).click()
                        time.sleep(1)
                        self._driver.find_elements_by_xpath(
                            "//td[@class='buttonTitle']")[3].click()
                        time.sleep(1)
                        self.wait.until(expected_conditions.visibility_of_element_located(
                            (By.NAME, "routingChannelTemplateKey")))
                        self._driver.find_elements_by_name("routingChannelTemplateKey")[
                            1].send_keys(self.fileContent["UpdateRC"])
                        self._driver.find_element_by_xpath(
                            "//div[contains(text(), 'Save')]").click()
                        time.sleep(1)
                        self.wait.until(expected_conditions.visibility_of_element_located(
                            (By.XPATH, "//td[contains(text(), 'Successful')]")))
                        self._driver.find_element_by_xpath(
                            "//div[contains(text(), 'OK')]").click()
                        time.sleep(1)
                        self._driver.find_elements_by_xpath(
                            "//td[@class='menuButton']")[1].click()
                        time.sleep(1)
                        self._driver.find_element_by_xpath(
                            "//div[contains(text(), 'Partners')]").click()
                        self.wait.until(expected_conditions.invisibility_of_element_located(
                            (By.XPATH, "//td[contains(text(), 'Finding Records that match your criteria...')]")))
                        self.wait.until(expected_conditions.visibility_of_element_located(
                            (By.NAME, "OrganizationName$148l")))
                        time.sleep(1)
                        self.dictator[self.fileContent["MainProducer"]][self.fileContent["MainConsumer"]].append(
                            "Updated RC to %s" % self.fileContent["UpdateRC"])

                    if (self.fileContent["RemoveConsumer"] == "" and self.fileContent["RemoveProducer"] == "") and (self.fileContent["UpdateSSH"] != "" or
                                                                                                                    self.fileContent["UpdateDir"] != "" or self.fileContent["UpdateFileRename"] != "" or self.fileContent["AddDetailEmail"] != "" or
                                                                                                                    self.fileContent["AddSuccessEmail"] != "" or self.fileContent["AddFailEmail"] != "" or self.fileContent["RemoveDetailEmail"] != "" or self.fileContent["RemoveSuccessEmail"] != "" or
                                                                                                                    self.fileContent["RemoveFailEmail"] != "" or self.fileContent["UpdatePGPEncrypt"] != "" or self.fileContent["UpdatePGPSign"] != "" or
                                                                                                                    self.fileContent["RemovePGPEncrypt"] != "" or self.fileContent["RemovePGPSign"] != ""):
                        self._driver.find_element_by_name(
                            "OrganizationName$148l").clear()
                        self._driver.find_element_by_name("OrganizationName$148l").send_keys(
                            self.fileContent["MainConsumer"])
                        self._driver.find_element_by_name(
                            "OrganizationName$148l").send_keys(Keys.ENTER)
                        time.sleep(1)
                        currentTabs = self._driver.window_handles
                        currentHandle = self._driver.current_window_handle
                        time.sleep(1)
                        self._driver.find_element_by_xpath(
                            "//div[contains(text(), '%s')]" % self.fileContent["MainConsumer"]).click()
                        time.sleep(1)
                        self._driver.find_elements_by_xpath(
                            "//td[@class='buttonTitle']")[3].click()
                        time.sleep(1)
                        postClick = self._driver.window_handles
                        currentWindow = list(set(currentTabs) ^ set(postClick))
                        self._driver.switch_to.window(currentWindow[0])
                        time.sleep(1)
                        self.wait.until(
                            lambda x: self._driver.find_elements_by_tag_name("a")[2])
                        self._driver.find_elements_by_tag_name("a")[2].click()
                        time.sleep(1)
                        self._driver.find_element_by_link_text("Next").click()
                        time.sleep(1)
                        self._driver.find_element_by_link_text("Next").click()

                        if(self.fileContent["HoldSetup"] != "True"):
                            self.wait.until(
                                lambda x: self._driver.find_element_by_id("SFTPDir"))
                            SFTPDir = (self._driver.find_element_by_id(
                                "SFTPDir").get_attribute("value")).strip()
                            SFTPNewName = (self._driver.find_element_by_id(
                                "SFTPNewName").get_attribute("value")).strip()
                            SFTPDEmailId = (self._driver.find_element_by_id(
                                "SFTPEmailId").get_attribute("value")).strip()
                            SFTPEmailIdSh = (self._driver.find_element_by_id(
                                "SFTPEmailIdSh").get_attribute("value")).strip()
                            SFTPFailEmailId = (self._driver.find_element_by_id(
                                "SFTPFailEmailId").get_attribute("value")).strip()
                            SFTPProfileId = Select(
                                self._driver.find_element_by_id("SFTPProfileId"))
                            SSHid = (SFTPProfileId.first_selected_option.get_attribute(
                                "value")).strip()
                            SFTPDEmailId = SFTPDEmailId.split(" ")
                            SFTPEmailIdSh = SFTPEmailIdSh.split(" ")
                            SFTPFailEmailId = SFTPFailEmailId.split(" ")

                            if self.fileContent["UpdateSSH"] != "":
                                SFTPProfileId.select_by_value(
                                    self.fileContent["UpdateSSH"])
                                self.dictator[self.fileContent["MainProducer"]][self.fileContent["MainConsumer"]].append(
                                    "Updated RemoteProfileID to %s" % self.fileContent["UpdateSSH"])

                            if self.fileContent["UpdateDir"] != "":
                                self._driver.find_element_by_id(
                                    "SFTPDir").clear()
                                self._driver.find_element_by_id("SFTPDir").send_keys(
                                    self.fileContent["UpdateDir"])
                                self.dictator[self.fileContent["MainProducer"]][self.fileContent["MainConsumer"]].append(
                                    "Updated Target directory to %s" % self.fileContent["UpdateDir"])

                            if self.fileContent["UpdateFileRename"] != "" and self.fileContent["UpdateFileRename"] != "Remove":
                                self._driver.find_element_by_id(
                                    "SFTPNewName").clear()
                                self._driver.find_element_by_id("SFTPNewName").send_keys(
                                    self.fileContent["UpdateFileRename"])
                                self.dictator[self.fileContent["MainProducer"]][self.fileContent["MainConsumer"]].append(
                                    "Updated FileRename to %s" % self.fileContent["UpdateFileRename"])
                            elif self.fileContent["UpdateFileRename"] == "Remove":
                                self._driver.find_element_by_id(
                                    "SFTPNewName").clear()
                                self.dictator[self.fileContent["MainProducer"]][self.fileContent["MainConsumer"]].append(
                                    "Removed FileRename")

                            self.addingEmails(
                                "AddDetailEmail", "SFTPEmailId", SFTPDEmailId, "RemoveDetailEmail")
                            self.addingEmails(
                                "AddSuccessEmail", "SFTPEmailIdSh", SFTPEmailIdSh, "RemoveSuccessEmail")
                            self.addingEmails(
                                "AddFailEmail", "SFTPFailEmailId", SFTPFailEmailId, "RemoveFailEmail")
                            self._driver.find_element_by_link_text(
                                "Next").click()
                            time.sleep(1)
                        try:
                            if self._driver.find_element_by_id("tradingPartner.sltAUKey").is_displayed():
                                self._driver.find_element_by_link_text(
                                    "Next").click()
                                time.sleep(1)
                        except:
                            pass

                        if self.fileContent["UpdatePGPSign"] != "":
                            self._driver.find_elements_by_css_selector(
                                "input[type='radio'][value='yes']")[0].click()
                            self.dictator[self.fileContent["MainProducer"]][self.fileContent["MainConsumer"]].append(
                                "Updated PGP sign to Yes")

                        if self.fileContent["RemovePGPSign"] != "":
                            self._driver.find_elements_by_css_selector(
                                "input[type='radio'][value='no']")[0].click()
                            self.dictator[self.fileContent["MainProducer"]][self.fileContent["MainConsumer"]].append(
                                "Updated PGP sign to No")

                        if self.fileContent["UpdatePGPEncrypt"] != "":
                            self._driver.find_elements_by_css_selector(
                                "input[type='radio'][value='yes']")[1].click()
                            self._driver.find_element_by_id("tradingPartnerForm.encryptKey").send_keys(
                                self.fileContent["UpdatePGPEncrypt"])
                            self.dictator[self.fileContent["MainProducer"]][self.fileContent["MainConsumer"]].append(
                                "Updated PGP Encrption to %s" % self.fileContent["UpdatePGPEncrypt"])

                        if self.fileContent["RemovePGPEncrypt"] != "":
                            self._driver.find_elements_by_css_selector(
                                "input[type='radio'][value='no']")[1].click()
                            self.dictator[self.fileContent["MainProducer"]][self.fileContent["MainConsumer"]].append(
                                "Removed PGP Encryption")

                        self._driver.find_element_by_link_text(
                            "Finish").click()
                        self.wait.until(
                            lambda x: self._driver.find_element_by_link_text("Return"))
                        self._driver.close()
                        time.sleep(1)
                        self._driver.switch_to.window(currentHandle)
            self._driver.quit()
        except Exception as e:
            print(e)
            self._driver.quit()

    def aplhaBooster(self, env):
        windows = self._driver.window_handles
        for window in windows:
            self._driver.switch_to.window(window)
            if env == "Prod":
                if self._driver.title == "Welcome to IBM Sterling File Gateway":
                    self.mainLogic()
                    return self.dictator
            elif env == "PreProd":
                if self._driver.title == '"Sterling File Gateway 6.0 Pre-Prod"':
                    self.mainLogic()
                    return self.dictator
