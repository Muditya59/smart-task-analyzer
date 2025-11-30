# Smart Task Analyzer (Singularium Technologies Assignment)

This is a mini-application built using Python/Django and Vanilla JavaScript/HTML/CSS to analyze a list of tasks and prioritize them based on a custom scoring algorithm.

---

## 1. Technical Stack

* **Backend:** Python 3.x, Django 5.x
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Database:** SQLite (Default)

---

## 2. Setup and Installation Guide

Follow these steps to run the application locally:

1.  **Clone or Download:** Get the project files.
2.  **Setup Environment:**
    ```bash
    cd task-analyzer
    python -m venv venv
    # Activate venv: source venv/bin/activate (or venv\Scripts\activate on Windows)
    pip install django
    ```
3.  **Run Migrations:**
    ```bash
    python manage.py makemigrations tasks
    python manage.py migrate
    ```
4.  **Start Server:**
    ```bash
    python manage.py runserver
    ```
5.  **Access App:** Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## 3. The Custom Prioritization Algorithm

The core logic resides in `tasks/scoring.py`. The algorithm calculates a composite **`priority_score`** for each task by weighing three main factors: Urgency, Importance, and Effort.

**Formula Overview:**
$$\text{Priority Score} = \text{Urgency Factor} + \text{Importance Factor} + \text{Effort Factor}$$

### **A. Urgency Factor (Highest Weight)**
* **Why Urgency is Weighted More:** Urgency (especially being overdue or due today) is given the highest weight because the goal is to help the user decide "what to work on first" to meet deadlines and prevent immediate failures.
* **Scoring Breakdown:**
    * **Overdue:** +100 points
    * **Due Today:** +75 points
    * **Due in 1-3 days:** +50 points
    * **Due in 4-7 days:** +20 points

### **B. Importance Factor (Medium Weight)**
* **Calculation:** Importance (1-10 scale) is multiplied by a **weight of 5**.
    * *Example:* Importance 10 gives 50 points (10 * 5).

### **C. Effort Factor (Quick Wins Bonus)**
* **Logic:** This factor rewards "quick wins"—tasks that can be completed quickly to build momentum.
* **Scoring Breakdown:**
    * **Estimated Hours < 2:** +15 points (Bonus for quick tasks)
    * **Estimated Hours > 8:** -5 points (Slight penalty for very large tasks)

---

## 4. Edge Case Handling

* **Past Due Dates:** Any task with a due date in the past receives the maximum Urgency score (+100) to ensure it gets top priority.
* **Missing Data:** If `importance` or `estimated_hours` are missing in the input JSON, the logic defaults to safe values (Importance=5, Estimated Hours=1) to prevent crashes.