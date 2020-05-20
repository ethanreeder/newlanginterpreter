import sys
from context import Context
from context import VariableTable
from context import FunctionTable
from parser import Parser
import node_types as NodeType
from error import Error
from error_types import ErrorType


class Interpreter:
    def __init__(self, ast, context):
        self.ast = ast
        self.context = context

    def interpret(self, node, context):
        for child in node:
            if child == NodeType.PROGRAM:
                return self.handle_program(node[child], context)
            else:
                return Error(ErrorType.INVALID_SYNTAX, "Expected program start token")

    def handle_program(self, node, context):
        for child in node:
            if child == NodeType.FUNCTION_DEFINITION:
                pass
            elif child == NodeType.RETURN:
                return self.handle_return(node[child], context)
            elif child == NodeType.IF:
                return self.handle_expression(node[child], context)
            else:
                return Error(ErrorType.INVALID_SYNTAX, 'Undefined node in abstract syntax tree')

    def handle_return(self, node, context):
        return self.handle_expression(node[NodeType.EXPRESSION], context)

    def handle_expression(self, node, context):
        for child in node:
            if child == NodeType.NUMBER:
                return node[NodeType.NUMBER]
            elif child == NodeType.STRING:
                return node[NodeType.STRING]

            if child == NodeType.VARIABLE_ACCESS:
                self.handle_variable_access(node, context)

    def handle_built_in_function(self, node, context):
        parameter_one = None
        parameter_two = None

        for child in node:
            if child == NodeType.EXPRESSION:
                if parameter_one is None:
                    parameter_one = self.handle_expression(node[NodeType.EXPRESSION], context)
                elif parameter_two is None:
                    parameter_two  = self.handle_expression(node[NodeType.EXPRESSION], context)
                else:
                    return Error(ErrorType.INVALID_SYNTAX, "Expected only two parameters for binary operation")

        for child in node:
            if child == NodeType.EQUALITY:
                return parameter_one == parameter_two
            if child == NodeType.PLUS:
                return parameter_one + parameter_two
            if child == NodeType.MINUS:
                return parameter_one + parameter_two

        return Error(ErrorType.INVALID_SYNTAX, "Expected '+', '-', or '=='")

    def handle_variable_declaration(self, node, context):
        variable_name = None
        variable_value = None

        for child in node:
            if child == NodeType.NAME:
                variable_name = node[child]
            if child == NodeType.VALUE:
                variable_value = node[child]

        if variable_name is None:
            return Error(ErrorType.INVALID_SYNTAX, 'Defined variable with no name')

        if variable_value is None:
            return Error(ErrorType.INVALID_SYNTAX, 'Defined function with no value')

        context.variable_table.set_value(variable_name, variable_value)
        print('set variable')

    def handle_variable_access(self, node, context):
        for child in node:
            if child == NodeType.NAME:
                if child in context.variable_table:
                    return context.variable_table.get_value(child)
                else:
                    return Error(ErrorType.INVALID_SYNTAX, 'Attempt to access undefined variable')

        return Error(ErrorType.INVALID_SYNTAX, 'Attempt to access variable with no name')

    def handle_function_definition(self, node, context):
        function_name = None
        function_statements = []
        function_variable_table = None

        for child in node:
            if child == NodeType.NAME:
                function_name = node[child]
                function_variable_table = VariableTable(context.variable_table, function_name)
            elif child == NodeType.EXPRESSION:
                function_statements.append({'expression': self.handle_expression(child, context)})
            elif child == NodeType.VARIABLE_DECLARATION:
                self.set_variable(node[child], function_variable_table)
            elif child == NodeType.VARIABLE_ACCESS:
                self.get_variable(node[child], function_variable_table)
            elif child == NodeType.RETURN:
                return self.handle_expression(node[child], context)

        if function_name is None:
            return Error(ErrorType.INVALID_SYNTAX, 'Defined function with no name for identifier')

        if not function_statements:
            return Error(ErrorType.INVALID_SYNTAX, 'Defined function with no statements')

        context.function_table.add_function(function_name, function_statements, function_variable_table)

    def handle_function_call(self, node, context):
        # function_name = None
        # function_expressions = {}
        #
        # for child in node:
        #     if child == NodeType.NAME:
        #         function_name = node['name']
        #     if child == NodeType.EXPRESSION:
        #         function_expressions
        pass

    def set_variable(self, node, variable_table):
        variable_table.set_value(node['name'], node['value'])

    def get_variable(self, node, variable_table):
        variable_table.get_value(node['name'])


def main():
    """
    """
    context = Context()

    if len(sys.argv) > 1:
        index = 1
        while index < len(sys.argv):
            if sys.argv[index] == "-f" and len(sys.argv) >= index+1:
                index += 1
                fn = sys.argv[index]
            index += 1
    else:
        print('Invalid or insufficient arguments')

    parser = Parser(fn)
    ast = parser.parse()

    if type(ast) == Error:
        print(ast)
        return

    # print(ast)
    # print(ast[NodeType.PROGRAM])

    interpreter = Interpreter(ast, context)
    result = interpreter.interpret(ast, context)

    print(result)



main()