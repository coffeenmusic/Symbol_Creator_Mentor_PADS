import random

class ObjectType:    
    """
    obj_dict: human readable key to the symbol object type's index
    """
    def __init__(self, obj_dict):
        self.idx2val = {v:k for k, v in obj_dict.items()}
        
        # identifier: single letter identifier of object type. 
        #    Valid Identifiers - V, K, Y, D, Z, i, L, U, A, Q, T, b, l, a, c, E
        self.identifier = self.idx2val[0]
        self.idx = obj_dict
        
        field = {}
        for k in obj_dict.keys():
            field[k] = {}
        self.field = field
        self.field_idx2val = {}
        
    def _add_field(self, name, field_dict):
        self.field[name] = field_dict
        self.field_idx2val[name] = {v:k for k, v in field_dict.items()}
    
    """ 
    Example:
    L x y size rotation justification locality visible inverted value
    L ?? ?? ?? 4 1 1 1 1 ??
    """
    def print_example(self):
        desc = self.identifier
        example = self.identifier
        for i in range(1, len(self.field.values())):
            # Description
            desc += ' ' + str(self.idx2val[i])
            
            # Example
            ex_values = list(self.field[self.idx2val[i]].values())
            if len(ex_values) > 0:
                rand_value = random.randrange(len(ex_values))
                example += ' ' + str(ex_values[rand_value])
            else:
                example += ' ??'
        print('Format: \t' + desc)
        print('Example:\t' + example)
        
class Fields:
    case = {'Case': 0} # Only option for case preservation

    color = {'Black': 0, 'Blue': 1, 'Green': 2, 'Cyan': 3, 'Red': 4, 'Magenta': 5, 'Brown': 6, 'Light Gray': 7, 'Gray': 8, 'Light Blue': 9, 'Light Green': 10, 'Light Cyan': 11, 'Light Red': 12, 'Light Magenta': 13, 'Yellow': 14, 'White': 15}

    fill_style = {'Automatic': -1, 'Hollow': 0, 'Solid': 1, 'Grey92': 2, 'Grey50': 4, 'Grey08': 6, 'Grey04': 7, 'Diagdn2': 8, 'Diagdn1': 11, 'Diagup2': 13, 'Diagup1': 16, 'Horiz': 19, 'Vert': 21, 'Grid2': 22, 'Grid1': 23, 'X2': 24, 'X1': 25}
    fill_style2 = {'Automatic': -1, 'Hollow': 0, 'Solid': 1, 'Diagdn1': 2, 'Diagup2': 3, 'Grey08': 4, 'Diagdn2': 5, 'Diagup1': 6, 'Horiz': 7, 'Vert': 8, 'Grid2': 9, 'Grid1': 10, 'X2': 11, 'X1': 12, 'Grey50': 13, 'Grey92': 14, 'Grey04': 15}

    font = {'Fixed': 0, 'Roman': 1, 'Roman Italic': 2, 'Roman Bold': 3, 'Roman Bold Italic': 4, 'Sans Serif': 5, 'Script': 6, 'Sans Serif Bold': 7, 'Script Bold': 8, 'Gothic': 9, 'Old English': 10, 'Kanji': 11, 'Plot': 12, 'Custom Style': 13  }

    inverted = {'Not Inverted': 0, 'Inverted': 1}

    justification = {'Upper Left': 1, 'Middle Left': 2, 'Lower Left': 3, 'Upper Center': 4, 'Middle Center': 5, 'Lower Center': 6, 'Upper Right': 7, 'Middle Right': 8, 'Lower Right': 9}

    label_visible = {'Hidden': 0, 'Visible': 1, 'Hatch': 3}

    locality = {'Local': 0, 'Global': 1}

    line_width = {'Automatic': -1, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10}

    line_style = {'Automatic': -1, 'Solid': 0, 'Dash': 1, 'Center': 2, 'Phantom': 3, 'Big Dash': 4, 'Dot': 5, 'Dash-Dot': 6, 'Medium Dash': 7}

    rotation = {'0': 0, '90': 1, '180': 2, '270': 3, 
                     'MirrorH': 4,    # Mirror Horizontal Rotate 0 degrees
                     '90MirrorH': 5,  # Mirror Horizontal Rotate 90 degrees 
                     '180MirrorH': 6, # Mirror Horizontal Rotate 180 degrees (Mirror Vertical)
                     '270MirrorH': 7} # Mirror Horizontal Rotate 270 degrees

    sheet_size = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'A4': 5, 'A3': 6, 'A2': 7, 'A1': 8, 'A0': 9, 'User': 10}

    side = {'Top': 0, 'Bottom': 1, 'Left': 2, 'Right': 3} # Symbol Pin's Side

    symbol_type = {'Composite': 0, 'Module': 1, 'Annotate': 3, 'Pin': 4, 'Border': 5}

    # Version: 50 means version 5.0
    version = {'Original': 50, 
                    'ViewDraw8': 51, 
                    'HighPrecision-OneTenthMil': 53, # 5.3 or higher required if F Case is used (Case preservation)
                    'HighPrecision-Metric': 54}

    visible = {'None': 0,       # All values Hidden
                    'Name&Value': 1, # Attribute Name Visible and Attribute Value Visible. Example: #=28
                    'Name': 2,       # Attribute Name Visible. Example: #=
                    'Value': 3}      # Attribute Value Visible. Example: 28
    
    def __init__(self):
        self.i_case = {v:k for k, v in self.case.items()}
        self.i_color = {v:k for k, v in self.color.items()}
        self.i_fill_style = {v:k for k, v in self.fill_style.items()}
        self.i_fill_style2 = {v:k for k, v in self.fill_style2.items()}
        self.i_font = {v:k for k, v in self.font.items()}
        self.i_inverted = {v:k for k, v in self.inverted.items()}
        self.i_justification = {v:k for k, v in self.justification.items()}
        self.i_label_visible = {v:k for k, v in self.label_visible.items()}
        self.i_locality = {v:k for k, v in self.locality.items()}
        self.i_line_width = {v:k for k, v in self.line_width.items()}
        self.i_line_style = {v:k for k, v in self.line_style.items()}
        self.i_rotation = {v:k for k, v in self.rotation.items()}
        self.i_sheet_size = {v:k for k, v in self.sheet_size.items()}
        self.i_side = {v:k for k, v in self.side.items()}
        self.i_symbol_type = {v:k for k, v in self.symbol_type.items()}
        self.i_version = {v:k for k, v in self.version.items()}
        self.i_visible = {v:k for k, v in self.visible.items()}
        
