import datetime

# Mentor Graphics human to index conversions
side_dict = {'Top': 0, 'Bottom': 1, 'Left': 2, 'Right': 3}
side_idx2val = {v:k for k, v in side_dict.items()}
    
def mils_to_units(mils):
    return int((mils/100)*254000)
    
def units_to_mils(units):
    return (units/254000)*100

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
        
    def set_box(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        
    def add_graphics(self, color, fill_style, line_style, w):
        g = GFX()
        g.set_graphics('|GRPHSTL_EXT01', color, color, fill_style, line_style, w)
        self.gfx = g
    
    # Create string of format: 'b x1 y1 x2 y2'
    def get_str(self):
        vals = {}
        vals[self.idx['b']] = 'b'
        vals[self.idx['x1']] = self.x1
        vals[self.idx['y1']] = self.y1
        vals[self.idx['x2']] = self.x2
        vals[self.idx['y2']] = self.y2
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
    def get_str_list(self):
        str_list = [self.get_str()]
        str_list += [self.gfx.get_str()]
        return str_list
        
class Color:                
    color_dict = {'Automatic': (-1,-1,-1), 'Red': (255,0,0), 'Dark Blue': (0,0,132), 'Blue': (0,0,255)}
    
    def __init__(self):
        self.color_idx2val = {v:k for k, v in self.color_dict.items()}
    
    # Set color values from color string
    def set_color(self, color_str):
        self.set_rgb(*self.color_dict[color_str])
    
    # Set color values from red green and blue 0-255 integers
    def set_rgb(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
        self.color_int = self.rgb_to_int(red, green, blue)
    
    # 0-255 red green & blue channels to 24bit int containing 8bits for each R,G,B channel
    def rgb_to_int(self, red, green, blue):
        color_int = red << 16 | green << 8 | blue
        if red < 0 or green < 0 or blue < 0: # Set color to automatic
            color_int = -1
        return color_int

    # Color string to 24bit int 8bits for R,G,B channels
    def color_to_int(self, color_str):
        return self.rgb_to_int(*self.color_dict[color_str])

class GFX:
    idx = {'|GRPHSTL_EXT01': 0, 'color': 1, 'fill-color': 2, 'fill-style': 3, 'line-style': 4, 'line-width': 5} # Graphics
    fill_style_idx = {'Automatic': -1, 'Hollow': 0, 'Solid': 1, 'Diagdn1': 2, 'Diagup2': 3, 'Grey08': 4, 'Diagdn2': 5, 'Diagup1': 6, 'Horiz': 7, 'Vert': 8, 'Grid2': 9, 'Grid1': 10, 'X2': 11, 'X1': 12, 'Grey50': 13, 'Grey92': 14, 'Grey04': 15}
    line_style_idx = {'Automatic': -1, 'Solid': 0, 'Dash': 1, 'Center': 2, 'Phantom': 3, 'Big Dash': 4, 'Dot': 5, 'Dash-Dot': 6, 'Medium dash': 7}
    
    def __init__(self):
        self.idx2val = {v:k for k, v in self.idx.items()}
    
    """
    - hdr [str]: Mentor symbol files header for given line. Ex: |GRPHSTL_EXT01
    - color_str [str]: color string defined in Color class' color_dict Keys
    - fill_color_str [str]: fill color string defined in Color class' color_dict Keys
    - fill_style [str]: see fill_style_idx Keys
    - line_style [str]: see line_style_idx Keys
    - w [int or str]: numeric value in pixels
    returns: Mentor symbol file string
    """
    def set_graphics(self, hdr, color_str, fill_color_str, fill_style, line_style, w):
        c = Color()
        c.set_color(color_str)
        
        c_fill = Color()
        c_fill.set_color(fill_color_str)
    
        self.header = hdr
        self.color = c
        self.fill_color = c_fill
        self.fill_style = self.fill_style_idx[fill_style]
        self.line_style = self.line_style_idx[line_style]
        self.line_width = w
        return self.get_str()
        
    # Create string of format: '|GRPHSTL_EXT01 color fill-color fill-style line-style line-width'
    def get_str(self):
        vals = {}
        vals[0] = self.header
        vals[self.idx['color']] = self.color.color_int
        vals[self.idx['fill-color']] = self.fill_color.color_int
        vals[self.idx['fill-style']] = self.fill_style
        vals[self.idx['line-style']] = self.line_style
        vals[self.idx['line-width']] = self.line_width
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
class Font:
    idx = {'|FNTSTL': 0, 'color': 1, 'type': 2}
    font_dict = {'Fixed': 0, 
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
     
    """
    - font [str]: font string that is one of the Keys from font_dict
    - color [str]: color string that is one of the Keys from color_dict
    returns: string in Mentor symbol file format
    """
    def set_font(self, font, color_str):
        c = Color()
        c.set_color(color_str)
        
        self.color = c
        self.font = self.font_dict[font]
        return self.get_str()
    
    def get_str(self):
        vals = {}
        vals[0] = self.idx2val[0]
        vals[self.idx['color']] = self.color.color_int
        vals[self.idx['type']] = self.font
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
class Property:
    idx = {'x': 1, 'y': 2, 'size': 3, 'rotation': 4, 'justification': 5, 'visible': 6, 'value': 7}
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
        
    def set_property(self, hdr, prop, x, y, size, rot, just, vis, val):
        self.hdr = hdr
        self.x = mils_to_units(x)
        self.y = mils_to_units(y)
        self.size = mils_to_units(size)
        self.rotation = self.rotation_dict[rot]
        self.justification = self.just_dict[just]
        self.visible = self.vis_dict[vis]
        self.value = val
        self.property = prop
        
    def get_str(self):
        vals = {0: self.hdr, 
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
        
    def set_property(self, x, y, size, rot, just, vis, val):
        super().set_property('L', '', x, y, size, rot, just, vis, val)
        
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
        
    def set_pin_from_str(self, line_str):
        vals = line_str.split()
        
        self.pid = vals[self.idx['id']]
        self.set_line_pos(vals[self.idx['x1']], vals[self.idx['x2']], vals[self.idx['y1']], vals[self.idx['y2']])
        self.side = self.side_dict[int(vals[self.idx['side']])]
        self.inverted = bool(int(vals[self.idx['inverted']]))
    
    def set_pin(self, pid, x1, y1, x2, y2, side, inv, ptype):
        self.pid = pid
        self.set_line_pos(mils_to_units(x1), mils_to_units(x2), mils_to_units(y1), mils_to_units(y2))
        self.side = self.side_dict[side]
        self.inverted = self.inv_dict[inv]
        self.set_pin_type(ptype)
        
    def set_pin_type(self, val):
        assert val in self.pin_types
        p = Property()
        p.set_property('A', 'PINTYPE', 0, 0, 100, 0, 'Middle Left', 'Hidden', val)
        self.Type = p
        
    def set_pin_name(self, x, y, side, val):
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
        name.set_property(lbl_x, lbl_y, 100, 0, just, 'Visible', val)
        self.Name = name
        
    def set_pin_number(self, x, y, side, val):
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
        num.set_property('A', '#', num_x, num_y, 100, 0, num_just, 'Visible', val)
        self.Number = num
     
    """
    - x [int]: x coordinate starting location in mils
    - y [int]: y coordinate starting location in mils
    - side [str]: Left, Right, Top, Bottom
    - inv [bool]: Include Invert symbol indicator
    - ptype [str]: 'IN', 'OUT', 'BI', 'TRI', 'OCL', 'OEM', 'POWER', 'GROUND', 'ANALOG'
    - name [str]: pin name
    - number [int or str]: pin number
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
            
        self.set_pin(pid, x1, y1, x2, y2, side, inv, ptype)
        self.set_pin_name(x, y, side, name)
        self.set_pin_number(x, y, side, number)
    
    # Gets string for pin row. Ex: 
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
        
    def get_str_list(self, name_font='Sans Serif', num_font='Sans Serif', name_color='Dark Blue', num_color='Automatic'):
        str_list = []
        str_list += [self.get_str()]
            
        str_list += [self.Name.get_str()]
        str_list += [Font().set_font(name_font, name_color)]
        
        str_list += [self.get_pintype_str()]
        
        str_list += [self.Number.get_str()]
        str_list += [Font().set_font(num_font, num_color)]
        
        return str_list
        
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
        
        
class Symbol:
    pins = {}
    boxes = []
    sym_headers = ['K','|R','Y','U','b']
    k_idx = {'name': 2}
    d_idx = {'date': 1} # Date row indexes
    u_idx = {'x': 1, 'y': 2, 'size': 3, 'rotation': 4, 'justification': 5, 'visible': 6, 'value': 7}
    y_idx = {'value': 1}
    symtype_to_idx = {'Composite': 0, 'Module': 1, 'Annotate': 3, 'Pin': 4, 'Border': 5}
    vis_dict = {0: 'Hidden', 2: 'Hidden-wProperty', 3: 'Visible', 4: 'Visible-wProperty'}
    sym_type = {0: 'Composite', 1: 'Module', 2: 'Pin', 4: 'Annotate', 5: 'Border'}
    
    def __init__(self, symbol_type='Module'):
        self.set_defaults()
        self.symbol_type = symbol_type
    
    """
    pid [int]: pin id
    x [int]: x starting coordinate in mils
    y [int]: y starting coordinate in mils
    side [str]: Left, Right, Top, or Bottom
    inv [bool or str or int]: Add Invert symbol to pin. True False, 0 1
    num [int or str]: pin number
    label [str]: pin name
    pin_type [str]: 'IN', 'OUT', 'BI', 'TRI', 'OCL', 'OEM', 'POWER', 'GROUND', 'ANALOG'
    """
    def add_pin(self, pid, x, y, side, inv, num, label, pin_type):
        pin = Pin()
        pin.simple_pin(pid, x, y, side, inv, pin_type, label, num)
        self.pins[pin.Number.value] = pin
    
    # Box that surrounds pin names and touches pins
    def add_box(self, x, y, w, h, color='Blue', fill_style='Hollow', line_style='Solid', line_width=1):
        x2 = x + w
        y2 = y + h
        box = Box()
        box.set_box(mils_to_units(x), mils_to_units(y), mils_to_units(x2), mils_to_units(y2))
        box.add_graphics(color, fill_style, line_style, line_width)
        self.box = box
        
        # Add refdes above box
        self.set_refdes(units_to_mils(box.x1), units_to_mils(box.y2))
        
        return box
        
    def units_to_mils(self, unit):
        return 100*unit/254000
    
    def parse_sym(self, line_str):
        vals = line_str.split()
        if vals[0] == 'K':
            self.name = vals[self.k_idx['name']]
        elif vals[0] == '|R':
            self.save_date = vals[self.d_idx['date']]
        elif vals[0] == 'Y':
            self.symbol_type = self.sym_type[int(vals[self.y_idx['value']])]
        elif vals[0] == 'U':
            self.parse_property(line_str)
        elif vals[0] == 'b':
            self.boxes += [Box(line_str)]
            
    def parse_property(self, line_str):
        sym_property = SymProperty(line_str)
        if sym_property.property == 'DEVICE':
            self.device = sym_property
        elif sym_property.property == 'FORWARD_PCB':
            self.forward = sym_property
        elif sym_property.property == 'HETERO':
            self.hetero = sym_property
        elif sym_property.property == 'PKG_STYLE':
            self.pkg_style = sym_property
        elif sym_property.property == 'PKG_TYPE':
            self.pkg_type = sym_property
        elif sym_property.property == 'PLACE':
            self.place = sym_property
        elif sym_property.property == 'REFDES':
            self.refdes = sym_property
        elif sym_property.property == 'VALUE':
            self.value = sym_property
        elif sym_property.property == 'NAME_PLACEHOLDER':
            self.name_placeholder = sym_property
        
    
    def parse_pin(self, pin_str_list):
        for line_str in pin_str_list:
            if line_str.startswith('P '):
                p = Pin(line_str)
            elif line_str.startswith('L '):
                p.set_name(PinName(line_str))
            elif '#=' in line_str:
                p.set_number(PinNumber(line_str))
            elif 'PINTYPE=' in line_str:
                p.set_type(PinType(line_str))
        
        self.pins[p.Number.value] = p
        return p
        
    def set_defaults(self):        
        self.property_forward_pcb = self.get_default_property('FORWARD_PCB', 1)
        self.property_place = self.get_default_property('PLACE', 'YES')
        self.property_pkg_type = self.get_default_property('PKG_TYPE', 'PKG_TYPE')
        self.property_device = self.get_default_property('DEVICE', 'DEVICE')
        self.property_value = self.get_default_property('VALUE', 'VALUE', x=300, y=-200, vis='Visible')
        self.property_pkg_style = self.get_default_property('PKG_STYLE', 'PKG_STL', x=300, y=-300, vis='Visible')
        
    def set_refdes(self, box_min_x, box_max_y):
        x = box_min_x + 100 # Add delta 100mil
        y = box_max_y + 100 # Add delta 100mil
        self.property_refdes = self.get_default_property('REFDES', 'U?', x=x, y=y, vis='Visible', just='Upper Left')
    
    # Get property object for one of the default symbol properties
    def get_default_property(self, prop, val, hdr='U', x=0, y=0, size=90, rot=0, just='Middle Left', vis='Hidden'):
        p = Property()
        p.set_property(hdr, prop, x, y, size, rot, just, vis, val)
        return p
  
    """
    - font [Font object]: change default font for symbol properties
    returns: all symbol file's properties as a list of strings
    """
    def get_property_str_list(self, font=None):
        if font == None:
            font = Font()
            font_str = font.set_font('Sans Serif', 'Automatic')
        else:
            font_str = font.get_str()
            
        str_list = []
        str_list += [self.property_forward_pcb.get_str()]
        str_list += [self.property_place.get_str()]
        str_list += [self.property_pkg_type.get_str()]
        str_list += [self.property_device.get_str()]
        str_list += [self.property_value.get_str()]
        str_list += [self.property_pkg_style.get_str()]
        str_list += [self.property_refdes.get_str()]
        
        str_list_w_fonts = [font_str]*2*len(str_list) # Create list twice the size of str_list filled with font strings
        str_list_w_fonts[::2] = str_list # Interleave the property strings into the font list for every other index
        
        return str_list_w_fonts
    
    # Returns all pin string rows in one concatenated list for the entire symbol
    def get_pins_str_list(self):
        str_list = []
        for p in self.pins.values():
            str_list += p.get_str_list()
        return str_list
        
    def get_box_str_list(self):
        return self.box.get_str_list()
    
    # Some of the header definition is unknown Ex: V, K's int value, F Case, and D
    def get_header_str_list(self):
        hdr = ['V 54']
        hdr += ['K 33671749690 new_symbol']
        hdr += ['F Case']
        hdr += ['|R ' + datetime.datetime.now().strftime('%H:%M:%S_%m-%d-%y')]
        hdr += ['|BORDERTYPESUPPORT']
        hdr += ['Y ' + str(self.symtype_to_idx[self.symbol_type])]
        hdr += ['D 0 0 2540000 2540000', 'Z 10', 'i 3', '|I 6']
        return hdr
    
    def get_footer_str_list(self):
        return ['E']
        
    # returns a list of all text necessary to recreate a symbol file
    # this includes header, symbol properties, pins, fonts, graphics, and symbol box
    def get_symbol_str_list(self):
        str_list = []
        str_list += self.get_header_str_list()
        str_list += self.get_pins_str_list()
        str_list += self.get_box_str_list()
        self.get_property_str_list()
        str_list += self.get_footer_str_list()
        
        return str_list
        