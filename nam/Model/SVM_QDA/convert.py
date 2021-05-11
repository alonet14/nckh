import numpy as np

a = np.loadtxt("HR_RR_T_SVM_1.txt")
b = a[:,2]
np.savetxt('b.txt', b)
import pandas as pd

read_file = pd.read_csv (r'b.txt')
read_file.to_csv (r'b.csv', index=None)