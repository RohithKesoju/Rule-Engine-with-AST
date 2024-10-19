# # import re
# # from operator import gt, lt, eq, ge, le

# # class Node:
# #     def __init__(self, type, left=None, right=None, value=None):
# #         self.type = type  # 'operator' or 'operand'
# #         self.left = left  # Left child (for operators)
# #         self.right = right  # Right child (for operators)
# #         self.value = value  # Condition (for operands), e.g., {'age': '> 30'}

# #     def to_dict(self):
# #         """
# #         Convert the Node object into a dictionary to allow for JSON serialization.
# #         Recursively converts children (left/right) as well.
# #         """
# #         node_dict = {
# #             'type': self.type,
# #             'value': self.value
# #         }
# #         if self.left:
# #             node_dict['left'] = self.left.to_dict()
# #         if self.right:
# #             node_dict['right'] = self.right.to_dict()
# #         return node_dict

# # def create_condition_node(condition_str):
# #     """
# #     Parses and converts a condition like 'age > 30' into a Node.
# #     Handles basic operators: >, <, >=, <=, =.
# #     """
# #     pattern = r'(\w+)\s*(>|<|>=|<=|=)\s*(\d+|\'.*?\')'
# #     match = re.match(pattern, condition_str.strip())
    
# #     if not match:
# #         raise ValueError(f"Invalid condition: {condition_str}")
    
# #     field, operator_str, value = match.groups()
    
# #     if operator_str == '>':
# #         operator_func = gt
# #     elif operator_str == '<':
# #         operator_func = lt
# #     elif operator_str == '=':
# #         operator_func = eq
# #     elif operator_str == '>=':
# #         operator_func = ge
# #     elif operator_str == '<=':
# #         operator_func = le
# #     else:
# #         raise ValueError(f"Invalid operator: {operator_str}")
    
# #     if value.startswith("'") and value.endswith("'"):
# #         value = value[1:-1]
    
# #     return Node(type='operand', value={field: (operator_func, value)})

# import re
# from operator import gt, lt, eq, ge, le

# class Node:
#     def __init__(self, type, left=None, right=None, value=None):
#         self.type = type  # 'operator' or 'operand'
#         self.left = left  # Left child (for operators)
#         self.right = right  # Right child (for operators)
#         self.value = value  # Condition (for operands), e.g., {'age': '> 30'}

#     def to_dict(self):
#         """
#         Convert the Node object into a dictionary to allow for JSON serialization.
#         Recursively converts children (left/right) as well.
#         """
#         node_dict = {
#             'type': self.type,
#             'value': self.value
#         }
#         if self.left:
#             node_dict['left'] = self.left.to_dict()
#         if self.right:
#             node_dict['right'] = self.right.to_dict()
#         return node_dict

# def create_condition_node(condition_str):
#     """
#     Parses and converts a condition like 'age > 30' into a Node.
#     Handles basic operators: >, <, >=, <=, =.
#     """
#     pattern = r'(\w+)\s*(>|<|>=|<=|=)\s*(\d+|\'.*?\')'
#     match = re.match(pattern, condition_str.strip())
    
#     if not match:
#         raise ValueError(f"Invalid condition: {condition_str}")
    
#     field, operator_str, value = match.groups()
    
#     # Remove quotes from string values like 'Sales'
#     if value.startswith("'") and value.endswith("'"):
#         value = value[1:-1]
    
#     # Store the operator as a string (e.g., '>', '=', etc.) instead of a function
#     return Node(type='operand', value={field: (operator_str, value)})


# def create_rule(rule_string):
#     """
#     Parses a rule string and converts it into an Abstract Syntax Tree (AST).
#     Handles nested parentheses and AND/OR operators.
#     """
#     rule_string = rule_string.strip().lstrip('(').rstrip(')')
#     tokens = re.split(r'\s+(AND|OR)\s+', rule_string)

#     if len(tokens) == 1:
#         return create_condition_node(tokens[0])

#     current_node = None
#     current_operator = None

