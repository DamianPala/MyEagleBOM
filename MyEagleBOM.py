'''
Created on 19.01.2017

@author: Haz
'''
import csv
from collections import defaultdict

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
        "Delete header row"
        del self.csvFile[0]

        for row in self.csvFile:
            item = self.GetItemFromCsvRow(row)
            self.TryInsertItemIntoBom(item)
            
        self.SortBom()
        
        for itemBom in self.bomByDesignator:
            for item in self.bomByDesignator[itemBom]:
                print item

    
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
        
        self.SortItemsByValue(self.bomByDesignator['R'])
        self.SortItemsByValue(self.bomByDesignator['C'])
        self.SortItemsByValue(self.bomByDesignator['L'])       
    
    
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
                if not metricPrefix:
                    metricPrefix = ConvertUnits.GetMetricPrefixValue(char)
                    fractionString += '.' 
            else:
                if char.isdigit():
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


  
bom = Bom(OpenCsvFile(filename))
bom.CreateBom()