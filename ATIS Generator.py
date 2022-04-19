import os
import time
import winsound
import requests

###################################################
key = "PUT YOUR KEY HERE"
###################################################

voiceUrl = "http://api.voicerss.org/?key=" + key + "&hl=en-gb&v=Harry&c=MP3&f=8khz_8bit_mono&src="

voiceTemplate = """{airport} INFORMATION {letter}, TIME {validTime} zulu.
DEPARTURE RUNWAY {departureRunway}, ARRIVAL RUNWAY {arrivalRunway}.
TRANSITION LEVEL FLIGHT LEVEL 1 5, SURFACE WIND VARIABLE.
VISIBILITY 10 KILOMETRES OR MORE.
TEMPERATURE PLUS 6, DEW POINT PLUS 5.
QNH 1 0 1 3 HECTOPASCALS.
ACKNOWLEDGE RECEIPT OF INFORMATION {letter}.
AND ADVISE AIRCRAFT TYPE ON FIRST CONTACT"""

textTemplate = """{airport} ATIS Information {letter}.
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
Valid as of {validTime}z.

Airspace Ceiling: FL060

Departure Runway: {departureRunway}
Arrival Runway: {arrivalRunway}
Max Taxi Speed: 25kts

Advise aircraft type on first contact and advise you have information {letter} onboard.

NOTAMS:
- Realistic emergencies are authorised.
- Providing top-down control over airspace.
- All aircraft must use latest charts (https://github.com/Treelon/ptfs-charts/tree/main/).
- PDC is avaliable (you may request and recieve IFR clearance in game chat)."""

phoneticNumbers = ["zero", "one", "two", "tree", "four", "fife", "six", "seven", "eight", "niner"]
phoneticAlphabet = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa", "quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey", "x-ray", "yankee", "zulu"]

atisLetterCode = -1

def updateAtisLetter():
    global atisLetterCode
    atisLetterCode += 1

    if atisLetterCode > 25:
        atisLetterCode -= 26
      
    return chr(65 + atisLetterCode)

def fetchUTCTime():
    utcTime = time.gmtime()
    hourString = str(utcTime.tm_hour)
    minuteString = str(utcTime.tm_min)

    if utcTime.tm_hour < 10:
        hourString = "0" + hourString

    if utcTime.tm_min < 10:
        minuteString = "0" + minuteString

    return hourString + minuteString

def phoneticRunway(runway):
    runwaySplit = list(runway)

    if len(runway) == 2:
        runwaySplit.append("")
    
    runwaySplit[0] = phoneticNumbers[int(runwaySplit[0])]
    runwaySplit[1] = phoneticNumbers[int(runwaySplit[1])]

    match runwaySplit[2]:
        case "L":
            runwaySplit[2] = "left"
        case "R":
            runwaySplit[2] = "right"
        case "C":
            runwaySplit[2] = "centre"

    return " ".join(runwaySplit)

def runwaysToVoice(runwayList):
    runwayString = phoneticRunway(runwayList[0])

    if len(runwayList) > 1:
        runwayList.pop(0)

        for runway in runwayList:
            runwayString = runwayString + " AND " + phoneticRunway(runway)

    return runwayString



print("ATIS Generator - Do not close this window if you want ATIS to be automatically generated every 30 minutes.")
print("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
airport = input("Airport Name: ")
departureRunwayInput = input("Departure Runway: ").upper().split("/")
arrivalRunwayInput = input("Arrival Runway: ").upper().split("/")
print("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")

departureRunways = '/'.join(departureRunwayInput)
phoneticDepartureRunways = runwaysToVoice(departureRunwayInput)

arrivalRunways = '/'.join(arrivalRunwayInput)
phoneticArrivalRunways = runwaysToVoice(arrivalRunwayInput)

while True:
    atisTime = fetchUTCTime()
    atisLetter = updateAtisLetter()
    phoneticAtisTime = phoneticNumbers[int(atisTime[0])] + " " + phoneticNumbers[int(atisTime[1])] + " " + phoneticNumbers[int(atisTime[2])] + " " + phoneticNumbers[int(atisTime[3])]
    
    textAtis = textTemplate.format(airport = airport.title(), letter = atisLetter, validTime = atisTime, departureRunway = departureRunways, arrivalRunway = arrivalRunways)
    voiceAtis = voiceTemplate.format(airport = airport.title(), letter = phoneticAlphabet[atisLetterCode], validTime = phoneticAtisTime, departureRunway = phoneticDepartureRunways, arrivalRunway = phoneticArrivalRunways)

    file = open("ATIS.txt", "w", encoding="utf-8")
    file.write(textAtis)
    file.close()

    voiceAtisRequest = requests.get(voiceUrl + voiceAtis)
    file = open('ATIS.mp3', 'wb')
    file.write(voiceAtisRequest.content)
    file.close()

    winsound.Beep(750, 750)
    print(atisTime + "z | Information " + atisLetter)

    os.startfile("ATIS.txt")

    time.sleep(30 * 60)
