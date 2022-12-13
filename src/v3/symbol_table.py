import uuid


__symtable = {}

class SymbolRedefinitionError(Exception):
    """Error raised when a symbol is already defined."""

    def __init__(self, obj, lineno):
        """Initialize error with proper message."""
        super().__init__(
            f"Redeclaration of symbol: {obj['name']}:{lineno}: "
            + f"Previously declared at line {obj['lineno']}"
        )


class InternalError(Exception):
    """Error raised when a symbol is already defined."""

    def __init__(self, msg):
        """Initialize error with proper message."""
        super().__init__(f"Internal error: {msg}")


def add_symbol(symbol, sym_type, lineno, **kwargs):
    """Create new symbol in the symbol table."""
    obj = get_symbol(symbol)

    if obj:
        raise SymbolRedefinitionError(obj, lineno)

    kwargs["name"] = symbol
    kwargs["type"] = sym_type
    kwargs["lineno"] = lineno
    __symtable[symbol] = kwargs
    return __symtable[symbol]


def set_symbol(symbol, **kwargs):
    """Set values of a symbol in symbol table."""
    obj = get_symbol(symbol)
    if obj is None:
        raise InternalError(f"Symbol not defined: {symbol}")
    if "name" in kwargs:
        raise InternalError(
            f"Cannot modify symbol '{symbol}' attribute 'name'."
        )
    if "lineno" in kwargs:
        raise InternalError(f"Cannot modify symbol {symbol} attribute 'line'.")
    obj.update(kwargs)


def get_symbol(symbol):
    """Retrieve symbol from symbol table."""
    return __symtable.get(symbol)


add_symbol('FO', 'PROCEDURE', None, value=None, optional_parameters=["num"])
add_symbol('FORWARD', 'PROCEDURE', None, value=None, optional_parameters=["num"])
add_symbol('BK', 'PROCEDURE', None, value=None, optional_parameters=["num"])
add_symbol('BACKWARD', 'PROCEDURE', None, value=None, optional_parameters=["num"])
add_symbol('RT', 'PROCEDURE', None, value=None, optional_parameters=["angle"])
add_symbol('RIGHT', 'PROCEDURE', None, value=None, optional_parameters=["angle"])
add_symbol('LEFT', 'PROCEDURE', None, value=None, optional_parameters=["num"])
add_symbol('LT', 'PROCEDURE', None, value=None, optional_parameters=["num"])
add_symbol('PU', 'PROCEDURE', None, value=None, optional_parameters = None)
add_symbol('PENUP', 'PROCEDURE', None, value=None, optional_parameters = None)
add_symbol('PD', 'PROCEDURE', None, value=None, optional_parameters = None)
add_symbol('PENDOWN', 'PROCEDURE', None, value=None, optional_parameters = None)
add_symbol('WC', 'PROCEDURE', None, value=None, optional_parameters = None)
add_symbol('WIPECLEAN', 'PROCEDURE', None, value=None, optional_parameters = None)
add_symbol('CS', 'PROCEDURE', None, value=None, optional_parameters = None)
add_symbol('CLEARSCREEN', 'PROCEDURE', None, value=None, optional_parameters = None)
add_symbol('HOME', 'PROCEDURE', None, value=None, optional_parameters = None)
add_symbol('SETXY', 'PROCEDURE', None, value=None, optional_parameters=["x", "y"])
add_symbol('XCOR', 'PROCEDURE', None, value=None, optional_parameters = None)
add_symbol('YCOR', 'PROCEDURE', None, value=None, optional_parameters = None)
add_symbol('HEADING', 'PROCEDURE', None, value=None, optional_parameters = None)
add_symbol('RANDOM', 'PROCEDURE', None, value=None, optional_parameters = None)
add_symbol('PRINT', 'PROCEDURE', None, value=None, optional_parameters=["data"])
add_symbol('TYPEIN', 'PROCEDURE', None, value=None, optional_parameters = None)

class Scope:
    def __init__(self, parent = None, childrens = []):
        self.parent = parent
        self.childrens = childrens
        self.symbols = {}
        self.identifier = str(uuid.uuid4())

    def add_symbol(self, symbol):
        name = f'{self.identifier}_{symbol.name}'
        obj = self.get_symbol(name)

        if obj:
            raise SymbolRedefinitionError(obj, self.line)

        symbol.name = name
        self.symbols[name] = symbol
        return  self.symbols[name]

    def add_symbol_internal(self, symbol):
        name = f'{symbol.name}'
        obj = self.get_symbol(name)

        if obj:
            raise SymbolRedefinitionError(obj, self.line)

        symbol.name = name
        self.symbols[name] = symbol
        return  self.symbols[name]

    def get_symbol(self, name):
        return self.symbols.get(f'{self.identifier}_{name}')

    def add_parent(self, parent):
        self.parent = parent

    def add_children(self, children):
        self.childrens.append(children)

    def get_parent(self):
        return self.parent

    def get_childrens(self):
        return self.childrens

