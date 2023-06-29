from django.shortcuts import render
from .forms import InputForm

def fcfs(dataObject, hPos):
    dataObjectforFCFS = dataObject.copy()
    sum = 0
    fcfsarr = []
    for i in range(len(dataObjectforFCFS)):
        sum += abs(hPos - dataObjectforFCFS[i])
        fcfsarr.append(hPos)
        hPos = dataObjectforFCFS[i]
    return (sum, fcfsarr)

def sstf(dataObject, hPos):
    dataObjectforSSTF = dataObject.copy()
    sum = 0
    sstfarr = []
    while len(dataObjectforSSTF) != 0:
        min = 100000
        for i in range(len(dataObjectforSSTF)):
            if abs(hPos - dataObjectforSSTF[i]) < min:
                min = abs(hPos - dataObjectforSSTF[i])
                index = i
        sum += min
        sstfarr.append(hPos)
        hPos = dataObjectforSSTF[index]
        dataObjectforSSTF.pop(index)
    return (sum, sstfarr)

def scan(dataObject, hPos, sPos, ePos):
    dataObjectforSCAN = dataObject.copy()
    sum = 0
    scanarr = []
    dataObjectforSCAN.append(hPos)
    dataObjectforSCAN.sort()
    index = dataObjectforSCAN.index(hPos)
    if index < len(dataObjectforSCAN)/2:
        for i in range(index, -1, -1):
            sum += abs(dataObjectforSCAN[i] - dataObjectforSCAN[i-1])
    else:
        for i in range(index, len(dataObjectforSCAN)-1):
            sum += abs(dataObjectforSCAN[i] - dataObjectforSCAN[i+1])
    return (sum, scanarr)

def cscan(dataObject, hPos, sPos, ePos):
    dataObjectforCSCAN = dataObject.copy()
    sum = 0
    dataObjectforCSCAN.append(hPos)
    dataObjectforCSCAN.sort()
    index = dataObjectforCSCAN.index(hPos)
    for i in range(index, len(dataObjectforCSCAN)-1):
        sum += abs(dataObjectforCSCAN[i] - dataObjectforCSCAN[i+1])
    sum += abs(dataObjectforCSCAN[len(dataObjectforCSCAN)-1] - dataObjectforCSCAN[0])
    for i in range(0, index):
        sum += abs(dataObjectforCSCAN[i] - dataObjectforCSCAN[i+1])
    return sum

def clook(dataObject, hPos, sPos, ePos):
    dataObjectforCLOOK = dataObject.copy()
    sum = 0
    dataObjectforCLOOK.append(hPos)
    dataObjectforCLOOK.sort()
    index = dataObjectforCLOOK.index(hPos)
    for i in range(index, len(dataObjectforCLOOK)-1):
        sum += abs(dataObjectforCLOOK[i] - dataObjectforCLOOK[i+1])
    for i in range(0, index):
        sum += abs(dataObjectforCLOOK[i] - dataObjectforCLOOK[i+1])
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
            (outputSCAN, scanarr) = scan(datalist, int(hPos), int(sPos), int(ePos))
            outArr.append(outputSCAN)
            outputCSCAN = cscan(datalist, int(hPos), int(sPos), int(ePos))
            outArr.append(outputCSCAN)
            outputCLOOK = clook(datalist, int(hPos), int(sPos), int(ePos))
            outArr.append(outputCLOOK)
            best = algoArr[outArr.index(min(outputFCFS, outputSSTF, outputSCAN, outputCSCAN, outputCLOOK))]
    return render(request, 'processing.html', {'outputFCFS': outputFCFS, 'outputSSTF': outputSSTF, 'outputSCAN': outputSCAN, 'outputCSCAN': outputCSCAN, 'outputCLOOK': outputCLOOK, 'best': best, 'fcfsarr': fcfsarr, 'sstfarr': sstfarr})