class SymbolFormat(Fields):                
    objects = {}
    
    def add_obj(self, obj):
        self.objects[obj.identifier] = obj
        
    def get_identifier_list(self):
        return list(self.objects.keys())
        
    def print_examples(self):
        for obj in self.objects.values():
            obj.print_example()
            print()
        
sf = SymbolFormat()


"""
Object Type Definitions ---------------------------------------------------------------------------------------
"""
# V - Version
#     Must be first line of the sybmol
v_obj = ObjectType({'V': 0, 'version': 1})
v_obj._add_field('version', sf.version)
sf.add_obj(v_obj)

# K - License
#     Must be second line of the symbol
k_obj = ObjectType({'K': 0, 
                    'magic-number': 1,    # Created from ViewLogic license and File Name
                    'original-name': 2})  # Name of the symbol when it was originally created
sf.add_obj(k_obj)

# F - Case Preservation
f_obj = ObjectType({'F': 0, 'case': 1})
sf.add_obj(f_obj)

# |R - TimeStamp
r_obj = ObjectType({'|R': 0, 'timestamp': 1}) # hour:minute_month-day-year
sf.add_obj(r_obj)

# |BORDERTYPESUPPORT - ??

# Y - Item Type
y_obj = ObjectType({'Y': 0, 'symbol-type': 1})
y_obj._add_field('symbol-type', sf.symbol_type)
sf.add_obj(y_obj)

# D - Symbol Block Size
d_obj = ObjectType({'D': 0, 'xmin': 1, 'ymin': 2, 'xmax': 3, 'ymax': 4})
sf.add_obj(d_obj)

# Z - Sheet Size
z_obj = ObjectType({'Z': 0, 'sheet-size': 1})
z_obj._add_field('sheet-size', sf.sheet_size)
sf.add_obj(z_obj)

# i - Object Counter
i_obj = ObjectType({'i': 0, 'max': 1}) # Maximum used object number
sf.add_obj(i_obj)

