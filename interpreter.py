import sys
from context import Context
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
        """
        Execute first step of interpretation based on program keyword

        :param node: the next level of the tree to visit
        :param context: global context
        :return: integer, float, string, or Error
        """
        for child in node:
            if child == NodeType.FUNCTION_DEFINITION:
                pass
            elif child == NodeType.RETURN:
                return self.handle_return(node[child], context)
            elif child == NodeType.IF:
                return self.handle_expression(node[child], context)
            else:
                return Error(ErrorType.INVALID_SYNTAX, 'Program included invalid child nodes')

    def handle_statement(self, node, context):
        """
        Execute statement of function definition, if, or return and only return value if includes return statement

        :param node: the next level of the tree to visit
        :param context: global context
        :return: integer, float, string, nothing, or Error
        """
        for child in node:
            if child == NodeType.FUNCTION_DEFINITION:
                self.handle_statement(node[child], context)
            if child == NodeType.IF:
                self.handle_if(node[child], context)
            if child == NodeType.RETURN:
                return self.handle_expression(node[child], context)
            else:
                return Error(ErrorType.INVALID_SYNTAX, 'Statement included invalid child nodes')

    def handle_function_definition(self, node, context):
        """
        Identify function name, parameters, and statements and add to the function table in context of relevant scope

        :param node: the next level of the tree to visit
        :param context: global context
        :return: integer, float, or string, or Error
        """
        function_name = None
        function_parameters = []
        function_statements = []
        function_variable_table = None

        for child in node:
            if child == NodeType.NAME:
                function_name = node[child]
            elif child == NodeType.PARAMETER:
                function_parameters.append(node[child])
            elif child == NodeType.STATEMENT:
                function_statements.append(node[child])
            elif child == NodeType.RETURN:
                return self.handle_expression(node[child], context)

        if function_name is None:
            return Error(ErrorType.INVALID_SYNTAX, 'Defined function with no name for identifier')

        if not function_statements:
            return Error(ErrorType.INVALID_SYNTAX, 'Defined function with no statements')

        context.function_table.add_function(function_name, function_parameters,
                                            function_statements, function_variable_table)

    def handle_if(self, node, context):
        """
        Execute if statement evaluating the provided expression
        If evaluation is true, execute all statements, if false, do nothing

        :param node: the next level of the tree to visit
        :param context: global context
        :return: n/a
        """
        expression = None
        statements = []

        for child in node:
            if child == NodeType.EXPRESSION:
                expression = self.handle_expression(node[child], context)
            if child == NodeType.STATEMENT:
                statements.append(self.handle_statement(node[child], context))

        if expression is None:
            return Error(ErrorType.INVALID_SYNTAX, "if statement has no expression to evaluate")

        if not statements:
            return Error(ErrorType.INVALID_SYNTAX, "if statement has no statements to execute")

        if expression:
            for statement in statements:
                self.handle_statement(statement, context)

    def handle_return(self, node, context):
        """
        Execute return statement

        :param node: the next level of the tree to visit
        :param context: global context
        :return: integer, float, or string
        """
        return self.handle_expression(node[NodeType.EXPRESSION], context)

    def handle_expression(self, node, context):
        """
        Evaluate an expression composed of nested other types, but culminating in a number or string

        :param node: the next level of the tree to visit
        :param context: global context
        :return: integer, float, or string
        """
        for child in node:
            if child == NodeType.NUMBER:
                return node[NodeType.NUMBER]
            elif child == NodeType.STRING:
                return node[NodeType.STRING]
            elif child == NodeType.FUNCTION_CALL:
                return self.handle_function_call(node[child], context)
            elif child == NodeType.BUILT_IN_FUNCTION:
                return self.handle_built_in_function(node[child], context)
            elif child == NodeType.PARAMETER:
                return self.handle_parameter(node[child], context)
            else:
                return Error(ErrorType.INVALID_SYNTAX, "Expression contained invalid node type")

    def handle_built_in_function(self, node, context):
        """
        Identify which built_in_function to use (all are binary operators)
        and call it on the two provided expressions, returning the result

        :param node: the next level of the tree to visit
        :param context: global context
        :return: integer, float, or boolean
        """
        function_name = None
        expressions = []

        for child in node:
            if child == NodeType.EXPRESSION:
                expressions.append(node[child])
            if child == NodeType.EQUALITY:
                if function_name is None:
                    function_name = NodeType.EQUALITY
                else:
                    return Error(ErrorType.INVALID_SYNTAX, "More than one built in function name provided")
            if child == NodeType.PLUS:
                if function_name is None:
                    function_name = NodeType.PLUS
                else:
                    return Error(ErrorType.INVALID_SYNTAX, "More than one built in function name provided")
            if child == NodeType.MINUS:
                if function_name is None:
                    function_name = NodeType.MINUS
                else:
                    return Error(ErrorType.INVALID_SYNTAX, "More than one built in function name provided")

        if function_name is None:
            return Error(ErrorType.INVALID_SYNTAX, "No built in function name provided")

        if len(expressions) != 2:
            return Error(ErrorType.INVALID_SYNTAX, "Expected only two inputs for binary operation")

        if function_name == NodeType.EQUALITY:
            return self.handle_expression(expressions[0], context) == self.handle_expression(expressions[1], context)
        elif function_name == NodeType.PLUS:
            return self.handle_expression(expressions[0], context) + self.handle_expression(expressions[1], context)
        elif function_name == NodeType.MINUS:
            return self.handle_expression(expressions[0], context) - self.handle_expression(expressions[1], context)

        return Error(ErrorType.INVALID_SYNTAX, "Unexpected built in function")

    def handle_function_call(self, node, context):
        """
        Identify function name, look up in function table in global context, and execute

        :param node: the next level of the tree to visit
        :param context: global context
        :return: returns evaluation of function if there is a return statement, if not, returns nothing
        """
        function_name = None
        function_expressions = []

        for child in node:
            if child == NodeType.NAME:
                function_name = node[child]
            if child == NodeType.EXPRESSION:
                function_expressions.append(node[child])

        if function_name is None:
            return Error(ErrorType.INVALID_SYNTAX, 'Called function without name as identifier')

        if function_name not in context.function_table:
            return Error(ErrorType.INVALID_SYNTAX, 'Called undefined function')

        if len(function_expressions) != context.function_table.num_parameters:
            return Error(ErrorType.INVALID_SYNTAX,
                         f"Function {function_name} expected {context.function_table.num_parameters} parameters " +
                         f"but received {len(function_expressions)} parameters")

        function = context.function_table[function_name]

        for statement in function.statements:
            if NodeType.RETURN in statement:
                return self.handle_statement(statement, context)
            else:
                self.handle_statement(statement, context)

    def handle_parameter(self, node, context):
        """
        Return string parameter
        Not to useful right now, but potential for expansion and necessary if variables are added

        :param node: the next level of the tree to visit
        :param context: global context
        :return: string
        """
        return node


def main():
    """
    Take in a file from user input, parse file and interpret parsed text, show output or error with details

    :return: string, integer, float, or Error
    """
    context = Context()
    fn = None

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

    interpreter = Interpreter(ast, context)
    result = interpreter.interpret(ast, context)

    print(result)
    return result


main()
