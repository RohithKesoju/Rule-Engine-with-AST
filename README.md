
# Rule Engine with AST 
Python Flask Implementation


## Objective:

This application is a Python Flask-based rule engine that leverages Abstract Syntax Trees (ASTs) to represent and evaluate conditional rules. It provides a flexible and efficient way to determine user eligibility based on various attributes.


### RESTful API: 
Exposes endpoints for creating, combining, and evaluating rules.

### AST Representation:
Rules are represented as ASTs for efficient parsing and evaluation.

### Data Storage: 
Rules and metadata are stored in a database for persistence.

### Error Handling:
Robust error handling mechanisms are in place.

### Extensibility:
The system is designed to be easily extended with new features.


## Installation and Usage

1. Clone the repository

```bash
  git clone https://github.com/your-username/rule-engine-flask
```

2. Install dependencies

```bash
cd rule-engine-flask
pip install -r requirements.txt
```
3. Create a database 

Set up your chosen database (e.g., PostgreSQL, MySQL, SQLite) and create the necessary tables.

4. Start the Flask application

```bash
python app.py
```
5. Use Postman to interact with the API

Method: POST
URL: http://localhost:5000/api/create_rule

```bash
{
    "rule": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
}
```

6. Combine rules
Method: POST
URL: http://localhost:5000/api/combine_rules

```bash
[
    {
        "rule": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
    }
]
```

7. Evaluate a rule

Method: POST
URL: http://localhost:5000/api/evaluate_rule

```bash
{
    "rule_id": 1,
    "data": {
        "age": 35,
        "department": "Sales",
        "salary": 60000,
        "experience": 3
    }
}
```
## API Endpoints

- /rules: Creates a new rule.
- /rules/combine: Combines multiple rules.
- /rules/evaluate: Evaluates a rule against given data.

## Data Structure

- Rules are stored in a database using a JSON representation of the AST.

## Database 

- sqlite3

## Extensions

- User-defined functions
- Rule modification
- Rule visualization
- Integration with other systems

## Outputs 
![3](https://github.com/user-attachments/assets/f22c2983-a3c6-4590-82bb-cd9b3b382da6)
![5](https://github.com/user-attachments/assets/42b31e2c-2dda-44d3-994c-3836bd6fe785)
![6](https://github.com/user-attachments/assets/e95faff1-347f-4c5f-9b65-a6ff052290c0)
![7](https://github.com/user-attachments/assets/dae4d87a-9c96-47ab-b315-0184ea5d25ca)
![8](https://github.com/user-attachments/assets/33493456-f13c-4aa6-8660-8dbe4a469a3f)
![1](https://github.com/user-attachments/assets/1fa028fc-c2ea-4756-a608-cf180ad67769)
![2](https://github.com/user-attachments/assets/3443955c-458c-4607-88ca-c865ed87c504)



