class FieldFormats:
    case = {'Case': 0} # Only option for case preservation

    color = {'Black': 0, 'Blue': 1, 'Green': 2, 'Cyan': 3, 'Red': 4, 'Magenta': 5, 'Brown': 6, 'Light Gray': 7, 'Gray': 8, 'Light Blue': 9, 'Light Green': 10, 'Light Cyan': 11, 'Light Red': 12, 'Light Magenta': 13, 'Yellow': 14, 'White': 15}

    fill_style = {'Automatic': -1, 'Hollow': 0, 'Solid': 1, 'Grey92': 2, 'Grey50': 4, 'Grey08': 6, 'Grey04': 7, 'Diagdn2': 8, 'Diagdn1': 11, 'Diagup2': 13, 'Diagup1': 16, 'Horiz': 19, 'Vert': 21, 'Grid2': 22, 'Grid1': 23, 'X2': 24, 'X1': 25}

    font = {'Fixed': 0, 'Roman': 1, 'Roman Italic': 2, 'Roman Bold': 3, 'Roman Bold Italic': 4, 'Sans Serif': 5, 'Script': 6, 'Sans Serif Bold': 7, 'Script Bold': 8, 'Gothic': 9, 'Old English': 10, 'Kanji': 11, 'Plot': 12, 'Custom Style': 13  }

    inverted = {'Not Inverted': 0, 'Inverted': 1}

    justification = {'Upper Left': 1, 'Middle Left': 2, 'Lower Left': 3, 'Upper Center': 4, 'Middle Center': 5, 'Lower Center': 6, 'Upper Right': 7, 'Middle Right': 8, 'Lower Right': 9}

    label_visible = {'Hidden': 0, 'Visible': 1, 'Hatch': 3}

    locality = {'Local': 0, 'Global': 1}

    line_width = {'Automatic': -1, 'w1': 1, 'w2': 2, 'w3': 3, 'w4': 4, 'w5': 5, 'w6': 6, 'w7': 7, 'w8': 8, 'w9': 9, 'w10': 10}

    line_style = {'Automatic': -1, 'Solid': 0, 'Dash': 1, 'Center': 2, 'Phantom': 3, 'Big Dash': 4, 'Dot': 5, 'Dash-Dot': 6, 'Medium Dash': 7}

    rotation = {'Rotate0': 0, 'Rotate90': 1, 'Rotate180': 2, 'Rotate270': 3, 
                         'MirrorH': 4,    # Mirror Horizontal Rotate 0 degrees
                         'MirrorH90': 5,  # Mirror Horizontal Rotate 90 degrees 
                         'MirrorH180': 6, # Mirror Horizontal Rotate 180 degrees (Mirror Vertical)
                         'MirrorH270': 7} # Mirror Horizontal Rotate 270 degrees

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
                    
class ObjectFormats:
    """
    First 2 Header Objects -----------------------------------------------------------------------------
    """
    # V - Version
    #     Must be first line of the symbol
    V = {'V': 0, 'version': 1} # See version FieldFormat for more info
    
    # K - License
    #     Must be second line of the symbol
    K = {'K': 0, 'magic_number': 1,    # Created from ViewLogic license and File Name
         'original_name': 2}  # Name of the symbol when it was originally created
         
    """
    Header Objects -------------------------------------------------------------------------------------
    """     
    # |BORDERTYPESUPPORT - ??
    # TODO: Add
    
    # D - Symbol Block Size
    D = {'D': 0, 'xmin': 1, 'ymin': 2, 'xmax': 3, 'ymax': 4}
    
    # F - Case Preservation
    F = {'F': 0, 'case': 1}
    
    # i - Object Counter
    i = {'i': 0, 'max': 1} # Maximum used object number
    
    # |R - TimeStamp
    R = {'|R': 0, 'timestamp': 1}
    
    # Y - Symbol Type
    Y = {'Y': 0, 'symbol_type': 1}    
    
    # Z - Sheet Size
    Z = {'Z': 0, 'sheet_size': 1}
    
    """
    Other Objects
    """
    # a - Arc
    # TODO: add
    
    # b - Box
    b = {'b': 0, 'x1': 1, 'y1': 2, 'x2': 3, 'y2': 4}
    
    # c - Circle
    # TODO: add

    # |FNTSTL - Font Style
    FNTSTL = {'|FNTSTL': 0, 'color_value': 1, # 24bit integer (0-255 per channel). red << 16 | green << 8 | blue. -1 = Auto
              'font': 2}
              
    # |GRPHSTL - Graphics Style
    GRPHSTL = {'|GRPHSTL': 0, 'color_value': 1, # 24bit integer (0-255 per channel). red << 16 | green << 8 | blue. -1 = Auto
                      'fill_color': 2, # 24bit integer (0-255 per channel). red << 16 | green << 8 | blue. -1 = Auto
                      'line_style': 3, # Solid, Dash, Dot, etc.
                      'line_width': 4} # 1-10, -1=Automatic
                      
    # |GRPHSTL_EXT01 - Graphics Style Extension 1
    GRPHSTL_EXT01 = {'|GRPHSTL_EXT01': 0, 'color_value': 1, 'fill_color': 2, 'fill_style': 3, 'line_style': 4, 'line_width': 5}
    
    # l - Line/Polyline
    l = {'l': 0, 'count': 1, # number of x/y endpoint coordinates . Always >= 2.
         'x1': 2, 'y1': 3, 'x2': 4, 'y2': 5} # 'x3': 6, 'y3': 7, ..., 'xn': count*2, 'yn': count*2 + 1})
    
    # Q - Font, Color, Style
    Q = {'Q': 0, 'color': 1, 'fill_style': 2, 'line_style': 3}
    
    # T - Text
    # TODO: Add
    
    # U - Unattached Attribute
    #     Symbol or schematic attribute. Independent Attribute.
    U = {'U': 0, 'x': 1, 'y': 2, 'size': 3, 'rotation': 4, 'justification': 5, 'visible': 6, 'value': 7} # Name(=Value)
    
    
    """
    Pin Objects -------------------------------------------------------------------------------------
    """
    # A - Attached Attribute
    #     Line follows the line it belongs to. (Follows pin). Dependent Attribute
    A = {'A': 0, 'x': 1, 'y': 2, 'size': 3, 'rotation': 4, 'justification': 5, 'visible': 6, 'value': 7} 

    # L - Label
    #     Label for the previous pin line item
    L = {'L': 0, 'x': 1, 'y': 2, 'size': 3, 'rotation': 4, 'justification': 5, 'locality': 6, 'label_visible': 7, 'inverted': 8, 'value': 9}  
    
    # P - Pin
    P = {'P': 0, 'id': 1, # Unique ID. Starts at 1 and less than max object count
         'x_net': 2, # x net/trace node side
         'y_net': 3, # y net/trace node side
         'x_sym': 4, # x symbol side (invert NOT bubble side)
         'y_sym': 5, # y symbol side (invert NOT bubble side)
         'unknown': 6, 'side': 7, 'inverted': 8}
    
    """
    Footer Objects -----------------------------------------------------------------------------
    """ 
    # E - End
    E = {'E': 0} # End of File
    

