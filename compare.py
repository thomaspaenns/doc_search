#USED FOR 5C & D
import sys
import os
import pathlib
from pathlib import Path
import math
import csv
import pandas as pd
import numpy as np
import scipy.stats as stats

if not len(sys.argv) > 3: #too few arguments
    sys.exit("enter the names of the two measures files you are comparing and the measure num")
fileName1 = sys.argv[1]
fileName2 = sys.argv[2]
measure = int(sys.argv[3])
runName1 = fileName1.replace("-measures.csv", "")
runName2 = fileName2.replace("-measures.csv", "")
filePath1 = Path("measures-files/" + fileName1)
filePath2 = Path("measures-files/" + fileName2)

one =  pd.read_csv(filePath1, header=None)
two = pd.read_csv(filePath2, header=None)

mean1 = one[measure].mean()
mean2 = two[measure].mean()
set1 = one[measure].tolist()
set2 = two[measure].tolist()
largest = max([mean1, mean2])
smallest = min([mean1, mean2])
improvement = 100*(largest - smallest) / smallest
pValue = stats.ttest_rel(set1, set2)

with open("single-result.csv", "w", newline='') as output:
    writer = csv.writer(output)
    writer.writerow([round(largest,3), round(smallest,3), round(improvement,3),round(pValue.pvalue,3)])
