import os
import numpy as np
import pandas as pd
import math
from collections import Counter
from sym_def import Symbol, Box, GFX, Font, Color, Pin, Property, PinName, mils_to_units, units_to_mils, side_dict, side_idx2val

class Symbol_Creator:
    """
    out_dir [str]: director path or name as string, don't need trailing /
    out_symbol_name [str]: name only, don't need extension
    """
    def __init__(self, out_dir='', out_symbol_name='export'):
        self.out_dir = out_dir
        self.out_symbol_name = out_symbol_name
    
    """
    f: open file to write symbol data to
    str_list [list]: a list where each new item is a string corresponding to a line in the symbol file
    """
    def write_str_list(self, f, str_list):
        for s in str_list:
            f.write(s)
            f.write('\n') 
    
    """
    Estimate the box outline width
    lbl_list: list of all pin labels
    lbl_size: label size in mils
    """
    def estimate_box_width(self, lbl_list, lbl_size=100):
        k = 22/38 # Rough estimate to be improved later if time
        max_w = max([len(l) for l in lbl_list])
        return math.ceil((int((max_w*k + 1)*2))/3)*3 * 100

    def estimate_box_height(self, count):
        return (math.ceil(count/2) + 2) * 100
    
    # From pins in the imported dataframe, find pins that share the same name minus the trailing _N or _P
    def get_diff_pairs(self, df):
        lbl_list = list(df['Pin Label'].values)
        diff_list = [l[:-1] if l.endswith(('_P', '_N')) else l for l in lbl_list]
        cnt = Counter(diff_list)
        diff_list = [l for l, v in cnt.items() if v > 1] # list labels that have both an _N and _P counterpart
        diff_list_full = [l for l in lbl_list if l.endswith(('_P', '_N')) and l[:-1] in diff_list] # get original label names for above list
        
        df['Diff'] = [diff_list.index(l[:-1]) if l in diff_list_full else -1 for l in lbl_list]
        return df
        
    """
    Pin order is defined as 0 to n from bottom to top
    df [DataFrame]: full csv as dataframe
    """
    def sort_pin_df(self, df):
        sort = ['Side', 'PWR', 'NC', 'PAD', 'GND', 'Diff', 'INV', 'Pin Number']
        
        nc = []
        pad = []
        gnd = []
        pwr = []
        inv = []
        
        idx = {col:i+1 for i, col in enumerate(df.columns)}
        for r in df.itertuples():
            i = r[0] # dataframe index
            lbl = r[idx['Pin Label']]
            num = r[idx['Pin Number']]
            ptype = r[idx['Pin Type']]
            side = r[idx['Side']]
            inverted = r[idx['Inverted']]
            diff = r[idx['Diff']]
            
            # Pins on symbols bottom should be lower numbers: 0
            # Pin at top should be higher numbers: n
            nc += [0 if lbl.startswith('NC') else 1]
            pad += [0 if 'PAD' in lbl else 1]
            gnd += [0 if ptype == 'GROUND' else 1]
            pwr += [1 if ptype == 'POWER' else 0] 
            inv += [0 if inverted else 1]
        
        df.loc[:, 'NC'] = nc
        df.loc[:, 'PAD'] = pad
        df.loc[:, 'GND'] = gnd
        df.loc[:, 'PWR'] = pwr
        df.loc[:, 'INV'] = inv
        
        df.sort_values(by=sort, inplace=True)
        df.reset_index(inplace=True, drop=True)
        
        df.loc[df.Side == side_dict['Left'], 'sort'] = [i for i in range(len(df.loc[df.Side == side_dict['Left'], 'Side']))]
        df.loc[df.Side == side_dict['Right'], 'sort'] = [i for i in range(len(df.loc[df.Side == side_dict['Right'], 'Side']))]
        
        return df
        
    def get_gaps(self, df):
        gap_list = []
        prev_diff = False
        gaps = np.zeros((len(df)))
        
        idx = {col:i+1 for i, col in enumerate(df.columns)}
        for i, r in enumerate(df.itertuples()):
            
            lbl = r[idx['Pin Label']]
            ptype = r[idx['Pin Type']]
            side = r[idx['Side']]
            inv = r[idx['Inverted']]
            diff = r[idx['Diff']]
            sort = r[idx['sort']]

            # Add gaps to differential pairs
            if diff and inv:
                gaps[i] = 1
            elif diff and not(inv):
                if i + 1 < len(df):
                    gaps[i+1] = 2
                
            if lbl.startswith('NC'):
                if i + 1 < len(df):
                    gaps[i+1] = 1
                
            if gaps[i] == 2:
                if not(diff):
                    gaps[i] = 1
            
            # Don't add gaps if this is the first pin
            if sort == 0:
                gaps[i] = 0
            
        df['gap'] = gaps
        
        return df
        
    def get_coordinates(self, df, w, pin_len=300):
        df = self.sort_pin_df(df)
        df = self.get_gaps(df)
        
        x = []
        y = []
        
        idx = {col:i+1 for i, col in enumerate(df.columns)}
        for r in df.itertuples():
            i = r[0] # dataframe index
            order = r[idx['Pin Order']]
            lbl = r[idx['Pin Label']]
            num = r[idx['Pin Number']]
            ptype = r[idx['Pin Type']]
            side = r[idx['Side']]
            inv = r[idx['Inverted']]
            diff = r[idx['Diff']]
            sort = r[idx['sort']]
            gap = r[idx['gap']]
            
            if sort == 0:
                gaps = 0
            
            gaps += gap*100
            x += [0 if side == side_dict['Left'] else w + pin_len*2]
            y += [sort*100 + gaps]
            
        df.loc[:, 'x'] = x
        df.loc[:, 'y'] = y
        
        return df
        
    def symbol_from_csv(self, csv_file, symbol_name, pin_len = 300, box_margin=100):    
        # Import CSV
        df = pd.read_csv(csv_file, delimiter=';')
        df = self.get_diff_pairs(df)
        
        w = self.estimate_box_width(list(df['Pin Label'].values))
        
        # Get Coordinates
        df = self.get_coordinates(df, w, pin_len=pin_len)
        
        h = max(df.y.values) + box_margin*2
        print('{}x{}'.format(w, h))
        
        symbol = Symbol()
        idx = {col:i+1 for i, col in enumerate(df.columns)}
        # Create and add pins to symbol object for each pin in imported csv
        for r in df.itertuples():
            i = r[0] # dataframe index
            order = r[idx['Pin Order']]
            lbl = r[idx['Pin Label']]
            num = r[idx['Pin Number']]
            ptype = r[idx['Pin Type']]
            side = r[idx['Side']]
            inv = r[idx['Inverted']]
            diff = r[idx['Diff']]
            x = r[idx['x']]
            y = r[idx['y']]
            
            symbol.add_pin(i+1, x, y, side_idx2val[side], inv, num, lbl, ptype)
        
        # Create and add symbol box
        box = symbol.add_box(300, -100, w, h)
        
        self.sym_str_list = symbol.get_symbol_str_list()
        
    def export_symbol(self):
        f = open(os.path.join(self.out_dir, self.out_symbol_name) + '.1', 'w')
        self.write_str_list(f, self.sym_str_list)
        f.close()