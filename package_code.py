## The objective is to retrive packages from repository and install on destination server
#


from  __future__  import  print_function
import os, platform, sys, subprocess, time




## Package Deployment for Java/Oracle

class OracleJavaPackageDeploy:
     def __init__(self, Username, DestServer, Package):
                  self.Username = Username
                  self.DestServer = DestServer
                  self.Package   = Package

     def  RetrievePackage(self):
                  COMMAND = "cd /UNXPRDFS/products;  ls -ld " + self.Package + "* | awk '{print $9}'"
                  sshcommand = subprocess.Popen(["ssh","-o","StrictHostKeyChecking=no","-l",self.Username,  "unxprdfs11", COMMAND],
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
                  time.sleep(2)
                  return(sshcommand)

     def DeployPackage(self):
                  time.sleep(2)
                  COMMAND = "cd /usr/local; sudo ls -ld " + self.Package
                  p = subprocess.Popen(["ssh","-o","StrictHostKeyChecking=no","-l",self.Username,  self.DestServer, COMMAND],
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
                  exit_code = p.wait()
                  if exit_code == 0:
                        return("Package is already installed")
                  else:
                        COMMAND = "cd /usr/local; sudo ln -s mount/" + self.Package
                        sshcommand = subprocess.Popen(["ssh","-o","StrictHostKeyChecking=no","-l",self.Username,  self.DestServer, COMMAND])
                        exit_code1 = sshcommand.wait()
                        if exit_code1 == 0:
                             return("Success")
                        else:
                             return("Failed")


     def QueryPackage(self):
                  COMMAND = "cd /usr/local; sudo ls -ld " + self.Package
                  p = subprocess.Popen(["ssh","-o","StrictHostKeyChecking=no","-l",self.Username,  self.DestServer, COMMAND],
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
                  exit_code = p.wait()
                  if exit_code == 0:
                        return("Package Found inside /usr/local" )
                  else:
                        return("No such package" )


## Package deployement for other application
class NormalPackageDeploy:
     def  __init__(self, Username, DestServer, Package):
                  self.Username = Username
                  self.DestServer = DestServer
                  self.Package   = Package

     def  RetrievePackage(self):
                  COMMAND = "sudo yum list " + self.Package + " | grep -i " + self.Package
                  sshcommand = subprocess.Popen(["ssh","-o","StrictHostKeyChecking=no","-l",self.Username,  self.DestServer, COMMAND],
                         shell=False,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').strip()
                  return(sshcommand)

     def  DeployPackage(self):
                  COMMAND = "sudo rpm -qa | grep -i " + self.Package
                  p = subprocess.Popen(["ssh","-o","StrictHostKeyChecking=no","-l",self.Username, self.DestServer, COMMAND],
                         shell=False,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
                  exit_code = p.wait()
                  if exit_code == 0:
                         return("Package is already installed")
                  else:
                         COMMAND = "sudo yum install -y " + self.Package
                         sshcommand = subprocess.Popen(["ssh","-o","StrictHostKeyChecking=no","-l",self.Username,  self.DestServer, COMMAND],
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
                         exit_code1 = sshcommand.wait()
                         if exit_code1 == 0:
                                 return("Success")
                         else:
                                 return("Failed")

     def QueryPackage(self):
                   COMMAND = "rpm -qa | grep -i " + self.Package
                   sshcommand = subprocess.Popen(["ssh","-o","StrictHostKeyChecking=no","-l",self.Username, self.DestServer, COMMAND],
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
                   return(sshcommand)