class Symbol:
    def __init__(self, name, type, value, optional_parameters = None, line = None):
        self.name = name
        self.type = type
        self.value = value
        self.optional_parameters = optional_parameters
        self.line = line

NUMBER_VARIABLE = 1
BOOLEAN_VARIABLE = 2
STRING_VARIABLE = 3
PROCEDURE = 4
ARGUMENT = 5

symbol_table = Scope()

identifier_procedures = str(uuid.uuid4())
symbol_table.add_symbol_internal(Symbol(
    f'{identifier_procedures}_num',
    ARGUMENT,
    None,
    None,
    None
))
symbol_table.add_symbol_internal(Symbol(
    f'{identifier_procedures}_data',
    ARGUMENT,
    None,
    None,
    None
))
symbol_table.add_symbol_internal(Symbol(
    f'{identifier_procedures}_x',
    ARGUMENT,
    None,
    None,
    None
))
symbol_table.add_symbol_internal(Symbol(
    f'{identifier_procedures}_y',
    ARGUMENT,
    None,
    None,
    None
))

symbol_table.add_symbol(Symbol(
    'FO', PROCEDURE, None, [f'{identifier_procedures}_num'], None 
))
symbol_table.add_symbol(Symbol(
    'FORWARD', PROCEDURE, None, [f'{identifier_procedures}_num'], None 
))
symbol_table.add_symbol(Symbol(
    'BK', PROCEDURE, None, [f'{identifier_procedures}_num'], None 
))
symbol_table.add_symbol(Symbol(
    'BACKWARD', PROCEDURE, None, [f'{identifier_procedures}_num'], None 
))
symbol_table.add_symbol(Symbol(
    'RT', PROCEDURE, None, [f'{identifier_procedures}_num'], None 
))
symbol_table.add_symbol(Symbol(
    'RIGHT', PROCEDURE, None, [f'{identifier_procedures}_num'], None 
))
symbol_table.add_symbol(Symbol(
    'LT', PROCEDURE, None, [f'{identifier_procedures}_num'], None 
))
symbol_table.add_symbol(Symbol(
    'LEFT', PROCEDURE, None, [f'{identifier_procedures}_num'], None 
))
symbol_table.add_symbol(Symbol(
    'PU', PROCEDURE, None, [], None 
))
symbol_table.add_symbol(Symbol(
    'PENUP', PROCEDURE, None, [], None 
))
symbol_table.add_symbol(Symbol(
    'PD', PROCEDURE, None, [], None 
))
symbol_table.add_symbol(Symbol(
    'PENDOWN', PROCEDURE, None, [], None 
))
symbol_table.add_symbol(Symbol(
    'WC', PROCEDURE, None, [], None 
))
symbol_table.add_symbol(Symbol(
    'WIPECLEAN', PROCEDURE, None, [], None 
))
symbol_table.add_symbol(Symbol(
    'CS', PROCEDURE, None, [], None 
))
symbol_table.add_symbol(Symbol(
    'CLEARSCREEN', PROCEDURE, None, [], None 
))
symbol_table.add_symbol(Symbol(
    'HOME', PROCEDURE, None, [], None 
))
symbol_table.add_symbol(Symbol(
    'SETXY', PROCEDURE, None, [f'{identifier_procedures}_x', f'{identifier_procedures}_y'], None 
))
symbol_table.add_symbol(Symbol(
    'XCOR', PROCEDURE, None, [], None 
))
symbol_table.add_symbol(Symbol(
    'YCOR', PROCEDURE, None, [], None 
))
symbol_table.add_symbol(Symbol(
    'HEADING', PROCEDURE, None, [], None 
))
symbol_table.add_symbol(Symbol(
    'RANDOM', PROCEDURE, None, [], None 
))
symbol_table.add_symbol(Symbol(
    'PRINT', PROCEDURE, None, [f'{identifier_procedures}_data'], None 
))
symbol_table.add_symbol(Symbol(
    'TYPEIN', PROCEDURE, None, [], None 
))