#!/usr/bin/env python

"""
New comment ! 
"""
from python_get_resolve import GetResolve
import json
import time
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--preset-name', dest='preset_name', type=str, help='DaVinci stills preset name')
parser.add_argument('--target-dir', dest='target_dir', type=str, help='Target directory for stills export')
parser.add_argument('--project-prefix', dest='project_prefix', type=str, help='Project prefix for stills export')
args = parser.parse_args()

#TARGET_DIR = "/Volumes/Macintosh HD/Users/theolopez/Desktop/STILLS/"
#PROJECT_PREFIX = "DMPTO"
#PRESET_NAME = "EXPORT_STILL_PNG"

PRESET_NAME = args.preset_name
PROJECT_PREFIX = args.project_prefix
TARGET_DIR = args.target_dir

def getMarkersOfTimeline(timeline, project, folder, rootFolder):
    markers = timeline.GetMarkers()
    #data = json.loads(str(markers))
    liste = list(markers.keys())
    directory = TARGET_DIR+"/"+str(rootFolder.GetName())+"/STILLS/"
    print(liste)
    project.SetCurrentTimeline(timeline)
    for frameNumber in liste:
        startFrame = timeline.GetStartFrame()
        project.LoadRenderPreset(PRESET_NAME)
        project.SetRenderSettings({"SelectAllFrames":False, "MarkIn":startFrame+frameNumber+1, "MarkOut":startFrame+frameNumber+1, "TargetDir":directory, "CustomName":PROJECT_PREFIX+"_"+rootFolder.GetName()+"_"})
        project.AddRenderJob()


def getTimelines(clip, project, folder, rootFolder):
    timelineCount = project.GetTimelineCount()
    inc = 1
    for i in range(timelineCount):
        timeline = project.GetTimelineByIndex(i+1)
        inc+=1
        name = timeline.GetName()
        if name == clip.GetName():
            print ('Sending ', timeline.GetName(), ' for marker analysis…')
            getMarkersOfTimeline(timeline, project, folder, rootFolder)




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


def AskDeleteAllRenderJob(project):
    res = input("Do you want to delete all render jobs ? [y/n] (default YES)")
    if(res == "" or res =="y" or res == "Y"):
        print("Deleting old render jobs…")
        time.sleep(2)
        project.DeleteAllRenderJobs() #delete all jobs
    elif(res == "n" or res =="N"):
        print("Old render jobs will be kept.")
    else:
        AskDeleteAllRenderJob(project)

# Get currently open project
resolve = GetResolve()
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()

AskDeleteAllRenderJob(project)
DisplayRootFolders(project)

