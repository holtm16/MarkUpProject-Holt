"""
Michael Holt
HTMLScorer.py
The below code implements a class to score a given input HTML file.
"""

# We begin by creating an empty dictionary to hold our scoring rules
scoreDict = {}
# Now we add all the appropriate relations, with tag names as keys and
# the associated score modifiers as values
scoreDict["div"] = 3
scoreDict["p"] = 1
scoreDict["h1"] = 3
scoreDict["h2"] = 2
scoreDict["html"] = 5
scoreDict["body"] = 5
scoreDict["header"] = 10
scoreDict["footer"] = 10
scoreDict["font"] = -1
scoreDict["center"] = -2
scoreDict["big"] = -2
scoreDict["strike"] = -1
scoreDict["tt"] = -2
scoreDict["frameset"] = -5
scoreDict["frame"] = -5

class HTMLScorer():
    
    # Our constructor initializes our object given a filename (like bob_2013_02_15.html)
    def __init__(self, fileName):
        self._fileName = fileName
        # Initialize the score to 0
        self._score = 0
        # Initialize the keyname to the first part of the file name (keyname_<otherStuff>.html)
        i = 0
        # We increment i until reaching the first underscore
        while fileName[i] != '_':
            i += 1
        self._keyName = fileName[0:i]
        self._listOfTagNames = []
        
        

    # scoreInput will parse through the object's file called fileName,
    # returning the score of the file using our scoring system
    def scoreInput(self):
        # Determine the actual file location within our directories
        actualFileLocation = "../data/" + self._fileName
        f = open(actualFileLocation, 'r')
        s = f.read()
        f.close()
        # Now we split the file into a list of lines
        listOfLines = s.split('\n')
        # Remove all empty lines and lowercase the line's characters
        # with the below list comprehension
        updatedListOfLines = [line.lower() for line in listOfLines if line != '']
        # Now we loop through each line within our list
        for line in updatedListOfLines:
            lenOfLine = len(line)
            for i in range(lenOfLine-1):
                # Check to see if we have the beginning of a tag
                if line[i] == '<' and line[i+1] != '/':
                    j = i+1
                    while line[j] != ' ' and line[j] != '>' and j < lenOfLine:
                        j += 1
                    # Now j should mark where the end of our tag name is, so
                    # we can add the tag name to our list
                    self._listOfTagNames.append(line[i+1:j])
        # Loop through all the found tag names and add the corresponding scores to our
        # score instance variable
        for tagName in self._listOfTagNames:
            self._score += scoreDict[tagName]
        print(self._keyName + "'s file has been scored")
        return self._score

    # getFilePrefix returns the prefix of the input file name
    def getFilePrefix(self):
        return self._keyName
            
