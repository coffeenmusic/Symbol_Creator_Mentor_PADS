import datetime
from sym_format import SymbolFormat

sf = SymbolFormat()
    
def mils_to_units(mils):
    return int((mils/100)*254000)
    
def units_to_mils(units):
    return (units/254000)*100
    
class PolyLine:
    def __init__(self):
        self.idx = sf.l().copy()
        self.idx['coord_start'] = 2
        
        self.Font = None
        self.count = 0
        self.coords = {}
    
    """
    Get string for symbol file's line
    Build string from class attributes
    """
    def get_str(self):
        vals = {}
        vals[sf.l['l']] = 'l'
        vals[sf.l['count']] = self.count
        
        cs = self.idx['coord_start']
        for i, coord in enumerate(self.coords.values(), int(cs/2)):
            x = coord['x']
            y = coord['y']
            vals[i*2] = x
            vals[i*2 + 1] = y
            
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
    def set_polyline_from_str(self, line_str, fnt_str=None):
        vals = line_str.split()
        
        assert vals[0] == 'l', 'Incorrect header for polyline: ' + line_str
        
        count = int(vals[self.idx['count']])
        cs = self.idx['coord_start'] # idx where first x coordinate starts
        
        for i in range(cs, (cs+count-1)*2, 2):
            x = int(vals[i])
            y = int(vals[i+1])
            self.add_coord(x, y)
            
        self.count = count
        
        self.add_font(fnt_str)
        
    def add_font(self, fnt_str):
        if not(fnt_str == None):
            f = Font()
            f.set_font_from_str(fnt_str)
            self.Font = f
        
    def add_coord(self, x, y):
        self.coords[self.count] = {'x': x, 'y': y}
        self.count += 1
        

class Box:            
    def set_box_from_str(self, line_str):
        vals = line_str.split()
        self.x1 = vals[sf.b['x1']]
        self.x2 = vals[sf.b['x2']]
        self.y1 = vals[sf.b['y1']]
        self.y2 = vals[sf.b['y2']]
        
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
        vals[sf.b['b']] = 'b'
        vals[sf.b['x1']] = self.x1
        vals[sf.b['y1']] = self.y1
        vals[sf.b['x2']] = self.x2
        vals[sf.b['y2']] = self.y2
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
    def get_str_list(self):
        str_list = [self.get_str()]
        str_list += [self.gfx.get_str()]
        return str_list
        
class Color:                
    color_dict = {'Automatic': (-1,-1,-1), 'Red': (255,0,0), 'Dark Blue': (0,0,132), 'Blue': (0,0,255)}
    
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
    def __init__(self):
        self.idx = sf.GRPHSTL()
        self.idx_gfx01 = sf.GRPHSTL_EXT01()
        self.fill_style_idx = sf.GRPHSTL_EXT01.fill_style()
        self.line_style_idx = sf.GRPHSTL.line_style()
        
        self.idx2val = {v:k for k, v in self.idx.items()}
        self.idx2val_gfx01 = {v:k for k, v in self.idx_gfx01.items()}
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
        if hdr == self.idx2val_gfx01[0]:
            idx = self.idx_gfx01
            self.fill_style = self.fillstyle_idx2val[int(vals[idx['fill_style']])]
        
        self.header = hdr
        
        c = Color()
        c.set_color_int(vals[idx['color_value']])   
        self.Color = c
        
        c_fill = Color()
        c_fill.set_color_int(vals[idx['fill_color']])            
        self.Fill_Color = c_fill
        
        self.line_style = self.linestyle_idx2val[int(vals[idx['line_style']])]
        self.line_width = int(vals[idx['line_width']])
        
    # Create string of format: '|GRPHSTL_EXT01 color fill-color fill-style line-style line-width' or '|GRPHSTL color fill-color line-style line-width'
    def get_str(self):
        vals = {}
        
        idx = self.idx
        if self.header == self.idx2val_gfx01[0]:
            idx = self.idx_gfx01
            vals[idx['fill_style']] = self.fill_style_idx[self.fill_style]
            
        vals[0] = self.header
        vals[idx['color_value']] = self.Color.color_int
        vals[idx['fill_color']] = self.Fill_Color.color_int
        vals[idx['line_style']] = self.line_style_idx[self.line_style]
        vals[idx['line_width']] = self.line_width
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
class Font:         
    """
    - font [str]: font string that is one of the Keys from font_dict
    - color [str]: color string that is one of the Keys from color_dict
    returns: string in Mentor symbol file format
    """
    def set_font(self, font, color_str):
        c = Color()
        c.set_color(color_str)
        
        self.Color = c
        self.font = font
        return self.get_str()
        
    def set_font_from_str(self, line_str):
        vals = line_str.split()
        
        c = Color()
        c.set_color_int(vals[sf.FNTSTL['color_value']])
        self.Color = c
        
        self.font = sf.FNTSTL.font[int(vals[sf.FNTSTL['font']])]
        
    def get_str(self):
        vals = {}
        vals[0] = sf.FNTSTL[0]
        vals[sf.FNTSTL['color_value']] = self.Color.color_int
        vals[sf.FNTSTL['font']] = sf.FNTSTL.font[self.font]
        return ' '.join([str(vals[i]) for i in range(len(vals))])

