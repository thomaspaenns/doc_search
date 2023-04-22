#USED FOR 5 A & B
import csv
import pathlib
from pathlib import Path
from turtle import rt
import math

#FROM HW 3
#measuresFiles = ["msmuckerAND-measures.csv", "student1-measures.csv", 
#    "student2-measures.csv", "student3-measures.csv", "student4-measures.csv", 
#    "student5-measures.csv", "student6-measures.csv", "student7-measures.csv", 
#    "student8-measures.csv", "student9-measures.csv", "student10-measures.csv", 
#    "student11-measures.csv", "student12-measures.csv", "student13-measures.csv", 
#    "student14-measures.csv"]

measuresFiles = ["hw4-bm25-baseline-tenns-measures.csv", "hw4-bm25-stem-tenns-measures.csv"]

#measuresFiles = ["hw5-baseline-tenns-measures.csv", "hw5-BERT-tenns-measures.csv"]

summaryPath = Path("data-summary.csv")
with open(summaryPath, "w", newline='') as output:
    writer = csv.writer(output)
    writer.writerow(["Run Name", "Mean Average Precision", "Mean P@10", "Mean NDCG@10", "Mean NDCG@1000", "Mean TBG"])
    for fileName in measuresFiles:
        pathName = "measures-files/" + fileName
        runName = fileName.replace("-measures.csv", "")
        if fileName in ["student6-measures.csv", "student10-measures.csv","student12-measures.csv"]:
            writer.writerow([runName, "bad format", "bad format", "bad format", "bad format", "bad format"])
        else:
            filePath = Path(pathName)
            with open(filePath, "r") as measures:
                reader = csv.reader(measures)
                totalAP = 0.0
                totalP10 = 0.0
                totalnDCG10 = 0.0
                totalnDCG1000 = 0.0
                totalTBG = 0.0
                count = 0.0
                outRow = [runName]
                for row in reader:
                    totalAP = totalAP + float(row[1])
                    totalP10 = totalP10 + float(row[2])
                    totalnDCG10 = totalnDCG10 + float(row[3])
                    totalnDCG1000 = totalnDCG1000 + float(row[4])
                    totalTBG = totalTBG + float(row[5])
                    count = count + 1
                outRow.append(round(totalAP/count, 3))
                outRow.append(round(totalP10/count, 3))
                outRow.append(round(totalnDCG10/count, 3))
                outRow.append(round(totalnDCG1000/count, 3))
                outRow.append(round(totalTBG/count, 3))
                writer.writerow(outRow)



