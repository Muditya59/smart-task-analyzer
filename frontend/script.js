// Function to fetch the initial suggestion text when the page loads
async function loadSuggestion() {
    try {
        const response = await fetch('/api/tasks/suggest/');
        const data = await response.json();
        document.getElementById('suggestion').innerText = `Suggestion: ${data.message}`;
    } catch (error) {
        console.error('Error loading suggestion:', error);
        document.getElementById('suggestion').innerText = 'Suggestion: API is loading...';
    }
}

// Function to determine the priority class for styling (used in displayResults)
function getPriorityClass(score) {
    if (score >= 80) {
        return 'priority-high';
    } else if (score >= 40) {
        return 'priority-medium';
    } else {
        return 'priority-low';
    }
}

// Function to dynamically display the sorted tasks in the UI
function displayResults(sortedTasks) {
    const taskListDiv = document.getElementById('taskList');
    taskListDiv.innerHTML = ''; // Purane results hatayein
    
    if (sortedTasks.length === 0) {
        document.getElementById('statusMessage').innerText = 'No tasks found after analysis.';
        return;
    }

    document.getElementById('statusMessage').innerText = `Found ${sortedTasks.length} tasks. Sorted by Priority Score:`;

    // Har sorted task ke liye card banayein
    sortedTasks.forEach((task, index) => {
        const priorityClass = getPriorityClass(task.priority_score);
        
        const card = document.createElement('div');
        card.className = `task-card ${priorityClass}`;
        card.innerHTML = `
            <h3>${index + 1}. ${task.title}</h3>
            <p><strong>Priority Score:</strong> ${task.priority_score}</p>
            <p><strong>Due Date:</strong> ${task.due_date}</p>
            <p><strong>Effort (hrs):</strong> ${task.estimated_hours} | 
            <strong>Importance (1-10):</strong> ${task.importance}</p>
        `;
        taskListDiv.appendChild(card);
    });
}


// MAIN FUNCTION: Called when the 'Analyze Priority' button is clicked
async function analyzeTasks() {
    const taskInput = document.getElementById('taskInput').value.trim();
    
    if (!taskInput) {
        alert("Please enter tasks in the JSON input area.");
        return;
    }

    try {
        document.getElementById('statusMessage').innerText = 'Analyzing tasks...';
        
        // 1. JSON string ko JavaScript object mein parse karein
        const tasks = JSON.parse(taskInput); 
        
        // 2. API ko POST request bhejein
        const response = await fetch('/api/tasks/analyze/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(tasks) // Data ko Django backend mein bhejein
        });
        
        // Agar response success na ho (e.g., 400 Bad Request)
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Server returned an error.');
        }

        const sortedTasks = await response.json();
        displayResults(sortedTasks); // 3. Sorted results display karein
        
    } catch (error) {
        console.error('Error during analysis:', error);
        document.getElementById('statusMessage').innerText = `Error: ${error.message}. Check console for details.`;
        alert(`Failed to analyze tasks. Please ensure your JSON format is correct.`);
    }
}

// Page load hone par suggestion function chalao
window.onload = loadSuggestion;

// Example JSON format for quick reference in the console:
console.log(`Example Input JSON: 
[
    { "title": "Urgent bug fix", "due_date": "2025-12-01", "importance": 10, "estimated_hours": 1 },
    { "title": "Low priority docs", "due_date": "2025-12-30", "importance": 2, "estimated_hours": 5 }
]
`);