#!/usr/bin/env python
import glob
import os
import subprocess
import time

TracesPath = r"C:\Program Files\Simenv 4.3.9.8_PMI\Workspace\Simenv\ScenariosTrace"
LogsPath = r"C:\Program Files\Simenv 4.3.9.8_PMI\Mei\Mei_1\ARCHIVES"
MESDLogsPath = r"C:\Program Files\Simenv 4.3.9.8_PMI\Mei\Mei_2\ARCHIVES"
loc_7z = r"C:\Program Files\7-Zip\7z.exe"

Header = '''Log7Zip.py v0.2 (30/11/2018)
7-Zip in max compression MEI and MESD log files found in %s when Alanceur is used.
Author: Tony Paulino'''

print 78 * '='
print Header % LogsPath
print 78 * '='


while True:
    TracesDirectory = [os.path.basename(path) for path in glob.glob(TracesPath + "\*.trc")]
    print TracesDirectory
    for script in TracesDirectory:
        os.chdir(LogsPath)
        MEILogNames = [path for path in glob.glob(script.replace(".trc","*.txt"))]
        print 78 * '='
        print MEILogNames
        for LogFile in MEILogNames:
            try:
                command = [
                    "%s" % loc_7z,
                    "a",
                    "%s" % LogFile.replace(".txt",".7z"),
                    "%s" % LogFile,
                    "-mx9"
                ]
                subprocess.call(command, shell=True)
                os.remove(LogFile)
            except:
                print("error in file:",LogFile)
                
        os.chdir(MESDLogsPath)
        MESDLogNames = [path for path in glob.glob(script.replace(".trc","*.txt"))]
        print 78 * '='
        print MESDLogNames
        for LogFile in MESDLogNames:
            try:
                command = [
                    "%s" % loc_7z,
                    "a",
                    "%s" % "MESD_" + LogFile.replace(".txt",".7z"),
                    "%s" % LogFile,
                    "-mx9"
                ]
                subprocess.call(command, shell=True)
                os.remove(LogFile)
            except:
                print("error in file:",LogFile)
    time.sleep(600)   
