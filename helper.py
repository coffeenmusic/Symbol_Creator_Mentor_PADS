# Symbol file value indexes for specified line
symtype_to_idx = {'Composite': 0, 'Module': 1, 'Annotate': 3, 'Pin': 4, 'Border': 5}
a_to_idx = {'A': 0, 'x': 1, 'y': 2, 'size': 3, 'rotation': 4, 'justification': 5, 'visible': 6, 'value': 7}
pin_to_idx = {'P': 0, 'id': 1, 'x1': 2, 'y1': 3, 'x2': 4, 'y2': 5, 'unk': 6, 'side': 7, 'inverted': 8} # Pin row to string index
lbl_to_idx = {'L': 0, 'x': 1, 'y': 2, 'size': 3, 'rotation': 4, 'justification': 5, 'unk': 6, 'visible': 7, 'unk2': 8, 'value': 9} # Line row values to string index

# Mentor Graphics human to index conversions
lbl_vis_dict = {'Hidden': 0, 'Visible': 1} # Label Visibility
prp_vis_dict = {'Hidden': 0, 'Hidden-wProperty':2, 'Visible': 3, 'Visible-wProperty': 4} # Property Visibility
inv_dict = {False: 0, 'False': 0, 'FALSE': 0, 'Inverted': 1, True: 1, 'True': 1, 'TRUE': 1} # Inverted
side_dict = {'Top': 0, 'Bottom': 1, 'Left': 2, 'Right': 3}
rotation_dict = {'0': 0, '90': 1, '180': 2, '270': 3, 0: 0, 90: 1, 180: 2, 270: 3}
just_dict = {'Upper Left': 1, 'Middle Left': 2, 'Lower Left': 3, 'Upper Center': 4, 'Middle Center': 5, 'Lower Center': 6, 'Upper Right': 7, 'Middle Right': 8, 'Lower Right': 9}
color_dict = {'Automatic': (-1,-1,-1), 'Red': (255,0,0), 'Dark Blue': (0,0,132), 'Blue': (0,0,255)}

pin_types = ['IN', 'OUT', 'BI', 'TRI', 'OCL', 'OEM', 'POWER', 'GROUND', 'ANALOG']

def rgb_to_int(red, green, blue):
    color = red << 16 | green << 8 | blue
    if red < 0 or green < 0 or blue < 0: # Set color to automatic
        color = -1
    return color

def color_to_int(color_str):
    return rgb_to_int(*color_dict[color_str])

class Box:
    idx = {'b': 0, 'x1': 1, 'y1': 2, 'x2': 3, 'y2': 4}
    
    def __init__(self):
        self.idx2val = {v:k for k, v in self.idx.items()}
        
    def create_box(self, line_str):
        vals = line_str.split()
        self.x1 = vals[self.idx['x1']]
        self.x2 = vals[self.idx['x2']]
        self.y1 = vals[self.idx['y1']]
        self.y2 = vals[self.idx['y2']]
    
    # Create string of format: 'b x1 y1 x2 y2'
    def create_str(self, x1, y1, x2, y2):
        vals = {}
        vals[self.idx['b']] = 'b'
        vals[self.idx['x1']] = x1
        vals[self.idx['y1']] = y1
        vals[self.idx['x2']] = x2
        vals[self.idx['y2']] = y2
        return ' '.join([str(vals[i]) for i in range(len(vals))])

class GFX:
    idx = {'|GRPHSTL_EXT01': 0, 'color': 1, 'fill-color': 2, 'fill-style': 3, 'line-style': 4, 'line-width': 5} # Graphics
    fill_style_idx = {'Automatic': -1, 'Hollow': 0, 'Solid': 1, 'Diagdn1': 2, 'Diagup2': 3, 'Grey08': 4, 'Diagdn2': 5, 'Diagup1': 6, 'Horiz': 7, 'Vert': 8, 'Grid2': 9, 'Grid1': 10, 'X2': 11, 'X1': 12, 'Grey50': 13, 'Grey92': 14, 'Grey04': 15}
    line_style_idx = {'Automatic': -1, 'Solid': 0, 'Dash': 1, 'Center': 2, 'Phantom': 3, 'Big Dash': 4, 'Dot': 5, 'Dash-Dot': 6, 'Medium dash': 7}
    
    def __init__(self):
        self.idx2val = {v:k for k, v in self.idx.items()}
    
    # Create string of format: '|GRPHSTL_EXT01 color fill-color fill-style line-style line-width'
    def create_str(self, hdr, color, fill_color, fill_style, line_style, w):
        vals = {}
        vals[0] = hdr
        vals[self.idx['color']] = color
        vals[self.idx['fill-color']] = fill_color
        vals[self.idx['fill-style']] = self.fill_style_idx[fill_style]
        vals[self.idx['line-style']] = self.line_style_idx[line_style]
        vals[self.idx['line-width']] = w
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
class Font:
    idx = {'|FNTSTL': 0, 'color': 1, 'type': 2}
    font_dict = {   'Fixed': 0, 
                'Roman': 1, 
                'Roman Italic': 2, 
                'Roman Bold': 3, 
                'Roman Bold Italic': 4, 
                'Sans Serif': 5, 
                'Script': 6, 
                'Sans Serif Bold': 7, 
                'Script Bold': 8, 
                'Gothic': 9, 
                'Old English': 10, 
                'Kanji': 11, 
                'Plot': 12, 
                'Custom Style': 13  }
    
    def __init__(self):
        self.idx2val = {v:k for k, v in self.idx.items()}
    
    # Create string of format: 'b x1 y1 x2 y2'
    def create_str(self, font, color):
        vals = {}
        vals[0] = self.idx2val[0]
        vals[self.idx['color']] = color_to_int(color)
        vals[self.idx['type']] = self.font_dict[font]
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        