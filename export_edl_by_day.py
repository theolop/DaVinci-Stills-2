#!/usr/bin/env python

"""
New comment ! 
"""
from python_get_resolve import GetResolve
import json
import time

TARGET_DIR = "/Volumes/SUBMERGEE_RAID/EXPORTS/"
PROJECT_PREFIX = "SUB"
PRESET_NAME = "EXPORT_STILL"

def exportToEDL(timeline, project, folder, rootFolder):
    newTimelineName = timeline.GetName()+'_copy'
    newTimeline = timeline.DuplicateTimeline(newTimelineName)
    numberOfAudioTracks = newTimeline.GetTrackCount("audio")
    print(numberOfAudioTracks)
    # for i in range(numberOfAudioTracks):
    #      print(i+1)
    #      newTimeline.DeleteTrack("audio", i+1)

    newTimeline.DeleteTrack("audio", 4)
    

def getTimelines(clip, project, folder, rootFolder):
    timelineCount = project.GetTimelineCount()
    inc = 1
    for i in range(timelineCount):
        timeline = project.GetTimelineByIndex(i+1)
        inc+=1
        name = timeline.GetName()
        if name == clip.GetName():
            print ('Timeline ', timeline.GetName(), ', ready to be exported to EDL…')
            exportToEDL(timeline, project, folder, rootFolder)




def DisplayTimelinesInfo( folder, displayShift, project, rootFolder ):
    print(displayShift + "- " + folder.GetName())
    clips = folder.GetClipList()
    for clip in clips:
        #print(displayShift + "  " + clip.GetClipProperty("File Name"))
        if clip.GetClipProperty()["Video Codec"] == "" and clip.GetClipProperty()["Audio Codec"] == "" :
            print(displayShift, "TL :", clip.GetClipProperty("File Name"))
            getTimelines(clip, project, folder, rootFolder)

    displayShift = "  " + displayShift

    folders = folder.GetSubFolderList()
    for folder in folders:
        DisplayTimelinesInfo(folder, displayShift, project, rootFolder)
    return

def getTimelinesOfFolder(folder, displayShift, project, rootFolder):
    clips = folder.GetClipList()
    print(folder.GetName())
    DisplayTimelinesInfo(folder, " ", project, rootFolder)


def DisplayRootFolders( project ):
    mediaPool = project.GetMediaPool()
    folder = mediaPool.GetRootFolder()
    folders = folder.GetSubFolderList()
    i = 1
    foldersList = []
    for folder in folders:
        print(str(i),") ",folder.GetName())
        foldersList.append(folder)
        i+=1
    folderChoice = input()
    getTimelinesOfFolder(foldersList[int(folderChoice)-1], "", project, foldersList[int(folderChoice)-1] )
    return




# Get currently open project
resolve = GetResolve()
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()

DisplayRootFolders(project)

