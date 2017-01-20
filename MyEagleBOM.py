'''
Created on 19.01.2017

@author: Haz
'''
import csv
from _elementtree import parse

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
        
        
class Bom:
#     In CSV
#     C2    1u 25V    C-EUC1206    C1206    CAPACITOR, European symbol    
#     In BOM should be
#     C2    1    1u 25V    C1206
    
    
    
    bom = []
    
    def __init__(self, csvFile):
        self.csvFile = csvFile  
    
    def ParseCsv(self):
#         for row in self.csvFile:
#             print row
        del self.csvFile[0]

        print self.GetItemFromCsvRow(self.csvFile[0])
    
    def GetDesignator(self, rowNum):
        return self.bom[rowNum][0] 

    def GetQuantity(self, rowNum):
        return self.bom[rowNum][1]
    
    def GetValue(self, rowNum):
        return self.bom[rowNum][2]
    
    def GetPavkage(self, rowNum):
        return self.bom[rowNum][3]
    
    def GetItemFromCsvRow(self, csvRow):
        item = []
        item.append(csvRow[0])
        item.append(1)
        item.append(csvRow[1])
        item.append(csvRow[3])
        
        return item
    
    def InsertItem(self, item):
        pass
    
    def IsThisItemInBom(self, item):
        notInList = True
        for bomItem in self.bom:
            if (bomItem[0] == item[0]):
                notInList = False
        pass
    
    def IsItemHasSamePackageAndValue(self, item):
        pass
    
    def SortBomByDesignatorType(self):
        pass
    
    def SortItemsByValue(self):
        pass
    
    def TryInsertItemIntoBom(self):
        pass
    

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
        
    def MergeRows(self, row1, row2):
        mergedRow = []
        for cell in row1:
            mergedRow.append(cell)
        
        mergedCell = []
        mergedCell.append(mergedRow[0])
        mergedCell.append(row2[0])
        mergedRow[0] = mergedCell
        
        return mergedRow
    
    def Test(self):
        print self.MergeRows(self.csvFile[1], self.csvFile[2])
        
    def CreateBOM(self):
        uniqueDesignatorTypeList = self.GetUniqueDesignetorTypeList()
        bom = []
        isFirstRow = True
        
        for designator in uniqueDesignatorTypeList:
            for row in self.csvFile:
                if (isFirstRow != True):                    
                    if (designator == self.GetDesignatorType(row[0]) ):
                        
                        pass
                else:
                    pass
                
                isFirstRow = False
        
        
parseEagleCSV = ParseEagleCSV(OpenCsvFile(filename))

bom = Bom(OpenCsvFile(filename))
bom.ParseCsv()


# class MyFirstLvlList:
#     item = "abc"
#     
# myFirstLvlList = MyFirstLvlList
#     
# myList = []
# myList.append(myFirstLvlList)
# 
# print myList[0].item
# 
# 
# OpenCsvFile(filename)
# print parseEagleCSV.GetDesignatorType('IC344')
# 
# parseEagleCSV.GetElementRowsGroupedByType()
# 
# parseEagleCSV.Test()
