# Command Line
### Help:  
`python run.py help`  
  
### Import [outdir is optional]: Import a csv (see example csv or use export from PADS Symbol Editor)  
`python run.py import symbolname inputfilename outdir`  
Example: `python run.py import new_symbol example.csv NewSymbols`  

### New From Count
`python run.py new symbolname count outdir`  
Example: `python run.py new new_symbol 20`

# Symbol_Creator
### Import From csv
`creator = Symbol_Creator(out_dir='NewSymbols', out_symbol_name='new_symbol')`  
`creator.symbol_from_csv('import_file.csv')`  

### Import From PADS Symbol
`creator.import_symbol(sym_files[2])`  

### Export To PADS Symbol
`creator.export_symbol()`  

# Notes
- Currently only assumes IC type symbols that have a single bounding box
- Import from csv doesn't currently allow for HETERO, but import from symbol does
- Two csv files are accepted, a simple csv ('import_example.csv') that contains Pin Label, Pin Number, & Pin Type. This will create an output by predicting Side and Inverted. Also, a csv exported directly from Mentor Symbol editor is accepted. This file fully defines Side and Inverted. Pin y-position will be estimated via the Symbol_Creator classes conditional arguments.