#     for token in tokens:
#         if token == 'AND' or token == 'OR':
#             current_operator = token
#         else:
#             token = token.strip().lstrip('(').rstrip(')')
#             condition_node = create_condition_node(token)
#             if current_node is None:
#                 current_node = condition_node
#             else:
#                 current_node = Node(type='operator', value=current_operator, left=current_node, right=condition_node)
    
#     return current_node

# # def evaluate_rule(ast, user_data):
# #     """
# #     Evaluate the AST by applying the user data to the rule.
# #     """
# #     if ast.type == 'operand':
# #         # Evaluate the operand (condition)
# #         field, (operator_func, value) = list(ast.value.items())[0]
# #         return operator_func(user_data.get(field), value)
    
# #     # Recursively evaluate left and right sides of the operator
# #     left_result = evaluate_rule(ast.left, user_data)
# #     right_result = evaluate_rule(ast.right, user_data)
    
# #     if ast.value == 'AND':
# #         return left_result and right_result
# #     elif ast.value == 'OR':
# #         return left_result or right_result
# #     else:
# #         raise ValueError(f"Invalid operator: {ast.value}")

# def evaluate_rule(ast, user_data):
#     """
#     Evaluate the AST by applying the user data to the rule.
#     """
#     # Map of operator strings to Python functions
#     operator_map = {
#         '>': gt,
#         '<': lt,
#         '=': eq,
#         '>=': ge,
#         '<=': le
#     }
    
#     if ast.type == 'operand':
#         # Evaluate the operand (condition)
#         field, (operator_str, value) = list(ast.value.items())[0]
#         operator_func = operator_map[operator_str]  # Convert operator string to function
#         return operator_func(user_data.get(field), value)
    
#     # Recursively evaluate left and right sides of the operator
#     left_result = evaluate_rule(ast.left, user_data)
#     right_result = evaluate_rule(ast.right, user_data)
    
#     if ast.value == 'AND':
#         return left_result and right_result
#     elif ast.value == 'OR':
#         return left_result or right_result
#     else:
#         raise ValueError(f"Invalid operator: {ast.value}")


# def recreate_ast(node_data):
#     """
#     Recreate the AST from a dictionary (JSON-like structure).
#     """
#     node = Node(type=node_data['type'], value=node_data.get('value'))
#     if node_data.get('left'):
#         node.left = recreate_ast(node_data['left'])
#     if node_data.get('right'):
#         node.right = recreate_ast(node_data['right'])
#     return node






import re
from operator import gt, lt, eq, ge, le

class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type  # 'operator' or 'operand'
        self.left = left  # Left child (for operators)
        self.right = right  # Right child (for operators)
        self.value = value  # Condition (for operands), e.g., {'age': '> 30'}

    def to_dict(self):
        """
        Convert the Node object into a dictionary to allow for JSON serialization.
        Recursively converts children (left/right) as well.
        """
        node_dict = {
            'type': self.type,
            'value': self.value
        }
        if self.left:
            node_dict['left'] = self.left.to_dict()
        if self.right:
            node_dict['right'] = self.right.to_dict()
        return node_dict

def create_condition_node(condition_str):
    """
    Parses and converts a condition like 'age > 30' into a Node.
    Handles basic operators: >, <, >=, <=, =.
    """
    pattern = r'(\w+)\s*(>|<|>=|<=|=)\s*(\d+|\'.*?\')'
    match = re.match(pattern, condition_str.strip())
    
    if not match:
        raise ValueError(f"Invalid condition: {condition_str}")
    
    field, operator_str, value = match.groups()
    
    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    
    return Node(type='operand', value={field: (operator_str, value)})

def create_rule(rule_string):
    """
    Parses a rule string and converts it into an Abstract Syntax Tree (AST).
    Handles nested parentheses and AND/OR operators.
    """
    rule_string = rule_string.strip().lstrip('(').rstrip(')')
    tokens = re.split(r'\s+(AND|OR)\s+', rule_string)

    if len(tokens) == 1:
        return create_condition_node(tokens[0])

    current_node = None
    current_operator = None

    for token in tokens:
        if token == 'AND' or token == 'OR':
            current_operator = token
        else:
            token = token.strip().lstrip('(').rstrip(')')
            condition_node = create_condition_node(token)
            if current_node is None:
                current_node = condition_node
            else:
                current_node = Node(type='operator', value=current_operator, left=current_node, right=condition_node)
    
    return current_node

