#!/usr/bin/env python

"""
Script by Théo Lopez 
Do not share.
"""
from python_get_resolve import GetResolve
import time
import random
import string

#Varaibles globales à modifier
TARGET_DIR = "/Users/theolopez/Desktop/STILLS/"
PROJECT_PREFIX = "CAV"
PRESET_NAME = "EXPORT_STILL"

#Récupère le nom du clip à partir du numéro de frame
def getClipNameByFrameNumber(frameNumber, project):
    timeline = project.GetCurrentTimeline()
    itemsInTimeline = timeline.GetItemsInTrack("video", 1)
    startFrame = timeline.GetStartFrame()
    for key, value in itemsInTimeline.items():
        try:
            if(itemsInTimeline[key].GetStart()-startFrame <= frameNumber <= itemsInTimeline[key+1].GetStart()-startFrame):
                return itemsInTimeline[key].GetName()
        except:
            return itemsInTimeline[key].GetName()
    random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
    return random_string #si le clip n'est pas trouvé (ça ne doit pas arriver), on génère un nom aléatoire

#Demande à l'utilisateur de choisir une couleur de marqueur
def askForMarkerColor(listOfMarkers):
    print("You have differents markers color. Please choose the marker color from the list, or press enter if you want to use them all :")
    markersColors = []
    for key, value in listOfMarkers.items():
        if(value["color"] not in markersColors):
            markersColors.append(value["color"])
    for color in markersColors:
        print(markersColors.index(color)+1,")", color)
    
    colorChoice = input()
    if(colorChoice != ""):
        try:
            colorChoice = int(colorChoice)
        except:
            print("Please enter a number")
            askForMarkerColor(listOfMarkers)
    
    #si colorchoice est dans le range de la liste et si colorchoice n'est pas vide
    if(colorChoice in range(1, len(markersColors)+1) and colorChoice != ""):
        print("You choose the color", markersColors[colorChoice-1])
        markersColors = [markersColors[colorChoice-1]]
        return markersColors[0]
    #sinon, si colorchoice est vide
    elif(colorChoice == ""):
        print("You choose all colors")
        return "All"
    #si c'est autre chose, relancer askForMarkerColor
    else:
        print('Please enter a number between 1 and', len(markersColors))
        askForMarkerColor(listOfMarkers)

def listMarkersByColor(listOfMarkers, color):
    markers = []
    if color == "All":
        return listOfMarkers.keys()
    for key, value in listOfMarkers.items():
        if(value["color"] == color):
            markers.append(key)
    return markers

#Récupère tous les marqueurs d'une timeline et les envoie en export
def getMarkersOfTimeline(timelineIndex, project):
    timeline = project.GetTimelineByIndex(timelineIndex)
    markers = timeline.GetMarkers()
    
    colorSelected = askForMarkerColor(markers)
    print("COLOR SELECTED :", colorSelected)
    selectedMarkers = listMarkersByColor(markers, colorSelected)
    liste = selectedMarkers

    directory = TARGET_DIR+"/STILLS/"
    print("Markers are located at", liste)
    project.SetCurrentTimeline(timeline) 
    print("***") 
    for frameNumber in liste:
        clipName = getClipNameByFrameNumber(frameNumber, project)
        clipName = clipName.split(".")[0]
        print('Creating job for', clipName, 'at frame', frameNumber, '…')
        startFrame = timeline.GetStartFrame()
        project.LoadRenderPreset(PRESET_NAME)
        project.SetRenderSettings({"SelectAllFrames":False, "MarkIn":startFrame+frameNumber, "MarkOut":startFrame+frameNumber, "TargetDir":directory, "CustomName":PROJECT_PREFIX+'_'+clipName+"_"+str(frameNumber)})
        project.AddRenderJob()
    print("***")
    print('All jobs added to render queue. Please verify and start render manually.')


#Demander si l'on supprime tous les jobs en cours
def AskDeleteAllRenderJob(project):
    res = input("Do you want to delete previous render jobs ? [y/n] (default YES)")
    if(res == "" or res =="y" or res == "Y"):
        print("Deleting old render jobs…")
        time.sleep(1)
        project.DeleteAllRenderJobs() #delete all jobs
    elif(res == "n" or res =="N"):
        print("Old render jobs will be kept.")
    else:
        AskDeleteAllRenderJob(project)

#Demander à l'utilisateur de choisir une timeline
def chooseTimeline(project):
    print('Please choose a timeline from this list :')
    timelineCount = project.GetTimelineCount()
    inc = 1
    for i in range(timelineCount):
        timeline = project.GetTimelineByIndex(i+1)
        name = timeline.GetName()
        print(str(inc)+') '+name)
        inc+=1
    timelineChoice = int(input())
    print("Sending timeline\"", project.GetTimelineByIndex(timelineChoice).GetName(), "\"for marker analysis…")
    return timelineChoice


# Get currently open project
resolve = GetResolve()
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()

print('Welcome. This script will export stills from a Davinci Resolve timeline.')
selectedTimeline = chooseTimeline(project)
AskDeleteAllRenderJob(project)
getMarkersOfTimeline(selectedTimeline, project)