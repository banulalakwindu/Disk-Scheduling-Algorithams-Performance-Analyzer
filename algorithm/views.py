from django.shortcuts import render
from .forms import InputForm

def sum(dataObject):
    sum = 0
    for i in range(len(dataObject)):
        sum += dataObject[i]
    return sum

def fcfs(dataObject, hPos):
    sum = 0
    fcfsarr = []
    for i in range(len(dataObject)):
        sum += abs(hPos - dataObject[i])
        fcfsarr.append(hPos)
        hPos = dataObject[i]
    print(dataObject)
    return (sum, fcfsarr)

def sstf(dataObject, hPos):
    length = len(dataObject)
    sum = 0
    sstfarr = []
    while len(dataObject) != 0:
        min = 100000
        for i in range(len(dataObject)):
            if abs(hPos - dataObject[i]) < min:
                min = abs(hPos - dataObject[i])
                index = i
        sum += min
        sstfarr.append(hPos)
        hPos = dataObject[index]
        dataObject.pop(index)
    return (sum, sstfarr)

def scan(dataObject, hPos, sPos, ePos):
    print(dataObject) 
    sum = 0
    scanarr = []
    dataObject.append(sPos)
    dataObject.append(hPos)
    dataObject.sort()
    index = dataObject.index(hPos)
    
    while index != 0:
        scanarr.append(dataObject[index])
        index -= 1
    while index != len(dataObject)-1:
        scanarr.append(dataObject[index])
        index += 1
    print(dataObject)    
    return (sum, scanarr)  
        
    

def cscan(dataObject, hPos, sPos, ePos):
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

def clook(dataObject, hPos, sPos, ePos):
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
            sPos = request.POST['sPos']
            ePos = request.POST['ePos']
            dataArr = data.split(' ')
            dataobject = map(int, dataArr)
            datalist = list(dataobject)
            (outputFCFS, fcfsarr) = fcfs(datalist, int(hPos))
            outArr.append(outputFCFS)
            (outputSSTF, sstfarr) = sstf(datalist, int(hPos))
            outArr.append(outputSSTF)
            (outputSCAN,scanarr) = scan(datalist, int(hPos), int(sPos), int(ePos))
            outArr.append(outputSCAN)
            outputCSCAN = cscan(datalist, int(hPos), int(sPos), int(ePos))
            outArr.append(outputCSCAN)
            outputCLOOK = clook(datalist, int(hPos), int(sPos), int(ePos))
            outArr.append(outputCLOOK)
            best = algoArr[outArr.index(min(outputFCFS, outputSSTF, outputSCAN, outputCSCAN, outputCLOOK))]
    return render(request, 'processing.html', {'outputFCFS': outputFCFS, 'outputSSTF': outputSSTF, 'outputSCAN': outputSCAN, 'outputCSCAN': outputCSCAN, 'outputCLOOK': outputCLOOK, 'best': best, 'fcfsarr': fcfsarr, 'sstfarr': sstfarr, 'scanarr': scanarr})