"""
    A: Attribute object type. 7 fields
    A x y size rotation justification visible value
"""        
class Attribute:    
    def __init__(self):
        self.GFX = None
        self.Font = None
    
    def set_attribute_from_str(self, line_str, identifier, gfx_str=None, fnt_str=None):
        # Add = sign to identifier if line_str has it, but identifier doesn't so value is assigned correctly
        if '=' in ' '.join(line_str.split()[sf.A['value']:]) and not('=' in identifier):
            identifier += '='
            
        vals = line_str.split()
        
        self.hdr = vals[sf.A['A']]
        self.x = int(vals[sf.A['x']])
        self.y = int(vals[sf.A['y']])
        self.size = int(vals[sf.A['size']])
        self.rotation = sf.A.rotation[int(vals[sf.A['rotation']])]
        self.justification = sf.A.justification[int(vals[sf.A['justification']])]
        self.visible = sf.A.visible[int(vals[sf.A['visible']])]
        self.value = ' '.join(vals[sf.A['value']:])[len(identifier):] # Account for spaces in property value
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
    - rot [int or str]: 0, 90, 180, 270, MirrorH, Mirror90, Mirror180, or MirrorH270 in degrees
    - just [str]: text justification string from sf.A.justification keys
    - vis [str]: text visibility string from sf.A.visible keys
    - val: Property value
    """
    def set_property(self, hdr, prop, x, y, size, rot, just, vis, val):
        if type(rot) == int: # 0, 90, 180, & 270 should be Rotate0, Rotate90, Rotate180, & Rotate270 strings
            rot = 'Rotate'+str(rot)
        elif type(rot) == str:
            if rot.isnumeric():
                rot = 'Rotate{}'.format(rot)
                
        assert rot in sf.A.rotation().keys(), 'Invalid rotation to Property.set_property()'
        assert just in sf.A.justification().keys(), 'Invalid justification to Property.set_property()'
        if hdr == 'A':
            assert vis in sf.A.visible().keys(), 'Invalid visibility to Property.set_property()'
        if hdr == 'L':
            assert vis in sf.L.label_visible().keys(), 'Invalid visibility to Property.set_property()'
    
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
            sf.A['x']: self.x,
            sf.A['y']: self.y,
            sf.A['size']: self.size,
            sf.A['rotation']: sf.A.rotation[self.rotation],
            sf.A['justification']: sf.A.justification[self.justification],
            sf.A['visible']: sf.A.visible[self.visible],
            sf.A['value']: self.property+'='+str(self.value)}
            
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
class PinName(Attribute):    
    def __init__(self):
        super().__init__()
        
    def set_attribute_from_str(self, line_str, gfx_str=None, fnt_str=None):
        super().set_attribute_from_str(line_str, '', gfx_str=gfx_str, fnt_str=fnt_str)
        
        vals = line_str.split()       
        self.visible = sf.L.label_visible[int(vals[sf.L['label_visible']])]
        self.value = vals[sf.L['value']]
        self.property = None
        
    def set_property(self, x, y, size, rot, just, vis, val):
        super().set_property('L', '', x, y, size, rot, just, vis, val)
        
    def get_str(self):
        vals = {sf.L['L']: 'L', 
            sf.L['x']: self.x,
            sf.L['y']: self.y,
            sf.L['size']: self.size,
            sf.L['rotation']: sf.L.rotation[self.rotation],
            sf.L['justification']: sf.L.justification[self.justification],
            sf.L['locality']: sf.L.locality['Local'],
            sf.L['label_visible']: sf.L.label_visible[self.visible],
            sf.L['inverted']: sf.L.inverted['Not Inverted'],
            sf.L['value']: str(self.value)}
            
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
  
class Pin:
    pin_types = ['IN', 'OUT', 'BI', 'TRI', 'OCL', 'OEM', 'POWER', 'GROUND', 'ANALOG', 'TERMINAL']
    active_low_id_end = ('_N', '#') # Identifies an active low pin name if it ends with these. I know there are more (not including). I'll leave that to someone else or some other time
    active_low_id_start = ('-') # Identifies an active low pin name if it starts with these. 
    
    def __init__(self):
        self._inv_dict = sf.P.inverted() # Inverted
        self._inv_dict.update({False: 0, 'False': 0, 'FALSE': 0, True: 1, 'True': 1, 'TRUE': 1})
        
        self.GFX = None
        
    def set_pin_from_str(self, line_str, gfx_str=None, fnt_str=None):
        vals = line_str.split()
        
        self.pid = vals[sf.P['id']]
        self.set_line_pos(vals[sf.P['x_net']], vals[sf.P['x_sym']], vals[sf.P['y_net']], vals[sf.P['y_sym']])
        self.side = sf.P.side[int(vals[sf.P['side']])]
        self.inverted = bool(int(vals[sf.P['inverted']]))
        
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
        ptype = Attribute()
        ptype.set_attribute_from_str(line_str, 'PINTYPE=', fnt_str=fnt_str)
        self.Type = ptype
        
    def set_pin_type(self, val):
        assert val in self.pin_types, 'Value passed: ' + str(val)
        a = Attribute()
        a.set_property('A', 'PINTYPE', 0, 0, 100, 0, 'Middle Left', 'None', val)
        self.Type = a
        
    def set_pin_name_from_str(self, line_str, gfx_str=None, fnt_str=None):
        name = PinName()
        name.set_attribute_from_str(line_str, gfx_str=gfx_str, fnt_str=fnt_str)
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
        num = Attribute()
        num.set_attribute_from_str(line_str, '#=')
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
        
        num = Attribute()
        num.set_property('A', '#', num_x, num_y, 100, 0, num_just, 'Value', val)
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
    
    # Gets string for pin row. Ex: 'P 364 0 5588000 762000 5588000 0 2 1'
    def get_str(self):
        x1, x2, y1, y2 = self.line_pos
        vals = {}        
        vals[sf.P['P']] = 'P'
        vals[sf.P['id']] = self.pid
        vals[sf.P['x_net']] = x1
        vals[sf.P['y_net']] = y1
        vals[sf.P['x_sym']] = x2
        vals[sf.P['y_sym']] = y2
        vals[sf.P['unknown']] = 0
        vals[sf.P['side']] = sf.P.side[self.side]
        vals[sf.P['inverted']] = self._inv_dict[self.inverted]
        
        return ' '.join([str(vals[i]) for i in range(len(vals))])
        
    def get_str_list(self, name_font='Sans Serif', num_font='Sans Serif', name_color='Dark Blue', num_color='Automatic'):
        str_list = []
        
        # Pin
        str_list += [self.get_str()]
        if not(self.GFX == None):
            str_list += [self.GFX.get_str()]
         
        # Pin Name
        str_list += [self.Name.get_str()]
        if not(self.Name.GFX == None):
            str_list += [self.Name.GFX.get_str()]
        if not(self.Name.Font == None):
            str_list += [self.Name.Font.get_str()]
        else:
            str_list += [Font().set_font(name_font, name_color)]
        
        # Pin Type
        str_list += [self.get_pintype_str()]
        if not(self.Type.Font == None):
            str_list += [self.Type.Font.get_str()]
        
        # Pin Number
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
    sym_headers = ['V','K','D','F','i','|R','Y','Z','U','b','l'] # All headers of the symbol file. This would exclude pin property headers
    _comp2refdes = {'IC': 'U?', 'Integrated Circuit': 'U?', 'Resistor': 'R?', 'Capacitor': 'C?', 'Inductor': 'L?', 
    'Connector': 'J?', 'Diode': 'D?', 'Test Point': 'TP?', 'Ferrite Bead': 'FB?', 'Transformer': 'T?', 'XFMR': 'T?', 
    'Oscillator': 'Y?', 'LED': 'LD?', 'Transistor': 'Q?', 'Switch': 'SW?'}
    
    def __init__(self, symbol_type='Module', version='HighPrecision-Metric'):           
        self.version = version
        self.lines = []
        self.Box = None
        self.pins = {}
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
            self.name = vals[sf.K['original_name']]
        elif vals[0] == '|R':
            self.save_date = vals[sf.R['timestamp']]
        elif vals[0] == 'Y':
            self.symbol_type = sf.Y.symbol_type[int(vals[sf.Y['symbol_type']])]
        elif vals[0] == 'U':
            self.__set_property_from_str(line_str)
        elif vals[0] == 'b':
            b = Box()
            b.set_box_from_str(line_str)
            b.add_graphics('Blue', 'Hollow', 'Solid', 1) # Temporary. Need to Import graphics from symbol file instead
            self.Box = b
        elif vals[0] == 'V':
            self.version = sf.V.version[int(vals[sf.V['version']])]
        elif vals[0] == 'l':
            l = PolyLine()
            l.set_polyline_from_str(line_str)
            self.lines += [l]               
            
    def __set_property_from_str(self, line_str):
        identifier = ''.join(line_str.split()[sf.U['value']:]).split('=')[0]
    
        attr = Attribute()
        attr.set_attribute_from_str(line_str, identifier)
        
        if attr.property == 'DEVICE':
            self.property_device = attr
        elif attr.property == 'FORWARD_PCB':
            self.property_forward_pcb = attr
        elif attr.property == 'HETERO':
            self.property_hetero = attr
        elif attr.property == 'PKG_STYLE':
            self.property_pkg_style = attr
        elif attr.property == 'PKG_TYPE':
            self.property_pkg_type = attr
        elif attr.property == 'PLACE':
            self.property_place = attr
        elif attr.property == 'REFDES':
            self.property_refdes = attr
        elif attr.property == 'VALUE':
            self.property_value = attr
        elif attr.property == 'NAME_PLACEHOLDER':
            self.property_name_placeholder = attr
        
    
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
            
        assert hasattr(p, 'Number'), "This symbol can't be imported. The symbol being imported does not have a pin number for the following:\n{}".format('\n'.join(pin_str_list))
        self.pins[p.Number.value] = p
        return p
        
    def __set_defaults(self):        
        self.property_forward_pcb = self.__get_default_property('FORWARD_PCB', 1)
        self.property_place = self.__get_default_property('PLACE', 'YES')
        self.property_pkg_type = self.__get_default_property('PKG_TYPE', 'PKG_TYPE')
        self.property_device = self.__get_default_property('DEVICE', 'DEVICE')
        self.property_value = self.__get_default_property('VALUE', 'VALUE', x=300, y=-200, vis='Value')
        self.property_pkg_style = self.__get_default_property('PKG_STYLE', 'PKG_STL', x=300, y=-300, vis='Value')
        
    def set_refdes(self, box_min_x, box_max_y, component='IC', delta_x=100, delta_y=100):
        x = box_min_x + delta_x # Add delta 100mil
        y = box_max_y + delta_y # Add delta 100mil
        refdes = self._comp2refdes[component] # Ex: U? for Integrated Circuit
        self.property_refdes = self.__get_default_property('REFDES', refdes, x=x, y=y, vis='Value', just='Upper Left')
    
    # Get property object for one of the default symbol properties
    def __get_default_property(self, attr, val, hdr='U', x=0, y=0, size=90, rot=0, just='Middle Left', vis='None'):
        a = Attribute()
        a.set_property(hdr, attr, x, y, size, rot, just, vis, val)
        return a
  
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
        if self.Box == None:
            return []
        else:
            return self.Box.get_str_list()
            
    def _get_polyline_str_list(self):
        str_list = []
        for l in self.lines:
            str_list += [l.get_str()]
        return str_list        
    
    """
        V: Version # [Must be the first line of the symbol]
        K: License MagicNumber Name
        F: Case Preservation
        |R: Datetime Comment
        Y: SymbolType
        D: Size x_min y_min x_max y_max
        Z: SheetSize
        i: MaxObject
    Notes: 
        | at the start of a line means it is a comment line
    """
    def _get_header_str_list(self):
        hdr = ['V '+str(sf.V.version[self.version])] # V [Version]
        hdr += ['K 33671749690 ' + self.name]
        hdr += ['F Case']
        hdr += ['|R ' + datetime.datetime.now().strftime('%H:%M:%S_%m-%d-%y')]
        hdr += ['Y ' + str(sf.Y.symbol_type[self.symbol_type])]
        hdr += ['D 0 0 2540000 2540000', 'Z 10', 'i 3']
        return hdr
    
    def _get_footer_str_list(self):
        return ['E'] # End
        
    # returns a list of all text necessary to recreate a symbol file
    # this includes header, symbol properties, pins, fonts, graphics, and symbol box
    def get_symbol_str_list(self):
        str_list = []
        str_list += self._get_header_str_list()
        str_list += self._get_pins_str_list()
        str_list += self._get_polyline_str_list()
        str_list += self._get_box_str_list()
        str_list += self._get_property_str_list()
        str_list += self._get_footer_str_list()
        
        return str_list
        