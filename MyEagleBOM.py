'''
Created on 19.01.2017

@author: Haz
'''
import csv
from _elementtree import parse
from collections import defaultdict
from operator import itemgetter
from audioop import reverse
from itertools import count

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
    bomByDesignator = defaultdict(list)
    
    def __init__(self, csvFile):
        self.csvFile = csvFile  
    
    def CreateBom(self):
#         for row in self.csvFile:
#             print row
        
        
        del self.csvFile[0]
        
        
#         self.bom.append([['C2'], 1, '100n 10V', 'C0603'])
# 
#         self.bom.append(self.GetItemFromCsvRow(self.csvFile[0]))
#         
#         self.bom.append([['C3'], 1, '10u 6V3', 'C1206'])
#         item = self.GetItemFromCsvRow(self.csvFile[5])
# #         print item
#         self.TryInsertItemIntoBom(item)

        for row in self.csvFile:
            item = self.GetItemFromCsvRow(row)
            self.TryInsertItemIntoBom(item)
            
        self.SortBom()
        
        
#         for item in self.bom:
#             print item
            
#         print self.GetItemFromCsvRow(self.csvFile[1])[0]
#         print self.IsThisItemInBom(self.GetItemFromCsvRow(self.csvFile[1]))

    
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
        item.append([csvRow[0]])
        item.append(1)
        item.append(csvRow[1])
        item.append(csvRow[3])
        
        return item
    
    def InsertItem(self, item):
        self.bom.append(item)
    
    def IsThisItemInBom(self, item):
        itemInList = False
        for bomItem in self.bom:
            for designator in bomItem[0]:
                if (designator == item[0][0]):
                    itemInList = True
        
        return itemInList
    
    def IsItemHasSamePackageAndValue(self, item1, item2):
        if (item1[2] == item2[2]) and (item1[3] == item2[3]):
            return True
        else:
            return False
        
    def SortBom(self):
        self.SortBomByDesignatorType()
#         self.SortItemsByValue(bom.bomByDesignator['C'])
        
#         print self.bomByDesignator['C']
#         self.SortItemsByValue(bom.bomByDesignator['R'])

#         for item in self.bomByDesignator['R']:
#             print item
            
        
        self.SortItemsByValue(bom.bomByDesignator['R'])
        self.SortItemsByValue(bom.bomByDesignator['C'])
        self.SortItemsByValue(bom.bomByDesignator['L'])
        for item in bom.bomByDesignator['R']:
            print item
        
    
    
    def SortBomByDesignatorType(self):        
        for item in self.bom:
            self.bomByDesignator[self.GetDesignatorType(item[0][0])].append(item)        
    
    
    def SortItemsByValue(self, items):
        sortableDic = defaultdict(list)
        nonSortableList = []
        tempList = list()
        for item in items:
            if self.IsItemAbleToSort(item):                
                sortableDic[self.GetItemValueFromDescription(item)].append(item)
            else:
                nonSortableList.append(item)
        
        dicList = sorted(sortableDic.keys())
        for item in dicList:       
            for lowItem in sortableDic[item]:
                tempList.append(lowItem)
        
        for item in nonSortableList:
            tempList.append(item)

        for i, item in enumerate(items):
            items[i] = tempList[i]        
            
            
    def IsItemAbleToSort(self, item):
        stringValue = item[2].partition(' ')[0]
        if stringValue and stringValue[0].isdigit():
            return True
        else:
            return False
    
    
    def GetItemValueFromDescription(self, item):
        description = item[2]
        value = description.partition(' ')[0]
        
        return ConvertUnits.ToNumericValue(value)
    
    
    def MergeItemWithItemInBom(self, itemInBom, itemToMerge):
        itemInBom[0].append(itemToMerge[0][0])
        self.IncrementItemNumberInBomItem(itemInBom)
        
    def IncrementItemNumberInBomItem(self, item):
        item[1] += 1
    
    def TryInsertItemIntoBom(self, item):
        if (self.IsThisItemInBom(item) == False):
            if self.TryMergeItemWithItemInBom(item):
                return True
            else:
                self.InsertItem(item)

            return True
        else:
            return False


    def TryMergeItemWithItemInBom(self, item):
        for itemInBom in self.bom:                
            if self.IsItemHasSamePackageAndValue(itemInBom, item):
                self.MergeItemWithItemInBom(itemInBom, item)                    
                return True
    
    
    def GetDesignatorType(self, designator):
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
        
        
class ConvertUnits:
    metricPrefixValues = {
            'G' : 1E9,
            'M' : 1E6,
            'k' : 1E3,
            'm' : 1E-3,
            'u' : 1E-6,
            'n' : 1E-9,
            'p' : 1E-12,
            'R' : 1,
            'F' : 1,
            'H' : 1,
        }
    
    @staticmethod
    def ToNumericValue(stringValue):
        metricPrefix = 0
        fractionString = ""
        
        for i, char in enumerate(stringValue):
            if ConvertUnits.IsMetricPrefix(char):
                metricPrefix = ConvertUnits.GetMetricPrefixValue(char)
                fractionString += '.' 
            else:
                fractionString += stringValue[i]
        
        if not metricPrefix:
            return stringValue
        else:            
            return float(fractionString) * metricPrefix
    
    @staticmethod
    def IsMetricPrefix(char):
        if char.isdigit() == False:
            return True
        else:
            return False
        
    @staticmethod
    def GetMetricPrefixValue(char):
        return ConvertUnits.metricPrefixValues.get(char, 'None')    
    
            

print ConvertUnits.ToNumericValue("100n") 
        
        
        
        

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
bom.CreateBom()
# bom.SortBomByDesignatorType()
# bom.SortItemsByValue(bom.bomByDesignator['C'])