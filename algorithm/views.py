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
    fcfsarr.append(hPos)
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
    sstfarr.append(hPos)
    return (sum, sstfarr)

def scan(dataObject, hPos, sPos):
    dataObjectforSCAN = dataObject.copy()
    sum = 0
    scanarr = []
    dataObjectforSCAN.append(hPos)
    dataObjectforSCAN.append(sPos)
    dataObjectforSCAN.sort()
    index = dataObjectforSCAN.index(hPos)
    for i in range(index,-1,-1):
        scanarr.append(dataObjectforSCAN[i])
    for i in range(index+1,len(dataObjectforSCAN)):
        scanarr.append(dataObjectforSCAN[i])
    #total head movement
    for i in range(len(scanarr)-1):
        sum += abs(scanarr[i] - scanarr[i+1])
    return (sum, scanarr)

def cscan(dataObject, hPos, sPos, ePos):
    dataObjectforCSCAN = dataObject.copy()
    sum = 0
    cscanarr = []
    dataObjectforCSCAN.append(hPos)
    dataObjectforCSCAN.append(sPos)
    dataObjectforCSCAN.append(ePos)
    dataObjectforCSCAN.sort()
    index = dataObjectforCSCAN.index(hPos)
    for i in range(index,len(dataObjectforCSCAN)):
        cscanarr.append(dataObjectforCSCAN[i])
    for i in range(0,index):
        cscanarr.append(dataObjectforCSCAN[i])
    #total head movement
    for i in range(len(cscanarr)-1):
        sum += abs(cscanarr[i] - cscanarr[i+1])
    return (sum, cscanarr)

def clook(dataObject, hPos):
    dataObjectforCLOOK = dataObject.copy()
    clookarr = []
    sum = 0
    dataObjectforCLOOK.append(hPos)
    dataObjectforCLOOK.sort()
    index = dataObjectforCLOOK.index(hPos)
    for i in range(index,len(dataObjectforCLOOK)):
        clookarr.append(dataObjectforCLOOK[i])
    for i in range(0,index):
        clookarr.append(dataObjectforCLOOK[i])
    #total head movement
    for i in range(len(clookarr)-1):
        sum += abs(clookarr[i] - clookarr[i+1])
    return (sum, clookarr)

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
            (outputSCAN, scanarr) = scan(datalist, int(hPos), int(sPos))
            outArr.append(outputSCAN)
            (outputCSCAN,cscanarr) = cscan(datalist, int(hPos), int(sPos), int(ePos))
            outArr.append(outputCSCAN)
            (outputCLOOK,clookarr) = clook(datalist, int(hPos))
            outArr.append(outputCLOOK)
            best = algoArr[outArr.index(min(outputFCFS, outputSSTF, outputSCAN, outputCSCAN, outputCLOOK))]
    return render(request, 'processing.html', {'outputFCFS': outputFCFS, 'outputSSTF': outputSSTF, 'outputSCAN': outputSCAN, 'outputCSCAN': outputCSCAN, 'outputCLOOK': outputCLOOK, 'best': best, 'fcfsarr': fcfsarr, 'sstfarr': sstfarr, 'scanarr': scanarr,'cscanarr': cscanarr, 'clookarr': clookarr })