# def evaluate_rule(ast, user_data):
#     """
#     Evaluate the AST by applying the user data to the rule.
#     """
#     operator_map = {
#         '>': gt,
#         '<': lt,
#         '=': eq,
#         '>=': ge,
#         '<=': le
#     }
    
#     if ast.type == 'operand':
#         # Evaluate the operand (condition)
#         field, (operator_str, value) = list(ast.value.items())[0]
#         operator_func = operator_map[operator_str]
#         return operator_func(user_data.get(field), value)
    
#     # Recursively evaluate left and right sides of the operator
#     left_result = evaluate_rule(ast.left, user_data)
#     right_result = evaluate_rule(ast.right, user_data)
    
#     if ast.value == 'AND':
#         return left_result and right_result
#     elif ast.value == 'OR':
#         return left_result or right_result
#     else:
#         raise ValueError(f"Invalid operator: {ast.value}")

from operator import gt, lt, eq, ge, le

from operator import gt, lt, eq, ge, le

# def evaluate_rule(ast, user_data):
#     """
#     Evaluate the AST by applying the user data to the rule.
#     """
#     operator_map = {
#         '>': gt,
#         '<': lt,
#         '=': eq,
#         '>=': ge,
#         '<=': le
#     }
    
#     if ast.type == 'operand':
#         # Evaluate the operand (condition)
#         field, (operator_str, value) = list(ast.value.items())[0]
#         operator_func = operator_map[operator_str]

#         # Convert the user data to match the type of the value being compared
#         user_value = user_data.get(field)
#         if isinstance(value, (int, float)) and isinstance(user_value, str):
#             user_value = float(user_value)  # Convert string to float for comparison
#         elif isinstance(value, str) and isinstance(user_value, (int, float)):
#             user_value = str(user_value)    # Convert number to string for comparison

#         return operator_func(user_value, value)

#     # Recursively evaluate left and right sides of the operator
#     left_result = evaluate_rule(ast.left, user_data)
#     right_result = evaluate_rule(ast.right, user_data)
    
#     if ast.value == 'AND':
#         return left_result and right_result
#     elif ast.value == 'OR':
#     # Short-circuit evaluation for OR
#         if left_result:
#             return True
#         return right_result
#     else:
#         raise ValueError(f"Invalid operator: {ast.value}")
    
    # if ast.value == 'AND':
    #     return left_result and right_result
    # elif ast.value == 'OR':
    #     return left_result or right_result
    # else:
    #     raise ValueError(f"Invalid operator: {ast.value}")


def evaluate_rule(ast, user_data):
    operator_map = {
        '>': gt,
        '<': lt,
        '=': eq,
        '>=': ge,
        '<=': le
    }

    if ast.type == 'operand':
        field, (operator_str, value) = list(ast.value.items())[0]
        operator_func = operator_map[operator_str]

        user_value = user_data.get(field)

        # Handle both number and string comparisons
        if isinstance(value, (int, float)) and isinstance(user_value, str):
            user_value = float(user_value)  # Convert string to float for comparison
        elif isinstance(value, str) and isinstance(user_value, (int, float)):
            user_value = str(user_value)  # Convert number to string for comparison

        # Ensure exact match for string comparisons
        return operator_func(user_value, value)

    # Evaluate left and right branches
    left_result = evaluate_rule(ast.left, user_data)
    right_result = evaluate_rule(ast.right, user_data)

    if ast.value == 'AND':
        return left_result and right_result
    elif ast.value == 'OR':
        if left_result:
            return True
        return right_result




def recreate_ast(node_data):
    """
    Recreate the AST from a dictionary (JSON-like structure).
    """
    node = Node(type=node_data['type'], value=node_data.get('value'))
    if node_data.get('left'):
        node.left = recreate_ast(node_data['left'])
    if node_data.get('right'):
        node.right = recreate_ast(node_data['right'])
    return node
