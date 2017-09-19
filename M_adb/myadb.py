import os
import  subprocess
import re

Meta = "cat firmware/verinfo/ver_info.txt"

class madb(object):

    __adbpath=None
    __output=None
    __error=None
    __devices=None
    __cmd=None

    def __init__(self,adbpath="adb"):
        self.__adbpath=adbpath

    def _clear_(self):
        self.__output = None
        self.__error  = None

    def _build_cmd_(self,cmd):
        #print("you are in build command {%s}" % cmd)
        cmd_list=[]
        #print(type(cmd))
        cmd_list.insert(0,self.__adbpath)
        cmd_list.insert(1,cmd)
        print("build cmd",cmd_list)
        #print("generating build command and returning from __build_cmd_() function  "," ".join(cmd_list))
        return " ".join(cmd_list)

    def shell_cmd(self, string):

        command = 'adb shell cat firmware/verinfo/ver_info.txt'
        p = subprocess.Popen(command, shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = p.communicate('ls')
        #print stdout
        return stdout

    def run_cmd(self,cmd):
        #print("start_run_cmd {%s}" % cmd)
        self._clear_()
        try:
            self.__cmd = self._build_cmd_(cmd)
            # print("[cmd]",self.__cmd)
            command = subprocess.check_output(self.__cmd,shell=True)
            #command = subprocess.Popen(self.__cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print ("command",command)
            return  command
        except OSError, e:
           self.__error = str(e)
           self.__devices=None
           print (self.__error)
           print ("Failed to execute",self.__cmd)

    def device_filter(self,cmd):
        # print ("device_filter",cmd) #Output :- ('device_filter', 'List of devices attached \n7dab6ce3\tdevice\n\n')
        # working
        dev = cmd.split(" ")[4]
        dev = dev.split("\t")[0].strip("\n")
        #print ("dev",dev)

        try:
            if dev != "" and  dev != "????????????":  # Need to filter more
             #print ("devide filter",dev)
             self.__devices= dev
        except :
            print ("please keep dvice in MTP mode ")

    def adb_devices(self):
        #print("adb devices")

        try:
            self.__devices=None
            cmd=self.run_cmd("devices")
            #print cmd
            self.device_filter(cmd)
            #print("cc",self.__devices)
            if self.__devices != None:
                print ("device_detected ",self.__devices)
            return True
        except :
            self.__devices-=None
            print (self.__devices)

    def adb_root(self):
        ch_adbd= "adbd"
        print("root")
        #self.__devices = None
        self.adb_devices()
        if self.__devices != None:
            #print ("device tetected ",self.__devices)
            data = self.run_cmd("root")
            #print("root fun",data)
            if ch_adbd  in data:
                print ("Devie is rooted")
                return True
            else:
                print ("Devuice is not rooted please check")
        '''
        except OSError,e:
            self.__error = str(e)
            # self.__error = str(e)
            print ("adb root failed",self.__error)
            self.__devices=None '''


    def adb_shell(self):
        print ("adb_shell function")
        command = 'adb shell cat firmware/verinfo/ver_info.txt'
        try:
            adb_return =self.adb_devices()
            if adb_return ==True and self.__devices != None:
                print ("Device detected successfully")
                root_return=self.adb_root()
                if root_return == True:
                       print ("adb rooted successfully")
                       #data = self.shell_cmd("cmd")
                       #print("shell",data)
                       mydata= self.shell_cmd(Meta)
                       print("-->",mydata)
                       print type(mydata)
                       #for meta in mydata:
                       #     print meta
        except:
            print ("failed in adb shell")

            """print ("adb shel fun",self.__devices)
             if(self.__devices) != None:
                print ("device detected",self.__devices)
                data = self.run_cmd("shell")
                   #self.run_cmd(cmd)
                print ("adb shell executed successfullay")
            else:
                print ("plese check devicess")"""

    def find_meta(self):
        print ("find_meta ")
        if (self.__devices) != None:
            print ("device detected ")
            data = self.run_cmd("shell")
            # self.run_cmd(cmd)
            print ("adb shell executed successfullay")
        else:
            print ("failed to detect devices please connect HW")
