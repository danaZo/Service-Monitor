import platform
import hashlib
import subprocess
from typing import TextIO
import psutil
import time
from datetime import date, datetime

fileHash = None
tVal: int
servList = {}

# determine Os type
isWin = False
if platform.system() == 'Windows':
    isWin = True


def getFileHash(fname: str):
    global fileHash
    with open(fname, "rb") as f:
        bytes = f.read()
        return hashlib.sha256(bytes).hexdigest()


def getCurTime() -> str:
    t = date.today()
    t = t.strftime("%d/%m/%Y")
    h = datetime.now()
    h = h.strftime("%H:%M:%S")
    return t + " " + h


def loadDictWin(slist: TextIO, slog: TextIO, isFirstTime: bool):
    global servList
    tempList = {}
    if isFirstTime:
        for s in list(psutil.win_service_iter()):
            s = s.as_dict()
            servList[s['display_name']] = s['status']
            slist.write(f'Service name: {s["display_name"]} , Status: {s["status"]} \n')
    else:
        for s in list(psutil.win_service_iter()):
            # write the service to the log file
            s = s.as_dict()
            tempList[s['display_name']] = s['status']
            slist.write(f'Service name: {s["display_name"]} , Status: {s["status"]} \n')

            # check if the service is new
            if s['display_name'] not in servList:
                slog.write(f'New service: {s["display_name"]}\n')  # write the new event to the log
                print(f'New service: {s["display_name"]}\n')
                tempList[s['display_name']] = s['status']  # add the new service to the watch list

            # check if status changed
            elif tempList[s['display_name']] != servList[s['display_name']]:
                s = f'Service\'s status changed- name: {s["display_name"]} ' \
                    f'old: {servList[s["display_name"]]} new: {s["status"]} \n '
                slog.write(s)
                print(s)
        servList = tempList.copy()


def loadDictLinux(slist: TextIO, slog: TextIO, isFirstTime: bool):
    global servList
    output_str = subprocess.check_output("service --status-all", shell=True).decode("UTF - 8")

    services = output_str.split('\n')

    tempList = {}
    if isFirstTime:
        for s in services[:-1]:
            status = ""  # parse the service status
            s = s.split(' ]  ')
            if s[0][3] == '-':
                status = 'stopped'
            elif s[0][3] == '+':
                status = 'running'
            else:
                status = 'Unknown'
            servList[s[1]] = status
            slist.write(f'Service name: {s[1]} , Status: {status} \n')
    else:
        for s in services[:-1]:
            status = ""  # parse the service status
            s = s.split(' ]  ')
            if s[0][3] == '-':
                status = 'stopped'
            elif s[0][3] == '+':
                status = 'running'
            else:
                status = 'Unknown'
            # write the service to the log file

            tempList[s[1]] = status
            slist.write(f'Service name: {s[1]} , Status: {status} \n')

            # check if the service is new
            if s[1] not in servList:
                slog.write(f'New service: {s[1]}\n')  # write the new event to the log
                print(f'New service: {s[1]}\n')
                tempList[s[1]] = status # add the new service to the watch list

            # check if status changed
            elif tempList[s[1]] != servList[s[1]]:
                s = f'Service\'s status changed- name: {s[1]} ' \
                    f'old: {servList[s[1]]} new: {status} \n '
                slog.write(s)
                print(s)
        servList = tempList.copy()

def getServiceByLineNum(lineNum: int) -> dict:
    slist = open('serverList.txt', 'r')
    servicesList = {}

    for i in range(lineNum + 1):
        slist.readline()
    for line in slist:

        if line == '\n': break  # we reached the end of the service list of this datestamp
        service = line.split(' , ')
        servicesList[service[0][14:]] = service[1][:-1]

    slist.close()
    return servicesList


def getServicesByTimeStamp(reqTime: datetime) -> dict:
    slist = open('serverList.txt', 'r')

    for num, line in enumerate(slist):
        if len(line) > 1 and line[2] == '/':  # the line contain date
            d = datetime.strptime(line[:-1], "%d/%m/%Y %H:%M:%S")
            # check if this date is close enough to the required datetime
            if (reqTime - d).total_seconds() <= tVal:
                slist.close()
                return getServiceByLineNum(num + 1)

    print(f"No data was recorded around {reqTime} ")
    slist.close()


def monitor(timeVal: int):
    global servList, fileHash, tVal
    tVal = int(timeVal)
    # open the log files
    slist = open('serverList.txt', 'w', encoding='utf-8')

    # load the services for the first time
    slist.write("\n" + getCurTime() + "\n\n")
    if isWin:
        loadDictWin(slist, None, True)
    else:
        loadDictLinux(slist,None, True)
    slist.close()
    slog = open('Status_Log.txt', 'w', encoding='utf-8')
    slog.close()
    fileHash = getFileHash("serverList.txt")
    while 1:
        time.sleep(int(timeVal))
        if fileHash != getFileHash('serverList.txt'):
            print("WARNING - LOG CHANGED FROM OUTER SOURCE")
            return
        slist = open('serverList.txt', 'a+', encoding='utf-8')
        slog = open('Status_Log.txt', 'a+', encoding='utf-8')

        slist.write("\n" + getCurTime() + "\n\n")
        if isWin:
            loadDictWin(slist, slog, False)
        else:
            loadDictLinux(slist, slog, False)
        slist.close()
        fileHash = getFileHash('serverList.txt')
        slog.close()


def manualMonitor(d1, d2, tVal):
    global fileHash
    if fileHash != getFileHash('serverList.txt'):
        print("WARNING - LOG CHANGED FROM OUTER SOURCE")
        return

    # get the 2 time samples to compare from the user
    # print("insert the first date")
    year1, mon1, day1, hour1, minute1, sec1 = map(int, d1.split('-'))
    d1 = datetime(year1, mon1, day1, hour1, minute1, sec1)
    # print("insert the second date")
    year2, mon2, day2, hour2, minute2, sec2 = map(int, d2.split('-'))
    d2 = datetime(year2, mon2, day2, hour2, minute2, sec2)
    early = min(d1, d2)
    later = max(d1, d2)

    # get the services from those timestamps
    servicesEarly = getServicesByTimeStamp(early)
    servicesLate = getServicesByTimeStamp(later)

    # compare the two dicts
    setEarly = set(servicesEarly.keys())
    setLate = set(servicesLate.keys())
    newServices = setLate - setEarly
    sharedServices = set.intersection(setEarly, setLate)
    print(f"\n\n Comparing changes between the logs from {d1} to {d2}\n\n")
    for s in newServices:
        print(f'New service: {s}')

    for s in sharedServices:
        # check if status changed
        if servicesEarly[s] != servicesLate[s]:
            print(f'Service\'s status changed, name: {s} Old {servicesEarly[s]}, New {servicesLate[s]}')
    print("\n\nBack to automatic monitor mode")


if __name__ == '__main__':
    tVal = int(input("Select a time interval in seconds: "))
    monitor(tVal)
