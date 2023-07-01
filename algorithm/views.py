from django.shortcuts import render
from .forms import InputForm
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def generate_chart(dataObject, title):
    order_of_execution = dataObject.copy()
    # Create y-coordinates for track numbers
    y_coords = range(1, len(order_of_execution) + 1)
    order_of_execution = order_of_execution[::-1]

    # Create a scatter plot
    plt.scatter(order_of_execution, y_coords)

    # Add arrows indicating the movement between execution points
    for i in range(len(order_of_execution) - 1):
        plt.annotate("", xy=(order_of_execution[i + 1], y_coords[i + 1]), xytext=(order_of_execution[i], y_coords[i]),
                     arrowprops=dict(arrowstyle="<-", color="black"))

    # Add vertical dot lines
    for x in order_of_execution:
        plt.vlines(x, ymin=1, ymax=len(order_of_execution),
                   colors='gray', linestyles='dotted')

    # Customize the chart
    plt.xlabel('Execution Point', fontsize=10)
    plt.ylabel('Track Number')
    plt.title(title, fontsize=16, fontweight='bold', color='green')

    # Set x-ticks to show execution points
    plt.xticks(order_of_execution, rotation=90)

    # Save the chart to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the chart image to a base64 string
    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Clear the current figure
    plt.clf()

    return chart_image


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
    for i in range(index, -1, -1):
        scanarr.append(dataObjectforSCAN[i])
    for i in range(index+1, len(dataObjectforSCAN)):
        scanarr.append(dataObjectforSCAN[i])
    # total head movement
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
    for i in range(index, len(dataObjectforCSCAN)):
        cscanarr.append(dataObjectforCSCAN[i])
    for i in range(0, index):
        cscanarr.append(dataObjectforCSCAN[i])
    # total head movement
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
    for i in range(index, len(dataObjectforCLOOK)):
        clookarr.append(dataObjectforCLOOK[i])
    for i in range(0, index):
        clookarr.append(dataObjectforCLOOK[i])
    # total head movement
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
            (outputCSCAN, cscanarr) = cscan(
                datalist, int(hPos), int(sPos), int(ePos))
            outArr.append(outputCSCAN)
            (outputCLOOK, clookarr) = clook(datalist, int(hPos))
            outArr.append(outputCLOOK)
            best = algoArr[outArr.index(
                min(outputFCFS, outputSSTF, outputSCAN, outputCSCAN, outputCLOOK))]
            fcfs_chart = generate_chart(fcfsarr, "FCFS")
            sstf_chart = generate_chart(sstfarr, "SSTF")
            scan_chart = generate_chart(scanarr, "SCAN")
            cscan_chart = generate_chart(cscanarr, "CSCAN")
            clook_chart = generate_chart(clookarr, "CLOOK")
    return render(request, 'processing.html', {'outputFCFS': outputFCFS, 'outputSSTF': outputSSTF, 'outputSCAN': outputSCAN, 'outputCSCAN': outputCSCAN, 'outputCLOOK': outputCLOOK, 'best': best, 'fcfsarr': fcfsarr, 'sstfarr': sstfarr, 'scanarr': scanarr, 'cscanarr': cscanarr, 'clookarr': clookarr, 'fcfs_chart': fcfs_chart, 'sstf_chart': sstf_chart, 'scan_chart': scan_chart, 'cscan_chart': cscan_chart, 'clook_chart': clook_chart})
