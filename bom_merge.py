'''
@brief 		Script to mergeing BOM to one file.
		
@author	 Damian Pala
@date	   19.01.2017
'''

import sys
import os
from MyEagleBOM import Bom, ExportBom, MergeCsvFilesToOneObjectNoRowMerge, OpenCsvFile, InputFileType, show_exception_and_exit

def create_new_bom_filename(input_files_list):
	new_file_name = ""
	for item in input_files_list:
		new_file_name += os.path.splitext(os.path.basename(item))[0] + "_"
		
	new_file_name += "merged_bom.csv"
	
	return new_file_name

if __name__ == "__main__":
	sys.excepthook = show_exception_and_exit
	fileName = sys.argv[1:]
	scritDirectory = os.path.dirname(sys.argv[0])

#	 fileName.append("bom1.csv")
#	 fileName.append("bom2.csv")

	if len(fileName) == 1:
		csvFile = OpenCsvFile(fileName[0])
		bom = Bom(csvFile)
		bom.CreateBom(InputFileType.BOM_FILE)
		exportBom = ExportBom(bom)
		exportBom.WriteCsv(create_new_bom_filename(fileName))
	elif len(fileName) > 1:
		csvFile = MergeCsvFilesToOneObjectNoRowMerge(fileName)
		bom = Bom(csvFile)
		bom.CreateBom(InputFileType.BOM_FILE)
		exportBom = ExportBom(bom)
		exportBom.WriteCsv(create_new_bom_filename(fileName))
	else:
		"""Do nothing"""