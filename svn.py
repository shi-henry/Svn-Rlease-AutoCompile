#!/usr/bin/env python
#-*-coding:utf-8-*-
import subprocess, os, os.path
import re
import time
import shutil

# RunTimelog = "/home/runTimeLog.txt"
# fRunTimelog = open(RunTimelog."w+")

basePath = "/home"
repoPath = basePath + r"/cleanTiRepo"
fileLastVision = repoPath + r"/lastVision.txt"
logDir = repoPath + r"/daily-release-"
workPath = repoPath + r"/VISION_SDK_02_09_01_00"
svnUpdateLog = repoPath + r"/svnUpdate.txt"
srcBin = workPath + r"/vision_sdk/binaries/vision_sdk/bin/tda2xx-evm/sbl_boot/AppImage"

stringPattern = r"^版本 (\d+)。$"
pattern = re.compile(stringPattern)

with open(fileLastVision, "r") as f:
    oldVer = f.readline().strip()
    if not oldVer:
        oldVer = "47"
    # print oldVer

os.chdir(workPath)
print os.getcwd()

with open(svnUpdateLog, "w+") as f:
    p = subprocess.Popen(["svn","cleanup","--force-interactive","--username","guangming.shi","--password","123456"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    p.wait()
    p = subprocess.Popen(["svn","update","--force-interactive","--username","guangming.shi","--password","123456"],stdin=subprocess.PIPE,stdout=f,stderr=subprocess.STDOUT)
    p.wait()

with open(svnUpdateLog, "r") as file1:
    for line in file1:
        match = pattern.match(line)
        if match:
            newVer = match.group(1)
            logDir += newVer
            # print newVer
            with open(fileLastVision, "w+") as f:
                f.write(newVer + "\n")

if os.path.isdir(logDir):
    logDir += "-"
    logDir += time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
os.mkdir(logDir)
# print logDir

shutil.move(svnUpdateLog, logDir)

updateLogFile = logDir + "/updateLog.txt"
compileLogFile = logDir + "/compileLog.txt"

with open(updateLogFile,"w+") as f:
    if oldVer == newVer:
        f.write("There is no update!\n")
    else:
        duration = oldVer + ":" + newVer
        # print duration
        p = subprocess.Popen(["svn","cleanup","--force-interactive","--username","guangming.shi","--password","123456"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        p.wait()
        p = subprocess.Popen(["svn","log","-r",duration,"--force-interactive","--username","guangming.shi","--password","123456"],stdin=subprocess.PIPE,stdout=f,stderr=subprocess.STDOUT)
        p.wait()


os.chdir(workPath + "/vision_sdk")
print os.getcwd()
with open(compileLogFile, "w+") as f:
    p = subprocess.Popen(["/usr/bin/make","all"],stdin=subprocess.PIPE,stdout=f,stderr=subprocess.STDOUT,shell=True)
    p.wait()
    f.write(os.getcwd())
    distBin = logDir
    shutil.copy2(srcBin, distBin)
