from django.shortcuts import render
from .forms import InputForm

def sum(dataObject):
    sum = 0
    for i in range(len(dataObject)):
        sum += dataObject[i]
    return sum

def fcfs(dataObject, hPos):
    sum = 0
    for i in range(len(dataObject)):
        sum += abs(hPos - dataObject[i])
        hPos = dataObject[i]
    average = sum / len(dataObject)
    return average

def sstf(dataObject, hPos):
    length = len(dataObject)
    sum = 0
    while len(dataObject) != 0:
        min = 100000
        for i in range(len(dataObject)):
            if abs(hPos - dataObject[i]) < min:
                min = abs(hPos - dataObject[i])
                index = i
        sum += min
        hPos = dataObject[index]
        dataObject.pop(index)
        average = sum / length
    return average

def scan(dataObject, hPos):
    sum = 0
    dataObject.append(hPos)
    dataObject.sort()
    index = dataObject.index(hPos)
    if index < len(dataObject)/2:
        for i in range(index, -1, -1):
            sum += abs(dataObject[i] - dataObject[i-1])
    else:
        for i in range(index, len(dataObject)-1):
            sum += abs(dataObject[i] - dataObject[i+1])
    return sum

def cscan(dataObject, hPos):
    sum = 0
    dataObject.append(hPos)
    dataObject.sort()
    index = dataObject.index(hPos)
    for i in range(index, len(dataObject)-1):
        sum += abs(dataObject[i] - dataObject[i+1])
    sum += abs(dataObject[len(dataObject)-1] - dataObject[0])
    for i in range(0, index):
        sum += abs(dataObject[i] - dataObject[i+1])
    return sum

def clook(dataObject, hPos):
    sum = 0
    dataObject.append(hPos)
    dataObject.sort()
    index = dataObject.index(hPos)
    for i in range(index, len(dataObject)-1):
        sum += abs(dataObject[i] - dataObject[i+1])
    for i in range(0, index):
        sum += abs(dataObject[i] - dataObject[i+1])
    return sum

def home(request):
    form = InputForm()
    return render(request, 'home.html', {'form': form})

def processing(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            algoArr = ['FCFS', 'SSTF', 'SCAN', 'CSCAN', 'CLOOK']
            outArr = []
            data = request.POST['data']
            hPos = request.POST['hPos']
            dataArr = data.split(' ')
            dataobject = map(int, dataArr)
            datalist = list(dataobject)
            outputFCFS = fcfs(datalist, int(hPos))
            outArr.append(outputFCFS)
            outputSSTF = sstf(datalist, int(hPos))
            outArr.append(outputSSTF)
            outputSCAN = scan(datalist, int(hPos))
            outArr.append(outputSCAN)
            outputCSCAN = cscan(datalist, int(hPos))
            outArr.append(outputCSCAN)
            outputCLOOK = clook(datalist, int(hPos))
            outArr.append(outputCLOOK)
            best = algoArr[outArr.index(min(outputFCFS, outputSSTF, outputSCAN, outputCSCAN, outputCLOOK))]
    return render(request, 'processing.html', {'outputFCFS': outputFCFS, 'outputSSTF': outputSSTF, 'outputSCAN': outputSCAN, 'outputCSCAN': outputCSCAN, 'outputCLOOK': outputCLOOK, 'best': best})