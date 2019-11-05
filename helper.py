# Symbol file value indexes for specified line
symtype_to_idx = {'Composite': 0, 'Module': 1, 'Annotate': 3, 'Pin': 4, 'Border': 5}
lbl_to_idx = {'L': 0, 'x': 1, 'y': 2, 'size': 3, 'rotation': 4, 'justification': 5, 'unk': 6, 'visible': 7, 'unk2': 8, 'value': 9} # Line row values to string index

# Mentor Graphics human to index conversions
lbl_vis_dict = {'Hidden': 0, 'Visible': 1} # Label Visibility
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
    
def mils_to_units(mils):
    return int((mils/100)*254000)

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
        
class Property:
    idx = {'A': 0, 'x': 1, 'y': 2, 'size': 3, 'rotation': 4, 'justification': 5, 'visible': 6, 'value': 7}
    just_dict = {'Upper Left': 1, 'Middle Left': 2, 'Lower Left': 3, 'Upper Center': 4, 'Middle Center': 5, 'Lower Center': 6, 'Upper Right': 7, 'Middle Right': 8, 'Lower Right': 9}
    rotation_dict = {0: '0', 1: '90', 2: '180', 3: '270'}
    vis_dict = {'Hidden': 0, 'Hidden-wProperty': 2, 'Visible': 3, 'Visible-wProperty': 4}
    
    def __init__(self):
        self.idx2val = {v:k for k, v in self.idx.items()}
        self.vis_idx2val = {v:k for k, v in self.vis_dict.items()}
        self.just_idx2val = {v:k for k, v in self.just_dict.items()}
    
    def create_property(self, line_str, identifier):
        vals = line_str.split()
        
        self.x = int(vals[self.idx['x']])
        self.y = int(vals[self.idx['y']])
        self.size = int(vals[self.idx['size']])
        self.rotation = self.rotation_dict[int(vals[self.idx['rotation']])]
        self.justification = self.just_idx2val[int(vals[self.idx['justification']])]
        self.visible = self.vis_idx2val[int(vals[self.idx['visible']])]
        self.value = ' '.join(vals[self.idx['value']:])[len(identifier):] # Account for spaces in property value
        self.property = identifier.split('=')[0]
        
    def define_property(self, prop, x, y, size, rot, just, vis, val):
        self.x = mils_to_units(x)
        self.y = mils_to_units(y)
        self.size = mils_to_units(size)
        self.rotation = self.rotation_dict[rot]
        self.justification = self.just_dict[just]
        self.visible = self.vis_dict[vis]
        self.value = val
        self.property = prop
        
    def get_str(self):
        vals = {self.idx['A']: 'A', 
            self.idx['x']: self.x,
            self.idx['y']: self.y,
            self.idx['size']: self.size,
            self.idx['rotation']: self.rotation,
            self.idx['justification']: self.justification,
            self.idx['visible']: self.visible,
            self.idx['value']: self.property+'='+str(self.value)}
            
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
class PinName(Property):
    idx = {'L': 0, 'x': 1, 'y': 2, 'size': 3, 'rotation': 4, 'justification': 5, 'unk': 6, 'visible': 7, 'unk2': 8, 'value': 9} # Line row values to string index
    vis_dict = {'Hidden': 0, 'Visible': 1}
    
    def __init__(self):
        super().__init__()
        
    def create_property(self, line_str):
        super().create_property(line_str, '')
        
    def define_property(self, x, y, size, rot, just, vis, val):
        super().define_property('', x, y, size, rot, just, vis, val)
        
    def get_str(self):
        vals = {self.idx['L']: 'L', 
            self.idx['x']: self.x,
            self.idx['y']: self.y,
            self.idx['size']: self.size,
            self.idx['rotation']: self.rotation,
            self.idx['justification']: self.justification,
            self.idx['visible']: self.visible,
            self.idx['value']: str(self.value),
            self.idx['unk']: 0,
            self.idx['unk2']: 0}
            
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
  
