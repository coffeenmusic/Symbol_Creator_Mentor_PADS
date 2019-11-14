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
        
    def set_box_from_str(self, line_str):
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
        
    def set_color_int(self, color_int):
        color_int = int(color_int)
        self.color_int = color_int
        self.blue = color_int & 255
        self.green = (color_int >> 8) & 255
        self.red = (color_int >> 16) & 255        
    
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
    idx = {'|GRPHSTL': 0, 'color': 1, 'fill-color': 2, 'line-style': 3, 'line-width': 4} # Graphics
    gfx01_idx = {'|GRPHSTL_EXT01': 0, 'color': 1, 'fill-color': 2, 'fill-style': 3, 'line-style': 4, 'line-width': 5} # Graphics Extension 1
    fill_style_idx = {'Automatic': -1, 'Hollow': 0, 'Solid': 1, 'Diagdn1': 2, 'Diagup2': 3, 'Grey08': 4, 'Diagdn2': 5, 'Diagup1': 6, 'Horiz': 7, 'Vert': 8, 'Grid2': 9, 'Grid1': 10, 'X2': 11, 'X1': 12, 'Grey50': 13, 'Grey92': 14, 'Grey04': 15}
    line_style_idx = {'Automatic': -1, 'Solid': 0, 'Dash': 1, 'Center': 2, 'Phantom': 3, 'Big Dash': 4, 'Dot': 5, 'Dash-Dot': 6, 'Medium dash': 7}
    
    def __init__(self):
        self.idx2val = {v:k for k, v in self.idx.items()}
        self.gfx01_idx2val = {v:k for k, v in self.gfx01_idx.items()}
        self.linestyle_idx2val = {v:k for k, v in self.line_style_idx.items()}
        self.fillstyle_idx2val = {v:k for k, v in self.fill_style_idx.items()}
    
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
        self.Color = c
        self.Fill_Color = c_fill
        #self.fill_style = self.fill_style_idx[fill_style]
        self.fill_style = fill_style
        #self.line_style = self.line_style_idx[line_style]
        self.line_style = line_style
        self.line_width = w
        return self.get_str()
        
    def set_graphics_from_str(self, line_str):
        vals = line_str.split()
        
        hdr = vals[0]
        idx = self.idx
        if hdr == self.gfx01_idx2val[0]:
            idx = self.gfx01_idx
            self.fill_style = self.fillstyle_idx2val[int(vals[idx['fill-style']])]
        
        self.header = hdr
        
        c = Color()
        c.set_color_int(vals[idx['color']])   
        self.Color = c
        
        c_fill = Color()
        c_fill.set_color_int(vals[idx['fill-color']])            
        self.Fill_Color = c_fill
        
        self.line_style = self.linestyle_idx2val[int(vals[idx['line-style']])]
        self.line_width = int(vals[idx['line-width']])
        
    # Create string of format: '|GRPHSTL_EXT01 color fill-color fill-style line-style line-width' or '|GRPHSTL color fill-color line-style line-width'
    def get_str(self):
        vals = {}
        
        idx = self.idx
        if self.header == self.gfx01_idx2val[0]:
            idx = self.gfx01_idx
            vals[idx['fill-style']] = self.fill_style_idx[self.fill_style]
            
        vals[0] = self.header
        vals[idx['color']] = self.Color.color_int
        vals[idx['fill-color']] = self.Fill_Color.color_int
        vals[idx['line-style']] = self.line_style_idx[self.line_style]
        vals[idx['line-width']] = self.line_width
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
        self.font_idx2val = {v:k for k, v in self.font_dict.items()}
     
    """
    - font [str]: font string that is one of the Keys from font_dict
    - color [str]: color string that is one of the Keys from color_dict
    returns: string in Mentor symbol file format
    """
    def set_font(self, font, color_str):
        c = Color()
        c.set_color(color_str)
        
        self.Color = c
        #self.font = self.font_dict[font]
        self.font = font
        return self.get_str()
        
    def set_font_from_str(self, line_str):
        vals = line_str.split()
        
        c = Color()
        c.set_color_int(vals[self.idx['color']])
        self.Color = c
        
        self.font = self.font_idx2val[int(vals[self.idx['type']])]
        
    def get_str(self):
        vals = {}
        vals[0] = self.idx2val[0]
        vals[self.idx['color']] = self.Color.color_int
        vals[self.idx['type']] = self.font_dict[self.font]
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
class Property:
    _idx = {'hdr': 0, 'x': 1, 'y': 2, 'size': 3, 'rotation': 4, 'justification': 5, 'visible': 6, 'value': 7}
    just_dict = {'Upper Left': 1, 'Middle Left': 2, 'Lower Left': 3, 'Upper Center': 4, 'Middle Center': 5, 'Lower Center': 6, 'Upper Right': 7, 'Middle Right': 8, 'Lower Right': 9}
    rotation_dict = {'0': 0, '90': 1, '180': 2, '270': 3}
    vis_dict = {'Hidden': 0, 'Hidden-wProperty': 2, 'Visible': 3, 'Visible-wProperty': 4}
    
    def __init__(self):
        self._idx2val = {v:k for k, v in self._idx.items()}
        self._rot_idx2val = {v:k for k, v in self.rotation_dict.items()}
        self._vis_idx2val = {v:k for k, v in self.vis_dict.items()}
        self._just_idx2val = {v:k for k, v in self.just_dict.items()}
        
        self.GFX = None
        self.Font = None
    
    def set_property_from_str(self, line_str, identifier, gfx_str=None, fnt_str=None):
        # Add = sign to identifier if line_str has it, but identifier doesn't so value is assigned correctly
        if '=' in ' '.join(line_str.split()[self._idx['value']:]) and not('=' in identifier):
            identifier += '='
            
        vals = line_str.split()
        
        self.hdr = vals[self._idx['hdr']]
        self.x = int(vals[self._idx['x']])
        self.y = int(vals[self._idx['y']])
        self.size = int(vals[self._idx['size']])
        self.rotation = self._rot_idx2val[int(vals[self._idx['rotation']])]
        self.justification = self._just_idx2val[int(vals[self._idx['justification']])]
        self.visible = self._vis_idx2val[int(vals[self._idx['visible']])]
        self.value = ' '.join(vals[self._idx['value']:])[len(identifier):] # Account for spaces in property value
        self.property = identifier.split('=')[0]
        
        self.set_gfx_from_str(gfx_str)
        self.set_fnt_from_str(fnt_str)
        
    def set_fnt_from_str(self, line_str):
        if not(line_str == None):
            f = Font()
            f.set_font_from_str(line_str)
            self.Font = f
        
    def set_gfx_from_str(self, line_str):
        if not(line_str == None):
            g = GFX()
            g.set_gfx_from_str(line_str)
            self.GFX = g
    
    """
    Set Property class variables via function args
    - hdr [str]: Header in string from symbol file line. Ex: A
    - prop [str]: Property name. Ex: PINTYPE
    - x [float]: x coordinate in mils of property text in symbol
    - y [float]: y coordinate in mils of property text in symbol
    - size [float]: text size of property in mils
    - rot [int or str]: 0, 90, 180, or 270 in degrees
    - just [str]: text justification string from just_dict keys
    - vis [str]: text visibility string from vis_dict keys
    - val: Property value
    """
    def set_property(self, hdr, prop, x, y, size, rot, just, vis, val):
        rot = str(rot) # Rotation can be set as string or int, but must be 0, 90, 180, or 270
        assert rot in self.rotation_dict.keys(), 'Invalid rotation to Property.set_property()'
        assert just in self.just_dict.keys(), 'Invalid justification to Property.set_property()'
        assert vis in self.vis_dict.keys(), 'Invalid visibility to Property.set_property()'
    
        self.hdr = hdr
        self.x = mils_to_units(x)
        self.y = mils_to_units(y)
        self.size = mils_to_units(size)
        self.rotation = rot
        self.justification = just
        self.visible = vis
        self.value = val
        self.property = prop
        
    def get_str(self):
        vals = {0: self.hdr, 
            self._idx['x']: self.x,
            self._idx['y']: self.y,
            self._idx['size']: self.size,
            self._idx['rotation']: self.rotation_dict[self.rotation],
            self._idx['justification']: self.just_dict[self.justification],
            self._idx['visible']: self.vis_dict[self.visible],
            self._idx['value']: self.property+'='+str(self.value)}
            
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
class PinName(Property):
    _idx = {'hdr': 0, 'x': 1, 'y': 2, 'size': 3, 'rotation': 4, 'justification': 5, 'unk': 6, 'visible': 7, 'unk2': 8, 'value': 9} # Line row values to string index
    vis_dict = {'Hidden': 0, 'Visible': 1}
    
    def __init__(self):
        super().__init__()
        
    def set_property_from_str(self, line_str, gfx_str=None, fnt_str=None):
        super().set_property_from_str(line_str, '', gfx_str=gfx_str, fnt_str=fnt_str)
        
    def set_property(self, x, y, size, rot, just, vis, val):
        super().set_property('L', '', x, y, size, rot, just, vis, val)
        
    def get_str(self):
        vals = {self._idx['hdr']: 'L', 
            self._idx['x']: self.x,
            self._idx['y']: self.y,
            self._idx['size']: self.size,
            self._idx['rotation']: self.rotation_dict[self.rotation],
            self._idx['justification']: self.just_dict[self.justification],
            self._idx['visible']: self.vis_dict[self.visible],
            self._idx['value']: str(self.value),
            self._idx['unk']: 0,
            self._idx['unk2']: 0}
            
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
  
