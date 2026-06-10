import requests
import time
import json
import socket
import main

import sys

algoName = "extTLKC"
algoId = socket.gethostname()
algoIdentity = {"identification":{"name":algoName, "id":algoId}}

def serverHealthcheck():
    while True:
        try:
            healthcheck = requests.get("http://cliandanalyzer:8000/healthcheck")
            if healthcheck.status_code == 200:
                return
        except:
            time.sleep(5)

def mainEntrypoint():
    serverHealthcheck()
    stayActive = True
    while stayActive:
        instructionRequestAnswer = requests.post("http://cliandanalyzer:8000/task", json={"name":algoName, "id":algoId})
        if instructionRequestAnswer.json() != {"instruction":"no_instruction"}:
            print("Received a new instruction.", flush=True)
            print(instructionRequestAnswer.json(), flush=True)
            startInstructionHandler(instructionRequestAnswer.json())
        time.sleep(5)

def collectRequirementsForAlgo():
    t = {"name":"t", "value":"someString", "description":"This tring should be a time value applicable ones are: original, seconds, minutes, hours, days.", "type":"string"}
    l = {"name":"l", "lowerBound":"0", "upperBound":None, "autoAdept":True, "type":"int"}
    k = {"name":"k", "lowerBound":"0", "upperBound":None, "autoAdept":True, "type":"int"}
    c = {"name":"c", "lowerBound":"0.0", "upperBound":"1.0", "autoAdept":True, "type":"float"}
    #logName = {"name":"logName", "value":"someString", "description":"This string is the name of the event log file you want to process.", "type":"string"}
    algoVariables = [t, l, k, c]
    return {**algoIdentity, "inputFormat":"xes", "outputStructure":"eventLog", "requirements":algoVariables}

def startInstructionHandler(instruction):
    print("Entered the instruction block.", flush=True)
    if instruction["instruction"] == "start_n_test":
        print("Accessed n_test function.", flush=True)
        requests.post("http://cliandanalyzer:8000/result/status", json={**algoIdentity, "instructionId":instruction["instructionId"], "status":"network_stable", "fileId":""})
    if instruction == {"instruction":"send_requirements"}:
        print("Accessed requirements function.", flush=True)
        jsonRequirements = collectRequirementsForAlgo()
        requests.post("http://cliandanalyzer:8000/myRequirements", json=jsonRequirements)
    if instruction["instruction"] == "comparison":
        print("Accessed Template function.", flush=True)
        algoDictionary = instruction.get("payload")
        t = "minutes"
        l = 2
        k = 20
        c = 0.5
        logName = "someString"
        for inputValues in algoDictionary["inputParameters"]:
            if inputValues["name"] == "t":
                t = inputValues["value"]
            if inputValues["name"] == "l":
                l = inputValues["value"]
            if inputValues["name"] == "k":
                k = inputValues["value"]
            if inputValues["name"] == "c":
                c = inputValues["value"]
            if inputValues["name"] == "logName":
                logName = inputValues["value"]
        main.executeExtTLKC(t, l, k, c, logName, instruction["instructionId"], algoIdentity["identification"]["id"], instruction["fileId"])
        print("Sending the result of the template function to the server.", flush= True)
        requests.post("http://cliandanalyzer:8000/result/status", json={**algoIdentity, "instructionId":instruction["instructionId"], "status":"finished_privacy_enhancing_algorithm", "fileId":instruction["fileId"]})
    return

if __name__ == "__main__":
    mainEntrypoint()
    #executeExtTLKC() from main.py
