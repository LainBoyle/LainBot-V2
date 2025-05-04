from dataclasses import dataclass
import re

@dataclass
class Session:
    is_active: bool = False 
    path = ""
    location = ""
    user = None
    id = 0
    awaitingInput = False
    info = None
    options = []
    userVars = []
    
    def __init__(self, user, path, filename):
        self.user = user
        self.path = re.sub(r'\W+', '', str(path)) 
        self.info = open(filename)
        self.getVariables()
    
    def setID(self, id):
        self.id = id
        
    def getID(self):
        return self.id
    
    def addPath(self, newPath):
        self.path = self.path + "/" + newPath 
        
    def getPath(self):
        return self.path
    
    def getInput(self):
        return
    
    def checkState(self):
        return True
    
    def setUser(self, user):
        self.user = user
        
    def getUser(self):
        return self.user
    
    def close(self):
        self.setVariables()
        with open("tracking.txt", "a") as tracking:
            trackPath = re.sub(r'\W+', '', self.path)
            tracking.write(str(self.user) + "," + trackPath + "\n")
        tracking.close()
        return
    
    def investigate(self):
            print("Investigating " + self.path)
            for line in self.info:
                if line.strip() == self.path:
                    output = self.info.readline()
                    if "!SET" in output:
                        self.handleSET(output)
                        output = self.info.readline()
                        
                    nextLine = self.info.readline()
                    if not "@" in nextLine and nextLine is not None:
                        output = output + self.handleOptions(nextLine)  
                    return output.replace("//", "\n\n")
                
    
    def handleOptions(self, line):
        unfilteredOptions = line.rstrip().split(",")
        output = self.promptInput()
        i=1
        for option in unfilteredOptions:
            if option[-1] == '}':
                optionComponents = option[:-1].split("{")
                print(optionComponents)
                param = optionComponents[1]
                thing = optionComponents[0]
                print("Thing: " + thing)
                if self.checkIfPass(param):
                    output = output + '\n' + str(i) + ") " + str(thing)
                    if thing not in self.options:
                        self.options.append(thing)
                    i = i + 1 
            else:
                output = output + '\n' + str(i) + ") " + str(option)
                if option not in self.options:
                    self.options.append(option)
                i = i + 1 
        return output 
    
    def checkIfPass(self, param):
        paramList = param.split(",")
        for i in paramList:
            if i not in self.userVars:
                return False
        return True
    
    def handleSET(self, line):
        outList = line.replace("!SET ", "").split(",")
        for variable in outList:
            found = False   
            for userVar in self.userVars:
                thisVarName = userVar.split("=")
                print("thisVarName: " + thisVarName[0])
                print("userVar: " + userVar)
                print("variable: " + variable)
                
                if thisVarName[0] in variable:
                    self.userVars[self.userVars.index(userVar)] = variable.strip()
                    found = True
            if found == False:
                self.userVars.append(variable.strip())
                    
    
    def getVariables(self):
        
        try:
            file = open(str(self.user) + ".txt", "r+")
            for line in file.readlines():
                if line.strip() not in self.userVars:  
                    self.userVars.append(line.strip())
        except:
            file = open(str(self.user) + ".txt", "x")
       
        file.close()

    
    def setVariables(self):
        with open(str(self.user) + ".txt", "w") as file:
            for var in self.userVars:
                file.write(var.strip())
        file.close()
            
                    
    def promptInput(self):
        self.awaitingInput = True
        return "\nWhat do you do?"
    
    
    
    def isAwaitingInput(self):
        return self.awaitingInput
    