class Pin:
    _idx = {'P': 0, 'id': 1, 'x1': 2, 'y1': 3, 'x2': 4, 'y2': 5, 'unk': 6, 'side': 7, 'inverted': 8} # Pin row to string index
    _side_dict = {'Top': 0, 'Bottom': 1, 'Left': 2, 'Right': 3}
    _inv_dict = {False: 0, 'False': 0, 'FALSE': 0, 'Inverted': 1, True: 1, 'True': 1, 'TRUE': 1} # Inverted
    pin_types = ['IN', 'OUT', 'BI', 'TRI', 'OCL', 'OEM', 'POWER', 'GROUND', 'ANALOG']
    active_low_identifiers = ('_N', '#') # I know there are more (not including). I'll leave that to someone else or some other time
    
    def __init__(self):
        self._idx2val = {v:k for k, v in self._idx.items()}
        self._side_idx2val = {v:k for k, v in self._side_dict.items()}
        
        self.GFX = None
        
    def set_pin_from_str(self, line_str, gfx_str=None, fnt_str=None):
        vals = line_str.split()
        
        self.pid = vals[self._idx['id']]
        self.set_line_pos(vals[self._idx['x1']], vals[self._idx['x2']], vals[self._idx['y1']], vals[self._idx['y2']])
        self.side = self._side_idx2val[int(vals[self._idx['side']])]
        self.inverted = bool(int(vals[self._idx['inverted']]))
        
        if not(gfx_str == None):
            g = GFX()
            g.set_graphics_from_str(gfx_str)
            self.GFX = g
    
    def set_pin(self, pid, x1, y1, x2, y2, side, inv, ptype):
        self.pid = pid
        self.set_line_pos(mils_to_units(x1), mils_to_units(x2), mils_to_units(y1), mils_to_units(y2))
        self.side = side
        self.inverted = inv
        self.set_pin_type(ptype)
        
    def set_pin_type_from_str(self, line_str, fnt_str=None):
        ptype = Property()
        ptype.set_property_from_str(line_str, 'PINTYPE=', fnt_str=fnt_str)
        self.Type = ptype
        
    def set_pin_type(self, val):
        assert val in self.pin_types
        p = Property()
        p.set_property('A', 'PINTYPE', 0, 0, 100, 0, 'Middle Left', 'Hidden', val)
        self.Type = p
        
    def set_pin_name_from_str(self, line_str, gfx_str=None, fnt_str=None):
        name = PinName()
        name.set_property_from_str(line_str, gfx_str=gfx_str, fnt_str=fnt_str)
        self.Name = name
        
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
    
    def set_pin_number_from_str(self, line_str):
        num = Property()
        num.set_property_from_str(line_str, '#=')
        self.Number = num
    
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
        vals[self._idx['P']] = 'P'
        vals[self._idx['id']] = self.pid
        vals[self._idx['x1']] = x1
        vals[self._idx['y1']] = y1
        vals[self._idx['x2']] = x2
        vals[self._idx['y2']] = y2
        vals[self._idx['unk']] = 0
        vals[self._idx['side']] = self._side_dict[self.side]
        vals[self._idx['inverted']] = self._inv_dict[self.inverted]
        
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
    def get_str_list(self, name_font='Sans Serif', num_font='Sans Serif', name_color='Dark Blue', num_color='Automatic'):
        str_list = []
        str_list += [self.get_str()]
        
        if not(self.GFX == None):
            str_list += [self.GFX.get_str()]
            
        str_list += [self.Name.get_str()]
        str_list += [Font().set_font(name_font, name_color)]
        if not(self.Name.GFX == None):
            str_list += [self.Name.GFX.get_str()]
        if not(self.Name.Font == None):
            str_list += [self.Name.Font.get_str()]
        
        str_list += [self.get_pintype_str()]
        if not(self.Type.Font == None):
            str_list += [self.Type.Font.get_str()]
        
        str_list += [self.Number.get_str()]
        str_list += [Font().set_font(num_font, num_color)]
        
        return str_list
        
    def get_pintype_str(self): 
        return self.Type.get_str()  
        
    # number: PinNumber Object
    def set_number(self, number):
        self.Number = number
    
    # ptype: PinType Object
    #def set_type(self, ptype):
    #    self.Type = ptype
        
    def set_line_pos(self, x1, x2, y1, y2):
        self.line_pos = (int(x1), int(x2), int(y1), int(y2))
        
    # name: PinName Object
    def set_name(self, name):
        self.Name = name
        
        
