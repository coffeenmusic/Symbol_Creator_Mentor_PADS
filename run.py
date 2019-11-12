import sys
import pandas as pd
from sym_creator import Symbol_Creator

csv_file_desc = """Note: 2 csv files are accepted, a simple csv that contains Pin Label, Pin Number, & Pin Type. This will create an output by assuming Side and Inverted. Also, a csv exported directly from Mentor Symbol editor is accepted. This file fully defines Side and Inverted. Pin y-position will be estimated via the Symbol_Creator classes conditional arguments."""

"""
python run.py cmd
"""
arg_cnt = len(sys.argv) - 1

py_name = sys.argv[0]

"""
cmd:
    - import symbol_name in_file out_dir
    - new symbol_name count out_dir
    - help
    
symbol_name: [Name Only no extension]

in_file: [Input csv filename]
    
out_dir: [Optional]
    Default to same directory
"""
cmd = sys.argv[1]

if arg_cnt >= 2:
    symbol_name = sys.argv[2]
    if '.' in symbol_name:
        symbol_name.split('.')[0] # Remove extension

if arg_cnt >= 3:
    in_file = sys.argv[3]

out_dir = ''
if arg_cnt >= 4:
    out_dir = sys.argv[4]
    
    
if cmd == 'import':
    if not('.' in in_file):
        in_file += '.csv'
        
    creator = Symbol_Creator(out_dir=out_dir, out_symbol_name=symbol_name)
    creator.symbol_from_csv(in_file)
    creator.export_symbol()
if cmd == 'new':
    count = int(in_file)
    creator = Symbol_Creator(out_dir=out_dir, out_symbol_name=symbol_name)
    creator.symbol_from_count(count) # in_file contains count
    creator.export_symbol()
else:
    print('--------------------------------------------------------')
    print('python {} cmd'.format(py_name))
    print("""cmd:
     - import symbol_name in_file out_dir
        + symbol_name: defines system file name and the Symbol Name property
        + in_file: csv file to import. There are 2 options. See note below *.
     - new symbol_name count out_dir
     - help
     """)
    print(csv_file_desc)