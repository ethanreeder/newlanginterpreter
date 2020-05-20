class Function:
    """
    Object representing function as defined by new language
    """
    def __init__(self, name, parameters, statements, variable_table, parent=None):
        self.name = name
        self.parameters = parameters
        self.num_parameters = len(parameters)
        self.statements = statements
        self.variable_table = variable_table
        self.parent = parent


class FunctionTable:
    """
    Object representing functions defined within a certain scope
    """
    def __init__(self):
        self.functions = {}
        self.parent = None

    def add_function(self, name, parameters, statements, variable_table):
        self.functions[name] = Function(name, parameters, statements, variable_table)


class Context:
    """
    Global context for lexing, parsing, and running code
    Includes list of functions by scope
    In the future can be updated to include list of variables by scope, traceback, or other helpful tools
    """
    def __init__(self):
        # self.variable_table = VariableTable()
        self.function_table = FunctionTable()

# TODO: implement global variable table
# class VariableTable:
#     """
#     Object representing variables defined within a certain scope
#     """
#     def __init__(self, parent=None, function_name=None):
#         self.parent = parent
#         self.function_name = function_name
#         self.variables = {}
#
#     def get_value(self, name):
#         value = self.variables.get(name, None)
#         if value is None and self.parent:
#             value = self.parent.get(name)
#         return value
#
#     def set_value(self, name, value):
#         self.variables[name] = value

