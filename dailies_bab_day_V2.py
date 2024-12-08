#!/usr/bin/env python

"""
Example DaVinci Resolve script:
Display project information: timeline, clips within timelines and media pool structure.
Example usage: 5_get_project_information.py
"""

from python_get_resolve import GetResolve
import json

TARGET_DIR = "/Volumes/SUBMERGEE_RAID/EXPORTS/"
# def DisplayTimelineTrack( timeline, trackType, displayShift ):
#     trackCount = timeline.GetTrackCount(trackType)
#     for index in range (1, int(trackCount) + 1):
#         print(displayShift + "- " + trackType + " " + str(index))
#         clips = timeline.GetItemListInTrack(trackType, index)
#         for clip in clips:
#             print(displayShift + "    " + clip.GetName())
#     return

# def DisplayTimelineInfo( timeline, displayShift ):
#     print(displayShift + "- " + timeline.GetName())
#     displayShift = "  " + displayShift
#     DisplayTimelineTrack(timeline , "video", displayShift)
#     DisplayTimelineTrack(timeline , "audio", displayShift)
#     DisplayTimelineTrack(timeline , "subtitle", displayShift)
#     return

# def DisplayTimelinesInfo( project ):
#     print("- Timelines")
#     timelineCount = project.GetTimelineCount()

#     for index in range (0, int(timelineCount)):
#         DisplayTimelineInfo(project.GetTimelineByIndex(index + 1), "  ")
#     return


def getCirclesOfTimeline(timeline, project, timelineCreated):
    #pass each clip 1 by one and copy them to a timeline
    project.SetCurrentTimeline(timeline)
    clips = timeline.GetItemListInTrack("Video", 1)
    for clip in clips:
        print("clipPpP"+str(clip))
        circle = clip.GetClipProperty("Shot")
        if circle == "1":
            timelineCreated.AppendToTimeline(clip)



def getTimelines(clip, project, folder):
    mediaPool = project.GetMediaPool()
    timelineCreated = mediaPool.CreateEmptyTimeline(folder.GetName()+"_dailies")  #create an empty timeline with folder name
    timelineCount = project.GetTimelineCount()
    inc = 1
    for i in range(timelineCount):
        timeline = project.GetTimelineByIndex(i+1)
        inc+=1
        name = timeline.GetName()
        if name == clip.GetName():
            print ('Sending ', timeline.GetName(), ' for bab creation…')
            getCirclesOfTimeline(timeline, project, timelineCreated)




def DisplayTimelinesInfo( folder, displayShift, project ):
    print(displayShift + "- " + folder.GetName())
    clips = folder.GetClipList()
    for clip in clips:
        #print(displayShift + "  " + clip.GetClipProperty("File Name"))
        if clip.GetClipProperty()["Video Codec"] == "":
            print(displayShift, "TL :", clip.GetClipProperty("File Name"))
            getTimelines(clip, project, folder)

    displayShift = "  " + displayShift

    folders = folder.GetSubFolderList()
    for folder in folders:
        DisplayTimelinesInfo(folder, displayShift, project)
    return

# def DisplayMediaPoolInfo( project ):
#     mediaPool = project.GetMediaPool()
#     print("- Media pool")
#     DisplayFolderInfo(mediaPool.GetRootFolder(), "  ")
#     return

def getTimelinesOfFolder(folder, displayShift, project):
    clips = folder.GetClipList()
    print(folder.GetName())
    DisplayTimelinesInfo(folder, " ", project)


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
    getTimelinesOfFolder(foldersList[int(folderChoice)-1], "", project)
    return


# def DisplayProjectInfo( project ):
#     print("-----------")
#     print("Project '" + project.GetName() +"':")
#     print("  Framerate " + str(project.GetSetting("timelineFrameRate")))
#     print("  Resolution " + project.GetSetting("timelineResolutionWidth") + "x" + project.GetSetting("timelineResolutionHeight"))

#     DisplayTimelinesInfo(project)
#     print("")
#     DisplayMediaPoolInfo(project)
#     return

# Get currently open project
resolve = GetResolve()
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()

DisplayRootFolders(project)
#project.CreateEmptyTimeline("day001_dailies")  #create an empty timeline with folder name
