from struct import *

userDataStruct = 'qhh'
userDataStructNames = ('clientTime', 'xv', 'yv') 

def packUserData(data):
    return pack(userDataStruct, *data)
    
def unpackUserData(binaryUserData):
    data = unpack(userDataStruct, binaryUserData)

    dataDict = {}
    for i in range(len(data)):
        dataDict[userDataStructNames[i]] = data[i]

    return dataDict