""" ObjectType
Create an ObjectType from key value pairs where keys become class attribute variables with
value being a Field object               
"""   
class ObjectType:
    def __init__(self, obj_dict):
        self._identifier = list(obj_dict.keys())[0]
        
        """ Format: [Dictionary]
        key: Property description
        value: new attribute object - Symbol property's line location index
        """
        self._format = obj_dict.copy()
        self._format_idx2val = {v:k for k, v in self._format.items()}

        obj_dict.pop(self._identifier)

        # Create properties for each key in the dictionary
        for k, v in obj_dict.items():        
            assert k[0].isalpha(), 'First letter of all keys must not be numeric'
            
            #if type(v) != int:
            if v > 0 and hasattr(FieldFormats, k):
                #print(getattr(FieldFormats, k))
                setattr(self, k, Field(v, getattr(FieldFormats, k)))
            else:
                setattr(self, k, Field(v))
                
    # Calling ObjectType will return the line format for that object
    def __call__(self):
        return self._format
        
    # Support indexing
    def __getitem__(self, key):
        if type(key) == int:
            return self._format_idx2val[key]
        else:
            return self._format[key]
        
    def __len__(self):
        return len(self._format) - 1
    
    # Returns symbol line's object type identifier
    def __str__(self):
        return str(self._identifier)    
    

""" Field
idx: Symbol property's line location index
format: [Dictionary] keys: attributes, values: Recognizable value to be decoded by CAD software (Mentor/ViewDraw)
    + attributes: Each attribute is a human readable description as a Field property that has a value matching the format dict's value
    
Example: Example of the A (Attribute) ObjectType's visible Field
    A.visible.idx: 6
    A.visible.format: {'None': 0, 'Name&Value': 1, 'Name': 2, 'Value': 3}
    A.visible.None = 0
    A.visible.Name&Value = 1
    A.visible.Name = 2
    A.visible.Value = 3                      
"""               
class Field:
    def __init__(self, idx, field_dict=None):
        self._idx = idx
        
        if field_dict != None:
            self._format = field_dict
            self._format_idx2val = {v:k for k, v in self._format.items()}
            
            # Create properties for each key in the dictionary
            for k, v in field_dict.items():
                assert k[0].isalpha(), 'First letter of all keys must not be numeric'
                setattr(self, k, v)
                
    def __call__(self):
        if hasattr(self, '_format'):
            return self._format
        else:
            return None
            
    # Support indexing
    def __getitem__(self, key):
        if hasattr(self, '_format_idx2val'):
            if type(key) == int:
                return self._format_idx2val[key]
            else:
                return self._format[key]
        else:
            return None        
            
    def __int__(self):
        return self._idx
            
    def __len__(self):
        if hasattr(self, '_format'):
            return len(self._format)
        else:
            return 0
        
""" SymbolFormat
Contains all formating information to recreate a new symbol file (ViewDraw/Mentor).
Each line of the symbol file is an object. The first space delimited value defines the
object type. All attributes of the SymbolFormat class are ObjectType objects for each
possible object type. These attributes are all defined on instantiation.
"""
class SymbolFormat:
    def __init__(self):
        # Auto generate all ObjectTypes and Fields using the ObjectFormats and FieldFormats classes
        for k in ObjectFormats.__dict__: # Iterate ObjectFormats' class attributes
            if not k.startswith('_'):
                # Add ObjectType for given ObjectFormats' attribute
                self._add_obj(ObjectType(getattr(ObjectFormats, k)))

    # Add Object Type
    def _add_obj(self, obj):
        attr_name = obj._identifier
        # If first character is not alphabetic then remove
        if not attr_name[0].isalpha(): 
            attr_name = obj._identifier[1:]           
        
        setattr(self, attr_name, obj)
