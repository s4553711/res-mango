#!/usr/bin/python
import time
import json
import os

class Deploy(object):
    def __init__(self):
        self.init()

    def setDest(self, f):
        if f != "":
            self.toFolder = f
        else:
            print "empty toFolder"
            exit

    def logger(self, message):
        print("["+time.strftime('%Y-%m-%d %H:%M%p %Z')+"] " + message)

    def init(self):
        self.logger("start init")
        with open("app.json") as json_file:
            self.setting = json.load(json_file)

    def fromTo(self, fromPath, fromF, toPath, toF):
        if os.path.islink(fromF):
            os.symlink(os.readlink(fromF), os.path.join(toPath, toF))
        else:
            os.symlink(os.path.join(fromPath, fromF), os.path.join(toPath, toF))

    def processEntry(self, folder, layout, ob):
        dest = self.toFolder + os.sep + layout[1:]
        if not os.path.exists(dest):
            os.makedirs(dest)

        if folder != "":
            for f in os.listdir(folder):
                self.fromTo(folder, f, dest, f)
                #if os.path.islink(f):
                #    os.symlink(os.readlink(f), os.path.join(dest, f))
                #else:
                #    os.symlink(os.path.join(folder, f), os.path.join(dest, f))

        if 'extra' in ob:
            for ele in ob['extra']:
                if type(ele) is dict:
                    for k,v in ele.iteritems():
                        #print "link with alternative"
                        sourceFolder = self.setting['resources'][k.split("/")[0]]['source']
                        fromF = k.split("/")[1]
                        self.fromTo(sourceFolder, fromF, dest, v)
                        #print "end"
                else:
                    #print "> link directly"
                    sourceFolder = self.setting['resources'][ele.split("/")[0]]['source']
                    fromF = ele.split("/")[1]
                    self.fromTo(sourceFolder, fromF, dest, fromF)

    def iter(self):
        for step in self.setting['resources']:
            self.logger("process " + step)
            if 'layout' in self.setting['resources'][step]:
                self.processEntry(self.setting['resources'][step]['source'], self.setting['resources'][step]['layout'], self.setting['resources'][step])
            else:
                self.logger("ignore "+step)
            
