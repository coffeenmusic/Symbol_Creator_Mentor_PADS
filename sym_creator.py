import os
import numpy as np
import pandas as pd
import math
import re
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
        self.create_default_conditions()
    
    # Default conditional arguments that define which side pins fall on
    def create_default_conditions(self):
        cond_list = ['not IN sw OUT R', 'not IN ew OUT R', 'not IN sw IN L', 'is IN all IN L', 'is OUT all OUT R']
        
        # Starts With substring, any pin type
        left = ['ADDR','EN_']
        cond_list += ['is any sw ' + v + ' L' for v in left]
        right = ['FB','NC','PG','SW','VCC','VDD']
        cond_list += ['is any sw ' + v + ' R' for v in right]
        
        # Contains substring, any pin type
        left = ['GND','GROUND','PAD','SCL','SDA']
        cond_list += ['is any c ' + v + ' L' for v in left]
        
        # Equals string, any pin type
        left = ['BIAS','EN','PVIN','RESET','VIN']
        cond_list += ['is any eq ' + v + ' L' for v in left]
        right = ['SNS','VSNS']
        cond_list += ['is any eq ' + v + ' R' for v in right]
        
        self.default_cond_list = cond_list
    
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
        diff_pair_identifiers = ('_N', '_P')
    
        lbl_list = list(df['Pin Label'].values)
        diff_list = [l[:-1] if l.endswith(diff_pair_identifiers) else l for l in lbl_list]
        cnt = Counter(diff_list)
        diff_list = [l for l, v in cnt.items() if v > 1] # list labels that have both an _N and _P counterpart
        diff_list_full = [l for l in lbl_list if l.endswith(diff_pair_identifiers) and l[:-1] in diff_list] # get original label names for above list
        
        df['Diff'] = [diff_list.index(l[:-1]) if l in diff_list_full else -1 for l in lbl_list]
        return df
        
    """
    Get signals that should be grouped together. Looks for matching names that end in numeric values
    """    
    def get_groups(self, df):
        p = re.compile('[a-zA-Z]{2,}[0-9]{1,}')
        matches = []
        for v in df['Pin Label'].values:
            m = p.match(v)
            if m != None:
                match_val = m.group()
                matches += [''.join([v for v in match_val if v.isalpha()])]
                
        # list of groups found
        groups = [k for k, v in Counter(matches).items() if v > 1]
        groups.sort()
        
        # enumerates groups with a group index from 0 to n. -1 for names that don't have a group
        df['group'] = [[i for i, g in enumerate(groups) if v.startswith(g)][0] if v.startswith(tuple(groups)) else -1 for v in df.loc[:, 'Pin Label'].values]
        return df
    
        
    """
    Sort df by values in sort list in decreasing order of importance
    Pin order is defined as 0 to n from bottom to top of symbol
    - df [DataFrame]: full csv as dataframe
    returns: sorted dataframe
    """
    def sort_pin_df(self, df):
        sort = ['Side', 'PWR', 'NC', 'PAD', 'GND', 'group', 'Diff', 'INV', 'Pin Number']
        df = self.get_groups(df)
        
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
    
    # Adds gaps between pins for given definition below
    # Setting a gap for a pin means the gap occurs below the pin
    def get_gaps(self, df):
        gap_list = []
        prev_diff = False
        gaps = np.zeros((len(df)))
        
        # Get gaps for pin type changes
        pt_list = list(df['Pin Type'].values)
        temp = pd.DataFrame({'Pin Type': pt_list, 'Next Type': [df.iloc[0]['Pin Type']]+pt_list[:-1]})
        df['Type_Change'] = temp['Pin Type'] != temp['Next Type']
        
        idx = {col:i+1 for i, col in enumerate(df.columns)}
        for i, r in enumerate(df.itertuples()):
            lbl = r[idx['Pin Label']]
            ptype = r[idx['Pin Type']]
            inv = r[idx['Inverted']]
            diff = r[idx['Diff']] >= 0
            sort = r[idx['sort']]
            tc = r[idx['Type_Change']]

            # Add gaps to differential pairs
            if diff and inv:
                gaps[i] = 1
            elif diff and not(inv):
                if i + 1 < len(df):
                    gaps[i+1] = -1
                
            if lbl.startswith('NC'):
                if i + 1 < len(df):
                    gaps[i+1] = 1 
            if tc:
                gaps[i] = 1
                
            if gaps[i] == -1:
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
        
        gaps = 0
        
        idx = {col:i+1 for i, col in enumerate(df.columns)}
        for r in df.itertuples():
            i = r[0] # dataframe index
            #order = r[idx['Pin Order']]
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
    
    """
    If names end with active low identifier, example '_N', then set inverted true and add to dataframe
    - df [dataframe]: csv as pandas df with pin labels.
    returns: dataframe
    """
    def predict_inverted_to_df(self, df):
        al = Pin().active_low_identifiers
        inv = [False]*len(df)
        
        idx = {col:i+1 for i, col in enumerate(df.columns)}
        for i, r in enumerate(df.itertuples()):
            lbl = r[idx['Pin Label']]
            
            if lbl.endswith(al):
                inv[i] = True
                
        df['Inverted'] = inv
        return df 

    """
    If pin type is in or name contains IN, then left side. Else right side.
    - df [dataframe]: csv as pandas df with pin type and label.
    - cond_list [list of strs]: each string in format to control which side
        'operator ptype method string side'. Example: 'not IN sw OUT R'
            operator: is, not (specifies not ptype. Ex: 'not IN' means any ptype except IN])
            ptype: any, IN, OUT, BI, TRI, ANALOG, POWER, etc.
            method: startswith 'sw', endswith 'ew', contains 'c', set for all pin names 'all ptype' ex: 'is IN all IN L' (sets all input pins to the left), equals 'eq'
            string: part of text you want to analyze in the pin label. Example: 'PAD'
            side: Left or Right
        note: items at the end of the list take highest priority
    returns: dataframe with addition of side column
    """
    def predict_side_to_df(self, df, cond_list):
        side_dict = Pin().side_dict
        cond2side = {'L':'Left', 'R':'Right', 'T':'Top', 'B':'Bottom'} # convert condition_list script sides to full word
        side = ['Left']*len(df)
        
        idx = {col:i+1 for i, col in enumerate(df.columns)}
        for i, r in enumerate(df.itertuples()):
            lbl = r[idx['Pin Label']]
            ptype = r[idx['Pin Type']]
            
            for c in cond_list:
                c = c.split()
                assert len(c) == 5, 'Each item in conditional list must contain 5 items seperated by spaces!'
                op = c[0] # Operator
                pt = c[1] # Pin Type
                mt = c[2] # Method
                t = c[3] # String Text
                s = cond2side[c[4]] # side
                
                # All these if statements just parse the cond_list of input scripts
                if op == 'is':
                    if ptype == pt:
                        if mt == 'sw':
                            if lbl.startswith(t):
                                side[i] = s
                        elif mt == 'ew':
                            if lbl.endswith(t):
                                side[i] = s
                        elif mt == 'c':
                            if t in lbl:
                                side[i] = s    
                        elif mt == 'eq':
                            if t == lbl:
                                side[i] = s
                        elif mt == 'all':
                            side[i] = s
                elif op == 'not':
                    if ptype != pt:
                        if mt == 'sw':
                            if lbl.startswith(t):
                                side[i] = s
                        elif mt == 'ew':
                            if lbl.endswith(t):
                                side[i] = s
                        elif mt == 'c':
                            if t in lbl:
                                side[i] = s
                        elif mt == 'eq':
                            if t == lbl:
                                side[i] = s
                        elif mt == 'all':
                            side[i] = s
                                
        df['Side'] = [side_dict[v] for v in side]
        return df 
        
    def symbol_from_csv(self, csv_file, symbol_name, pin_len = 300, box_margin=100, cond_list=None):    
        # Import CSV
        df = pd.read_csv(csv_file, delimiter=';')
        df = self.get_diff_pairs(df)
        
        # If csv doesn't have Inverted Column, then create it
        if not('Inverted' in df.columns.values):
            df = self.predict_inverted_to_df(df)
        if not('Side' in df.columns.values):
            if cond_list == None:
                cond_list = self.default_cond_list
            df = self.predict_side_to_df(df, cond_list)
        
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
            #order = r[idx['Pin Order']]
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