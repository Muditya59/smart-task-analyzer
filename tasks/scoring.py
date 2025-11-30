from datetime import datetime, date

def calculate_task_score(task_data):
    """
    Calculates a priority score based on Urgency, Importance, and Effort.
    Higher score = Higher priority.
    """
    score = 0
    
    # --- 1. Urgency Calculation ---
    try:
        # Incoming date is expected as a string "YYYY-MM-DD" from JSON
        due_date_val = task_data.get('due_date')
        if isinstance(due_date_val, str):
            due_date_obj = datetime.strptime(due_date_val, '%Y-%m-%d').date()
        else:
            # Handle if it somehow comes as a date object (less likely from API)
            due_date_obj = due_date_val

        today = date.today()
        # Calculate days difference
        days_until_due = (due_date_obj - today).days

        if days_until_due < 0:
            score += 100  # OVERDUE! Huge priority boost
        elif days_until_due == 0:
            score += 75   # Due today
        elif days_until_due <= 3:
            score += 50   # Due very soon
        elif days_until_due <= 7:
            score += 20   # Due this week
    except Exception:
        # If date is missing or invalid, we add no score for urgency
        score += 0

    # --- 2. Importance Weighting ---
    # Importance is 1-10.
    importance = int(task_data.get('importance', 5)) # Default to 5 if missing
    score += (importance * 5) # Gives a maximum of 50 points

    # --- 3. Effort (Quick wins logic) ---
    estimated_hours = int(task_data.get('estimated_hours', 1)) # Default to 1 hour
    if estimated_hours < 2:
        score += 15  # Bonus for quick tasks
    elif estimated_hours > 8:
        score -= 5   # Slight penalty for tasks taking more than a day

    return score