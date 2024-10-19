// Handle rule creation
document.getElementById('rule-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const ruleString = document.getElementById('rule').value;

    // Send a POST request to create the rule
    fetch('http://127.0.0.1:5000/api/create_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rule_string: ruleString }) // Send the rule string in JSON format
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        if (data.ast) {
            console.log('Success:', data);
            document.getElementById('ast-diagram').innerText = JSON.stringify(data.ast, null, 2); // Display AST
            // Store AST globally for later use
            window.astData = data.ast;  // Save AST to global scope
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error during rule creation:', error);
    });
});

// Handle rule evaluation
document.getElementById('data-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Gather user data from the form
    const userData = {
        age: parseInt(document.getElementById('age').value, 10),
        department: document.getElementById('department').value,
        salary: parseInt(document.getElementById('salary').value, 10),
        experience: parseInt(document.getElementById('experience').value, 10),
    };

    // Check if AST data is available for evaluation
    if (!window.astData) {
        alert('Please create a rule first.');
        return;
    }

    // Send a POST request to evaluate the rule
    fetch('http://127.0.0.1:5000/api/evaluate_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ast: window.astData, user_data: userData }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        if (data.result !== undefined) {
            document.getElementById('result').innerText = `Evaluation Result: ${data.result}`;
        } else {
            alert(data.error);
        }
    })
    .catch(error => console.error('Error during rule evaluation:', error));
});