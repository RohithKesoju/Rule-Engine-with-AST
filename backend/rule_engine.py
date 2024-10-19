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

def combine_rules(rules, operator='AND'):
    """
    Combines a list of ASTs into a single AST using the specified operator.
    
    :param rules: List of ASTs (Node objects) to combine.
    :param operator: Logical operator ('AND'/'OR') used to combine the rules. Default is 'AND'.
    :return: Root node of the combined AST.
    """
    if not rules:
        raise ValueError("No rules provided for combination.")
    
    # Initialize the combined AST with the first rule
    combined_ast = rules[0]
    
    # Combine all the subsequent rules
    for rule in rules[1:]:
        combined_ast = Node(
            type='operator',
            left=combined_ast,
            right=rule,
            value=operator
        )
    
    return combined_ast

def evaluate_rule(ast, user_data):
    """
    Evaluate the AST by applying the user data to the rule.
    """
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
    
#     if value.startswith("'") and value.endswith("'"):
#         value = value[1:-1]
    
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

# def combine_rules(rules, operator='AND'):
#     """
#     Combines a list of ASTs into a single AST using the specified operator.
    
#     :param rules: List of ASTs (Node objects) to combine.
#     :param operator: Logical operator ('AND'/'OR') used to combine the rules. Default is 'AND'.
#     :return: Root node of the combined AST.
#     """
#     if not rules:
#         raise ValueError("No rules provided for combination.")
    
#     # Initialize the combined AST with the first rule
#     combined_ast = rules[0]
    
#     # Combine all the subsequent rules
#     for rule in rules[1:]:
#         combined_ast = Node(
#             node_type='operator',
#             left=combined_ast,
#             right=rule,
#             value=operator
#         )
    
#     return combined_ast

# from operator import gt, lt, eq, ge, le

# from operator import gt, lt, eq, ge, le


# def evaluate_rule(ast, user_data):
#     operator_map = {
#         '>': gt,
#         '<': lt,
#         '=': eq,
#         '>=': ge,
#         '<=': le
#     }

#     if ast.type == 'operand':
#         field, (operator_str, value) = list(ast.value.items())[0]
#         operator_func = operator_map[operator_str]

#         user_value = user_data.get(field)

#         # Handle both number and string comparisons
#         if isinstance(value, (int, float)) and isinstance(user_value, str):
#             user_value = float(user_value)  # Convert string to float for comparison
#         elif isinstance(value, str) and isinstance(user_value, (int, float)):
#             user_value = str(user_value)  # Convert number to string for comparison

#         # Ensure exact match for string comparisons
#         return operator_func(user_value, value)

#     # Evaluate left and right branches
#     left_result = evaluate_rule(ast.left, user_data)
#     right_result = evaluate_rule(ast.right, user_data)

#     if ast.value == 'AND':
#         return left_result and right_result
#     elif ast.value == 'OR':
#         if left_result:
#             return True
#         return right_result




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
