from flask import Flask, render_template, request, jsonify
from rule_engine import create_rule, evaluate_rule, recreate_ast, combine_rules
from database import save_rule, get_rule_by_id, create_rules_table

app = Flask(__name__, static_folder='static', template_folder='templates')

create_rules_table()

# Serve the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# API to create rule and generate AST
@app.route('/api/create_rule', methods=['POST'])
def create_rule_api():
    data = request.json
    rule_string = data.get('rule_string')

    if not rule_string:
        return jsonify({'error': 'Rule string is required'}), 400

    try:
        ast = create_rule(rule_string)  # Create the AST from the rule string
        rule_id = save_rule(rule_string, ast)  # Save the rule and AST to the database
        return jsonify({'ast': ast.to_dict(), 'rule_id': rule_id}), 200  # Include the rule ID in the response
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API to evaluate rule based on user data
@app.route('/api/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    data = request.json
    ast_data = data.get('ast')
    user_data = data.get('user_data')

    if not ast_data or not user_data:
        return jsonify({'error': 'Both AST and user data are required'}), 400

    try:
        ast = recreate_ast(ast_data)  # Recreate the AST from the incoming data
        result = evaluate_rule(ast, user_data)  # Evaluate the rule against user data
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API to combine multiple rules into a single rule (AST)
@app.route('/api/combine_rules', methods=['POST'])
def combine_rules_api():
    data = request.json
    rule_ids = data.get('rule_ids')
    operator = data.get('operator', 'AND')  # Default operator is 'AND'

    if not rule_ids or len(rule_ids) < 2:
        return jsonify({'error': 'At least two rule IDs are required for combination'}), 400

    try:
        # Fetch the ASTs of the rules by their IDs
        rules = []
        for rule_id in rule_ids:
            rule_data = get_rule_by_id(rule_id)
            if not rule_data:
                return jsonify({'error': f'Rule with ID {rule_id} not found'}), 404
            
            # Assuming rule_data is a dictionary with 'ast_data' as the AST string
            rules.append(recreate_ast(rule_data['ast_data']))

        # Combine the rules into a single AST
        combined_ast = combine_rules(rules, operator)

        # Return the combined AST as a response
        return jsonify({'combined_ast': combined_ast.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)