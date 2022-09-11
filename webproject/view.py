from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render
import pickle
import numpy as np
import os
from pandas.core.indexes.base import Index 
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
import pandas as pd
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt


dataPath = os.path.join(os.getcwd(),"webproject","data") 
bostonPath = os.path.join(dataPath,"boston","boston.txt")
bankPath = os.path.join(dataPath,"bank","bank.txt")
fraudPath = os.path.join(dataPath,"fraud","fraud.txt")
toxicPath = os.path.join(dataPath,"toxic","toxic.txt")

data = ["boston","bank","fraud","toxic"]
pathLs = [bankPath,bostonPath,fraudPath,toxicPath]
headLs = dict()

def write_csv(path,df):
    with open(path, 'a+', newline='') as f:
        df.to_csv(f, mode='a',header=False, index = False)
        print("Appended to result.csv")

def create_csv(headLs, dataPath, data):
    for name in data:
        temp = os.path.join(dataPath,name,"result.csv")
       
        if not os.path.exists(temp):
            # open(temp,'w').close()
            with open(temp, 'w', newline='') as outcsv:
                writer = csv.writer(outcsv)
                writer.writerow(headLs[name])
        else:
            print(name," - result.csv exists")

        # headTemp = headLs[name]
        # print(headTemp)
        # df = pd.read_csv(temp)
        # df.to_csv(temp,header=headTemp,index=False)

with open(bankPath) as f1:
    bankContent = f1.read().splitlines()
    headLs["bank"] = bankContent[0].replace(" ","").split(",") 

with open(bostonPath) as f2:
    bostonContent = f2.read().splitlines()
    headLs["boston"] = bostonContent[0].replace(" ","").split(",") 

with open(fraudPath) as f3:
    fraudContent = f3.read().splitlines()
    headLs["fraud"] = fraudContent[0].replace(" ","").split(",") 

with open(toxicPath) as f4:
    toxicContent = f4.read().splitlines()
    headLs["toxic"] = toxicContent[0].replace(" ","").split(",") 

#bank mapping
def bankMapper(dataPath):
    tempPath = os.path.join(dataPath,"bank","bankMap.txt")

    with open(tempPath, encoding='utf-8') as f:
        bankMap = f.read().splitlines()

    bankCategory = bankMap[0].replace(" ","").split(",")
 
    bankMap = bankMap[1:]

    bankDict = dict()
   
    count = 0
    for cat in bankCategory:
        bankVal = bankMap[count].replace(" ","").split(",")
        bankKey = bankMap[count+1].replace(" ","").split(",")   
        for key, value in zip(bankKey,bankVal):
            bankDict[cat] = bankDict.get(cat,{})
            bankDict[cat][key] = value
     
        count+=2
    # print(bankDict)

    return bankDict

#homepage
def home(request):
    # return HttpResponse("hello world")
    return render(request,"home.html")

#bank classification
@api_view(['POST'])
def bankOut(request):
  
    inputData = json.loads(request.body.decode("utf-8"))
    # print(inputData)

    
    file = open("./model/bank_1.pkl",'rb')
    model = pickle.load(file)
    file.close()
    temp = inputData["sample"]
    input = np.array(temp)
    input = input.astype(np.float)
    input = np.reshape(input,(1,-1))

    ans = model.predict(input)
    # print(ans)
    ans = ans[0]
    output = temp
    tempans = str(float(ans))

    if ans == 0:
        ans = "no"
    else: 
        ans = "yes"

    output.append(tempans)

    pathway = os.path.join(dataPath,"bank","result.csv")
    df = pd.DataFrame([output])
    write_csv(pathway,df)
    
    return Response(ans)


#bank fields
@api_view(['GET'])
def getBank(request):
    input = bankContent[0].split(",")
    input = input[:-1]

    sample = selectBank.split(",")
    sample = sample[:-1]

    output = {
        "field":input,
        "sample":sample,
        "bankMap":bankMap
    }
    
    # print(input)
    # print("==============\n",sample)
    return Response(output)


#bank page
def bank(request):

    file = open("./model/bank_1.pkl",'rb')
    model = pickle.load(file)
    file.close()

    input = selectBank.replace(" ","").split(",")
    # print(input)
    target = int(input[-1][0])

    if target == 0:
        target = "no"
    else: 
        target = "yes"

    return render(request,"bank.html",{'target':target,'model':model})


#bank classification
@api_view(['POST'])
def houseOut(request):
  
    inputData = json.loads(request.body.decode("utf-8"))
    # print(inputData)

    
    file = open("./model/boston_11.pkl",'rb')
    model = pickle.load(file)
    file.close()
    temp = inputData["sample"]
    output = temp
    input = np.array(temp)
    input = input.astype(np.float)
    input = np.reshape(input,(1,-1))

    ans = model.predict(input)
    # print(ans)
    ans = ans[0]
    tempans = str(float(ans))
    output.append(tempans)
    # print(output)
    pathway = os.path.join(dataPath,"boston","result.csv")
    df = pd.DataFrame([output])
    write_csv(pathway,df)

    return Response(ans)

