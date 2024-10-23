
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
![1](https://github.com/user-attachments/assets/0f5413d2-651d-4a58-b8ad-db2351e6dbe1)
![2](https://github.com/user-attachments/assets/eb10ddcc-8979-44ef-a70b-93088eab10ab)
![3](https://github.com/user-attachments/assets/b5c6af31-957f-4376-910f-0c113ef17189)
![4](https://github.com/user-attachments/assets/0b3bea50-5ad6-40dc-8bd7-98247ac413e4)
![5](https://github.com/user-attachments/assets/9883e2b9-0147-43e2-b24f-5c949290d785)
![6](https://github.com/user-attachments/assets/80b43619-ad00-4721-bfe9-e50f4ee09d0e)
![7](https://github.com/user-attachments/assets/dc1f0e96-f3e0-49c8-847b-264bae4918fe)
![8](https://github.com/user-attachments/assets/38cfb7d9-b034-49db-9c68-6befc3df7b10)


