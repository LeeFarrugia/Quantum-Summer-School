import pandas as pd
import numpy as np

import pydicom
from pydicom.data import get_testdata_file

filename = get_testdata_file('rtplan.dcm')
ds = pydicom.dcmread(filename)

print(ds)

# df = pd.read_excel('cath_dummy_data.xlsx', sheet_name='Sheet1') 

# df['ProcedureDate'] = pd.to_datetime(df['ProcedureDate'])
# df['DOB'] = pd.to_datetime(df['DOB'])

# df['Age'] = np.floor((df['ProcedureDate'] - df['DOB']).dt.days / 365.25)

# print(df)