#bank fields
@api_view(['GET'])
def getHouse(request):
    input = bostonContent[0].split(",")
    input = input[:-1]
    
    sample = selectBoston.split(",")
    sample = sample[:-1]
    output = {
        "field":input,
        "sample":sample
    }

    return Response(output)
    
def house(request):
   
    file = open("./model/boston_11.pkl",'rb')
    model = pickle.load(file)
    file.close()

    input = selectBoston.split(",")
    # print(input)
    target = input[-1]

    bostonDetails = os.path.join(dataPath,"boston","details.txt")
    
    with open(bostonDetails) as fd:
        bostonDesc = fd.readlines()
    
    # print(bostonDesc)
    return render(request,"house.html",{'target':target,'model':model,'details':str(bostonDesc)})

@api_view(['POST'])
def regressOut(request):
  
    inputData = json.loads(request.body.decode("utf-8"))
    # print(inputData)
    
    file = open("./model/boston_11.pkl",'rb')
    model = pickle.load(file)
    file.close()
    temp = inputData["sample"]
    output = temp
    input = np.array(temp)
    input = input.astype(np.float)
    input = np.reshape(input,(1,-1))

    ans = model.predict(input)
    # print(ans)
    ans = ans[0]
    tempans = str(float(ans))
    output.append(tempans)
    # print(output)
    pathway = os.path.join(dataPath,"boston","result.csv")
    df = pd.DataFrame([output])
    write_csv(pathway,df)

    return Response(ans)

#bank fields
@api_view(['GET'])
def getRegressor(request):
    input = bostonContent[0].split(",")
    input = input[:-1]
    
    sample = selectBoston.split(",")
    sample = sample[:-1]
    output = {
        "field":input,
        "sample":sample
    }

    return Response(output)


#credit card fraud classification    
def fraud(request):
    file = open("./model/fraud_1.pkl",'rb')
    model = pickle.load(file)
    file.close()

    input = selectFraud.split(",")
    # print(input)
    target = input[-1]

    if target == 0:
        target = "no"
    else: 
        target = "yes"

    return render(request,"fraud.html",{'target':target,'model':model})

@api_view(['POST'])
def fraudOut(request):
  
    inputData = json.loads(request.body.decode("utf-8"))
    # print(inputData)
    
    file = open("./model/fraud_1.pkl",'rb')
    model = pickle.load(file)
    file.close()
    temp = inputData["sample"]
    print(inputData["field"])
    print(temp)
    input = np.array(temp)
    input = input.astype(np.float)
    input = np.reshape(input,(1,-1))

    ans = model.predict(input)
    # print(ans)
    ans = ans[0]
    output = temp
    tempans = str(float(ans))

    if ans == 0:
        ans = "no"
    else: 
        ans = "yes"

    output.append(tempans)

    pathway = os.path.join(dataPath,"fraud","result.csv")
    df = pd.DataFrame([output])
    write_csv(pathway,df)
    
    return Response(ans)

#bank fields
@api_view(['GET'])
def getFraud(request):
    input = fraudContent[0].split(",")
    input = input[:-1]
    
    sample = selectFraud.split(",")
    sample = sample[:-1]
    output = {
        "field":input,
        "sample":sample
    }

    return Response(output)


#credit card fraud classification    
def toxic(request):

    file = open("./model/toxic/comments_temp.pkl",'rb')
    model = pickle.load(file)
    file.close()
    
    input = selectToxic.split(",")
    # print(input)
    target = input[-1]

    # print(bostonDesc)
    return render(request,"toxic.html",{'target':target,'model':model})


@api_view(['POST'])
def toxicOut(request):
    inputData = json.loads(request.body.decode("utf-8"))
    # print(inputData)
    
    file = open("./model/toxic/comments_temp.pkl",'rb')
    model = pickle.load(file)
    file.close()
    temp = inputData["sample"][0]
    filename = "./model/toxic/tfifd_189775.pkl"
    vect = TfidfVectorizer(analyzer='word',stop_words='english',vocabulary=pickle.load(open(filename,"rb")))
    text_trans = vect.fit_transform([temp])

    ans = model.predict(text_trans)[0]

    tempans = ans

    if ans == 0:
        ans = "no"
    else: 
        ans = "yes"

    pathway = os.path.join(dataPath,"toxic","result.csv")
    df = pd.DataFrame([[temp,tempans]])
    write_csv(pathway,df)
    
    return Response(ans)

#bank fields
@api_view(['GET'])
def getToxic(request):
    input = toxicContent[0].split(",")
    input = input[:-1]
    
    sample = selectToxic.split(",")
    sample = sample[:-1]
    output = {
        "field":input,
        "sample":sample
    }
    return Response(output)

n = 2
selectBank = bankContent[n]
selectBoston = bostonContent[n]
selectToxic = toxicContent[n]
selectFraud = fraudContent[n]

create_csv(headLs, dataPath,data)
bankMap = bankMapper(dataPath)