class Pin:
    idx = {'P': 0, 'id': 1, 'x1': 2, 'y1': 3, 'x2': 4, 'y2': 5, 'unk': 6, 'side': 7, 'inverted': 8} # Pin row to string index
    side_dict = {'Top': 0, 'Bottom': 1, 'Left': 2, 'Right': 3}
    inv_dict = {False: 0, 'False': 0, 'FALSE': 0, 'Inverted': 1, True: 1, 'True': 1, 'TRUE': 1} # Inverted
    pin_types = ['IN', 'OUT', 'BI', 'TRI', 'OCL', 'OEM', 'POWER', 'GROUND', 'ANALOG']
    
    def __init__(self):
        self.idx2val = {v:k for k, v in self.idx.items()}
        
    def define_pin_from_str(self, line_str):
        vals = line_str.split()
        
        self.pid = vals[self.idx['id']]
        self.set_line_pos(vals[self.idx['x1']], vals[self.idx['x2']], vals[self.idx['y1']], vals[self.idx['y2']])
        self.side = self.side_dict[int(vals[self.idx['side']])]
        self.inverted = bool(int(vals[self.idx['inverted']]))
    
    def define_pin(self, pid, x1, y1, x2, y2, side, inv, ptype):
        self.pid = pid
        self.set_line_pos(mils_to_units(x1), mils_to_units(x2), mils_to_units(y1), mils_to_units(y2))
        self.side = self.side_dict[side]
        self.inverted = self.inv_dict[inv]
        self.define_pin_type(ptype)
        
    def define_pin_type(self, val):
        assert val in self.pin_types
        p = Property()
        p.define_property('PINTYPE', 0, 0, 100, 0, 'Middle Left', 'Hidden', val)
        self.Type = p
        
    def define_pin_name(self, x, y, side, val):
        lbl_x = x
        lbl_y = y
        lbl_delta = 350
        
        # TODO: Add justification for Top and Bottom pins
        just = 'Middle ' + side
        if side == 'Left':
            lbl_x += lbl_delta
        elif side == 'Right':
            lbl_x -= lbl_delta
        
        name = PinName()
        name.define_property(lbl_x, lbl_y, 100, 0, just, 'Visible', val)
        self.Name = name
        
    def define_pin_number(self, x, y, side, val):
        num_x = x
        num_y = y
        num_just = 'Lower Right'
        
        # TODO: Add justification for Top and Bottom pins
        num_delta_x = 200
        if side == 'Left':
            num_x += num_delta_x
        elif side == 'Right':
            num_x -= num_delta_x
            num_just = 'Lower Left'
        
        num = Property()
        num.define_property('#', num_x, num_y, 100, 0, num_just, 'Visible', val)
        self.Number = num
     
    """
    x - int: x coordinate starting location in mils
    y - int: y coordinate starting location in mils
    side - string: Left, Right, Top, Bottom
    inv - bool: Include Invert symbol indicator
    """
    def simple_pin(self, pid, x, y, side, inv, ptype, name, number):
        pin_length = 300 # 300 mils
        x1 = x
        x2 = x
        y1 = y
        y2 = y
        
        if side == 'Left':
            x2 = x1 + pin_length
        elif side == 'Right':
            x2 = x1 - pin_length
        elif side == 'Top':
            y1 = y2 + pin_length
        elif side == 'Bottom':
            y2 = y1 + pin_length
            
        self.define_pin(pid, x1, y1, x2, y2, side, inv, ptype)
        self.define_pin_name(x, y, side, name)
        self.define_pin_number(x, y, side, number)
    
    def get_str(self):
        x1, x2, y1, y2 = self.line_pos
        vals = {}        
        vals[self.idx['P']] = 'P'
        vals[self.idx['id']] = self.pid
        vals[self.idx['x1']] = x1
        vals[self.idx['y1']] = y1
        vals[self.idx['x2']] = x2
        vals[self.idx['y2']] = y2
        vals[self.idx['unk']] = 0
        vals[self.idx['side']] = self.side
        vals[self.idx['inverted']] = self.inverted
        
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
    def get_pintype_str(self): 
        return self.Type.get_str()  
        
    # number: PinNumber Object
    def set_number(self, number):
        self.Number = number
    
    # ptype: PinType Object
    def set_type(self, ptype):
        self.Type = ptype
        
    def set_line_pos(self, x1, x2, y1, y2):
        self.line_pos = (int(x1), int(x2), int(y1), int(y2))
        
    # name: PinName Object
    def set_name(self, name):
        self.Name = name
        