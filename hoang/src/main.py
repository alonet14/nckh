import PIL
import pandas
import os
from config import config_path as cfp

# path_name_file = cfp.path_to_project + cfp.path_to_data + '/1samp-2-60s.xlsx'
path_name_file = '/home/nvh/python_project/nckh/hoang/data/1samp-2-60s.xlsx'
data = pandas.read_excel(path_name_file, index_col=0)

print(data)
