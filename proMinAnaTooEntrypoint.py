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
    l = {"name":"l", "lowerBound":"2", "upperBound":"2", "type":"int"}
    k = {"name":"k", "lowerBound":"20", "upperBound":"20", "type":"int"}
    c = {"name":"c", "lowerBound":"0.5", "upperBound":"0.5", "type":"float"}
    logName = {"name":"logName", "value":"someString", "description":"This string is the name of the event log file you want to process.", "type":"string"}
    algoVariables = [t, l, k, c, logName]
    return {**algoIdentity, "requirements":algoVariables}

def startInstructionHandler(instruction):
    print("Entered the instruction block.", flush=True)
    if instruction == {"instruction":"start_n_test"}:
        print("Accessed n_test function.", flush=True)
        requests.post("http://cliandanalyzer:8000/result/status", json={**algoIdentity, "status":"network_stable"})
    if instruction == {"instruction":"send_requirements"}:
        print("Accessed requirements function.", flush=True)
        jsonRequirements = collectRequirementsForAlgo()
        requests.post("http://cliandanalyzer:8000/myRequirements", json=jsonRequirements)
    if isinstance(instruction.get("instruction"), dict):
        print("Accessed Template function.", flush=True)
        algoDictionary = instruction.get("instruction")
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
        main.executeExtTLKC(t, l, k, c, logName)
    return

if __name__ == "__main__":
    mainEntrypoint()
    #executeExtTLKC() from main.py
