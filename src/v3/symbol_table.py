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

add_symbol('FO', 'PROCEDURE', None, value=None, parameters=["num"])
add_symbol('FORWARD', 'PROCEDURE', None, value=None, parameters=["num"])
add_symbol('BK', 'PROCEDURE', None, value=None, parameters=["num"])
add_symbol('BACKWARD', 'PROCEDURE', None, value=None, parameters=["num"])
add_symbol('RT', 'PROCEDURE', None, value=None, parameters=["angle"])
add_symbol('RIGHT', 'PROCEDURE', None, value=None, parameters=["angle"])
add_symbol('LEFT', 'PROCEDURE', None, value=None, parameters=["num"])
add_symbol('LT', 'PROCEDURE', None, value=None, parameters=["num"])
add_symbol('PU', 'PROCEDURE', None, value=None)
add_symbol('PENUP', 'PROCEDURE', None, value=None)
add_symbol('PD', 'PROCEDURE', None, value=None)
add_symbol('PENDOWN', 'PROCEDURE', None, value=None)
add_symbol('WC', 'PROCEDURE', None, value=None)
add_symbol('WIPECLEAN', 'PROCEDURE', None, value=None)
add_symbol('CS', 'PROCEDURE', None, value=None)
add_symbol('CLEARSCREEN', 'PROCEDURE', None, value=None)
add_symbol('HOME', 'PROCEDURE', None, value=None)
add_symbol('SETXY', 'PROCEDURE', None, value=None, parameters=["x", "y"])
add_symbol('XCOR', 'PROCEDURE', None, value=None)
add_symbol('YCOR', 'PROCEDURE', None, value=None)
add_symbol('HEADING', 'PROCEDURE', None, value=None)
add_symbol('RANDOM', 'PROCEDURE', None, value=None)
add_symbol('PRINT', 'PROCEDURE', None, value=None, parameters=["data"])
add_symbol('TYPEIN', 'PROCEDURE', None, value=None)