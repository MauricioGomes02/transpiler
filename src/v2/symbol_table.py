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

add_symbol('FO', 'PROCEDURE', None, value=None, args=["num"])
add_symbol('FORWARD', 'PROCEDURE', None, value=None, args=["num"])