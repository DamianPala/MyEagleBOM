'''
Created on 19.01.2017

@author: Haz
'''
import csv

filename = 'Fingerprint_Sensor_Button_HW'

def OpenCsvFile(filename):
    with open(filename + '.csv', 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter = ';')
        reader = list(reader)
    return reader

class ElementRowsWithSamePackage:
    elementRowWithSamePackage = []
    def __del__(self):
        print "deling", self

class ParseEagleCSV:
    elementRowsGroupedByTypeList = []
    elementRowsGroupedByTypeList2 = []
    
    def __init__(self, csvFile):
        self.csvFile = csvFile            
        
    def GetDesignatorType(self, designator):
        designatorType = 'adas'
        char = ''
        for char in designator:
            if(char.isdigit()):
                designatorType = designator.partition(char)
                return designatorType[0]
    
    def GetUniqueDesignetorTypeList(self):
        uniqueDesigantorTypeList = []
        for row in self.csvFile:
            uniqueDesigantorTypeList.append(self.GetDesignatorType(row[0]))
            uniqueDesigantorTypeList = list(set(uniqueDesigantorTypeList))
        return uniqueDesigantorTypeList
    
    def GetElementRowsGroupedByType(self):
        uniqueDesignatorTypeList = self.GetUniqueDesignetorTypeList()
        
        for designatorType in uniqueDesignatorTypeList:
            elementsTypeGroup = []
            for row in self.csvFile:
                if (self.GetDesignatorType(row[0]) == designatorType):
                    elementsTypeGroup.append(row)
            
            
            
            
            
            
            
#             self.elementRowsGroupedByTypeList.append(elementsTypeGroup)
            
#             print self.GetUniquePackageList(elementsTypeGroup)
#             elementRowsWithSamePackage = ElementRowsWithSamePackage
#             elementRowsWithSamePackage.elementRowWithSamePackage.append(self.GetElementRowsWithSamePackage(elementsTypeGroup))
            self.elementRowsGroupedByTypeList.append(self.GetElementRowsWithSamePackage(elementsTypeGroup))
#             
#             
#             for item in elementRowsWithSamePackage.elementRowWithSamePackage:
#                 print item
#             print "end1"
#             print self.GetElementRowsWithSamePackage(elementsTypeGroup)
#             print "end2"
#             
#             del elementRowsWithSamePackage
#             
#             
#         for item in self.elementRowsGroupedByTypeList:
#             print item.elementRowWithSamePackage
#             self.elementRowsGroupedByTypeList2.append(object)
        
        for item in self.elementRowsGroupedByTypeList:
              
            print item
    
    def GetUniquePackageList(self, rowList):
        uniquePackageList = []
        for row in rowList:
            uniquePackageList.append(row[3])
        
        uniquePackageList = list(set(uniquePackageList))
        
        return uniquePackageList
    
    def GetElementRowsWithSamePackage(self, elementsGroup):
        elementRowsWithSamePackageList = []
        packageList = self.GetUniquePackageList(elementsGroup)     
        
        for package in packageList:
            elementRowsWithSamePackage = []            
            for element in elementsGroup:
                if (element[3] == package):
                    elementRowsWithSamePackage.append(element)
            elementRowsWithSamePackageList.append(elementRowsWithSamePackage)
        
        return elementRowsWithSamePackageList
        
        
        
parseEagleCSV = ParseEagleCSV(OpenCsvFile(filename))



class MyFirstLvlList:
    item = "abc"
    
myFirstLvlList = MyFirstLvlList
    
myList = []
myList.append(myFirstLvlList)

print myList[0].item


OpenCsvFile(filename)
print parseEagleCSV.GetDesignatorType('IC344')

parseEagleCSV.GetElementRowsGroupedByType()