class Symbol:
    pins = {}
    sym_headers = ['V','K','|R','Y','U','b'] # All headers of the symbol file. This would exclude pin property headers
    _v_idx = {'value': 1}
    _k_idx = {'name': 2}
    _d_idx = {'date': 1} # Date row indexes
    _u_idx = {'x': 1, 'y': 2, 'size': 3, 'rotation': 4, 'justification': 5, 'visible': 6, 'value': 7}
    _y_idx = {'value': 1}
    _units_dict = {'OneTenthMil': 53, 'Base': 54} # Not exactly sure if this is correct for what the 'V num' property is
    _symtype_to_idx = {'Composite': 0, 'Module': 1, 'Annotate': 3, 'Pin': 4, 'Border': 5}
    _sym_type_dict = {'Composite': 0, 'Module': 1, 'Pin': 2, 'Annotate': 4, 'Border': 5}
    _comp2refdes = {'IC': 'U?', 'Integrated Circuit': 'U?', 'Resistor': 'R?', 'Capacitor': 'C?', 'Inductor': 'L?', 
    'Connector': 'J?', 'Diode': 'D?', 'Test Point': 'TP?', 'Ferrite Bead': 'FB?', 'Transformer': 'T?', 'XFMR': 'T?', 
    'Oscillator': 'Y?', 'LED': 'LD?', 'Transistor': 'Q?', 'Switch': 'SW?'}
    
    def __init__(self, symbol_type='Module'):       
        self._sym_type_idx2val = {v:k for k, v in self._sym_type_dict.items()}
        self._units_idx2val = {v:k for k, v in self._units_dict.items()}
    
        self.units = 'Base'
        self.property_forward_pcb = None
        self.property_place = None
        self.property_pkg_type = None
        self.property_device = None
        self.property_value = None
        self.property_pkg_style = None
        self.property_refdes = None
        self.property_hetero = None
        
        self.__set_defaults()
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
        self.Box = box
        
        # Add refdes above box
        self.set_refdes(units_to_mils(box.x1), units_to_mils(box.y2))
        
        return box
        
    def units_to_mils(self, unit):
        return 100*unit/254000
    
    def parse_sym(self, line_str):
        vals = line_str.split()
        if vals[0] == 'K':
            self.name = vals[self._k_idx['name']]
        elif vals[0] == '|R':
            self.save_date = vals[self._d_idx['date']]
        elif vals[0] == 'Y':
            self.symbol_type = self._sym_type_idx2val[int(vals[self._y_idx['value']])]
        elif vals[0] == 'U':
            self.__set_property_from_str(line_str)
        elif vals[0] == 'b':
            b = Box()
            b.set_box_from_str(line_str)
            b.add_graphics('Blue', 'Hollow', 'Solid', 1) # Temporary. Need to Import graphics from symbol file instead
            self.Box = b
        elif vals[0] == 'V':
            self.units = self._units_idx2val[int(vals[self._v_idx['value']])]
            
    def __set_property_from_str(self, line_str):
        identifier = ''.join(line_str.split()[self._u_idx['value']:]).split('=')[0]
    
        prop = Property()
        prop.set_property_from_str(line_str, identifier)
        
        if prop.property == 'DEVICE':
            self.property_device = prop
        elif prop.property == 'FORWARD_PCB':
            self.property_forward_pcb = prop
        elif prop.property == 'HETERO':
            self.property_hetero = prop
        elif prop.property == 'PKG_STYLE':
            self.property_pkg_style = prop
        elif prop.property == 'PKG_TYPE':
            self.property_pkg_type = prop
        elif prop.property == 'PLACE':
            self.property_place = prop
        elif prop.property == 'REFDES':
            self.property_refdes = prop
        elif prop.property == 'VALUE':
            self.property_value = prop
        elif prop.property == 'NAME_PLACEHOLDER':
            self.property_name_placeholder = prop
        
    
    def set_pin_from_str_list(self, pin_str_list):
        p = Pin()
        
        nxt_hdr = ''
        for i, line_str in enumerate(pin_str_list):
            gfx_str = None
            fnt_str = None
            
            # Get next header
            if i < len(pin_str_list) - 1:
                nxt_hdr = pin_str_list[i+1].split()[0]
            else:
                nxt_hdr = ''
                
            if line_str.startswith('P '):
                if nxt_hdr.startswith('|GRPHSTL'):
                    gfx_str = pin_str_list[i+1]
                p.set_pin_from_str(line_str, gfx_str=gfx_str)
            elif line_str.startswith('L '):
                if nxt_hdr.startswith('|GRPHSTL'):
                    gfx_str = pin_str_list[i+1]
                elif nxt_hdr.startswith('|FNTSTL'):
                    fnt_str = pin_str_list[i+1]
                p.set_pin_name_from_str(line_str, gfx_str=gfx_str, fnt_str=fnt_str)
            elif '#=' in line_str:
                p.set_pin_number_from_str(line_str)
            elif 'PINTYPE=' in line_str:
                if nxt_hdr.startswith('|FNTSTL'):
                    fnt_str = pin_str_list[i+1]
                p.set_pin_type_from_str(line_str, fnt_str=fnt_str)
            
        
        self.pins[p.Number.value] = p
        return p
        
    def __set_defaults(self):        
        self.property_forward_pcb = self.__get_default_property('FORWARD_PCB', 1)
        self.property_place = self.__get_default_property('PLACE', 'YES')
        self.property_pkg_type = self.__get_default_property('PKG_TYPE', 'PKG_TYPE')
        self.property_device = self.__get_default_property('DEVICE', 'DEVICE')
        self.property_value = self.__get_default_property('VALUE', 'VALUE', x=300, y=-200, vis='Visible')
        self.property_pkg_style = self.__get_default_property('PKG_STYLE', 'PKG_STL', x=300, y=-300, vis='Visible')
        
    def set_refdes(self, box_min_x, box_max_y, component='IC', delta_x=100, delta_y=100):
        x = box_min_x + delta_x # Add delta 100mil
        y = box_max_y + delta_y # Add delta 100mil
        refdes = self._comp2refdes[component] # Ex: U? for Integrated Circuit
        self.property_refdes = self.__get_default_property('REFDES', refdes, x=x, y=y, vis='Visible', just='Upper Left')
    
    # Get property object for one of the default symbol properties
    def __get_default_property(self, prop, val, hdr='U', x=0, y=0, size=90, rot=0, just='Middle Left', vis='Hidden'):
        p = Property()
        p.set_property(hdr, prop, x, y, size, rot, just, vis, val)
        return p
  
    """
    - font [Font object]: change default font for symbol properties
    returns: all symbol file's properties as a list of strings
    """
    def _get_property_str_list(self, font=None):
        if font == None:
            font = Font()
            font_str = font.set_font('Sans Serif', 'Automatic')
        else:
            font_str = font.get_str()
            
        properties = {self.property_forward_pcb: 'Forward to PCB', 
        self.property_place: 'Place', 
        self.property_pkg_type: 'Package Type', 
        self.property_device: 'Device', 
        self.property_value: 'Value', 
        self.property_pkg_style: 'Package Style', 
        self.property_refdes: 'Reference Designator', 
        self.property_hetero: 'Hetero'}
            
        str_list = []
        for prop, name in properties.items():   
            if prop != None:
                str_list += [prop.get_str()]
            else:
                print('{} property not set.'.format(name))
        
        str_list_w_fonts = [font_str]*2*len(str_list) # Create list twice the size of str_list filled with font strings
        str_list_w_fonts[::2] = str_list # Interleave the property strings into the font list for every other index
        
        return str_list_w_fonts
    
    # Returns all pin string rows in one concatenated list for the entire symbol
    def _get_pins_str_list(self):
        str_list = []
        for p in self.pins.values():
            str_list += p.get_str_list()
        return str_list
        
    def _get_box_str_list(self):
        return self.Box.get_str_list()
    
    # Some of the header definition is unknown Ex: V, K's int value, F Case, and D
    def _get_header_str_list(self):
        hdr = ['V '+str(self._units_dict[self.units])]
        hdr += ['K 33671749690 new_symbol']
        hdr += ['F Case']
        hdr += ['|R ' + datetime.datetime.now().strftime('%H:%M:%S_%m-%d-%y')]
        hdr += ['|BORDERTYPESUPPORT']
        hdr += ['Y ' + str(self._symtype_to_idx[self.symbol_type])]
        hdr += ['D 0 0 2540000 2540000', 'Z 10', 'i 3', '|I 6']
        return hdr
    
    def _get_footer_str_list(self):
        return ['E']
        
    # returns a list of all text necessary to recreate a symbol file
    # this includes header, symbol properties, pins, fonts, graphics, and symbol box
    def get_symbol_str_list(self):
        str_list = []
        str_list += self._get_header_str_list()
        str_list += self._get_pins_str_list()
        str_list += self._get_box_str_list()
        str_list += self._get_property_str_list()
        str_list += self._get_footer_str_list()
        
        return str_list
        