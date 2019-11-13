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
- Symbol files have graphics settings that will export, but are currently not imported from the Symbol import