# L - Label
#     Label for the previous pin line item
l_obj = ObjectType({'L': 0, 'x': 1, 'y': 2, 'size': 3, 'rotation': 4, 'justification': 5, 'locality': 6, 'visible': 7, 'inverted': 8, 'value': 9})
l_obj._add_field('rotation', sf.rotation)
l_obj._add_field('justification', sf.justification)
l_obj._add_field('locality', sf.locality)
l_obj._add_field('visible', sf.label_visible)
l_obj._add_field('inverted', sf.inverted)
sf.add_obj(l_obj)

# U - Unattached Attribute
#     Symbol or schematic attribute. Independent Attribute.
u_obj = ObjectType({'U': 0, 'x': 1, 'y': 2, 'size': 3, 'rotation': 4, 'justification': 5, 'visible': 6, 
                    'value': 7}) # Name(=Value)
u_obj._add_field('rotation', sf.rotation)
u_obj._add_field('justification', sf.justification)
u_obj._add_field('visible', sf.visible)
sf.add_obj(u_obj)

# A - Attached Attribute
#     Line follows the line it belongs to. (Follows pin). Dependent Attribute
a_obj = ObjectType({'A': 0, 'x': 1, 'y': 2, 'size': 3, 'rotation': 4, 'justification': 5, 'visible': 6, 
                    'value': 7}) # Name(=Value)
a_obj._add_field('rotation', sf.rotation)
a_obj._add_field('justification', sf.justification)
a_obj._add_field('visible', sf.visible)
sf.add_obj(a_obj)

# P - Pin
p_obj = ObjectType({'P': 0, 'id': 1, # Unique ID. Starts at 1 and less than max object count
                    'x-net': 2, # x net/trace node side
                    'y-net': 3, # y net/trace node side
                    'x-sym': 4, # x symbol side (invert NOT bubble side)
                    'y-sym': 5, # y symbol side (invert NOT bubble side)
                    'unk': 6, 'side': 7, 'inverted': 8})
p_obj._add_field('side', sf.side)
p_obj._add_field('inverted', sf.inverted)
sf.add_obj(p_obj)

# |FNTSTL - Font Style
fnt_obj = ObjectType({'|FNTSTL': 0, 'color': 1, # 24bit integer (0-255 per channel). red << 16 | green << 8 | blue. -1 = Auto
                      'style': 2})
fnt_obj._add_field('style', sf.font)
sf.add_obj(fnt_obj)

# |GRPHSTL - Graphics Style
gfx_obj = ObjectType({'|GRPHSTL': 0, 'color': 1, # 24bit integer (0-255 per channel). red << 16 | green << 8 | blue. -1 = Auto
                      'fill-color': 2, # 24bit integer (0-255 per channel). red << 16 | green << 8 | blue. -1 = Auto
                      'line-style': 3, # Solid, Dash, Dot, etc.
                      'line-width': 4}) # 1-10, -1=Automatic
gfx_obj._add_field('line-style', sf.line_style)
gfx_obj._add_field('line-width', sf.line_width)
sf.add_obj(gfx_obj)

# |GRPHSTL_EXT01 - Graphics Style Extension 1
gfx_ex1_obj = ObjectType({'|GRPHSTL_EXT01': 0, 'color': 1, 'fill-color': 2, 'fill-style': 3, 'line-style': 4, 'line-width': 5})
gfx_ex1_obj._add_field('line-style', sf.line_style)
gfx_ex1_obj._add_field('line-width', sf.line_width)
sf.add_obj(gfx_ex1_obj)

# Q - Font, Color, Style
q_obj = ObjectType({'Q': 0, 'color': 1, 'fill-style': 2, 'line-style': 3})
q_obj._add_field('color', sf.color)
q_obj._add_field('fill-style', sf.fill_style)
q_obj._add_field('line-style', sf.line_style)
sf.add_obj(q_obj)

# T - Text

# b - Box
b_obj = ObjectType({'b': 0, 'x1': 1, 'y1': 2, 'x2': 3, 'y2': 4})
sf.add_obj(b_obj)

# l - Line/Polyline
pl_obj = ObjectType({'l': 0, 'count': 1, # number of x/y endpoint coordinates . Always >= 2.
                     'x1': 2, 'y1': 3, 'x2': 4, 'y2': 5}) # 'x3': 6, 'y3': 7, ..., 'xn': count*2, 'yn': count*2 + 1})
sf.add_obj(pl_obj)


# a - Arc

# c - Circle

# E - End
e_obj = ObjectType({'E': 0}) # End of File
sf.add_obj(e_obj)