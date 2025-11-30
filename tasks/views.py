import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .scoring import calculate_task_score # Humne jo function banaya hai, use import kiya
from django.shortcuts import render
@csrf_exempt
def analyze_tasks(request):
    """
    Endpoint: /api/tasks/analyze/
    Method: POST. Accepts a list of tasks, calculates score, and returns sorted list.
    """
    if request.method == 'POST':
        try:
            # 1. Incoming JSON data ko load karo
            data = json.loads(request.body)
            tasks = data if isinstance(data, list) else []
            
            # 2. Har task ka score calculate karo
            processed_tasks = []
            for task in tasks:
                score = calculate_task_score(task)
                task['priority_score'] = score # Score task object mein add kiya
                processed_tasks.append(task)
            
            # 3. Score ke hisaab se sort karo (Highest score first)
            sorted_tasks = sorted(processed_tasks, key=lambda x: x['priority_score'], reverse=True)
            
            # 4. JSON response wapas bhejo
            return JsonResponse(sorted_tasks, safe=False)
        except json.JSONDecodeError:
            # Agar JSON format galat ho toh error do
            return JsonResponse({'error': 'Invalid JSON format in request body.'}, status=400)
    
    return JsonResponse({'error': 'POST method required for analysis.'}, status=405)

def suggest_tasks(request):
    """
    Endpoint: /api/tasks/suggest/
    Method: GET. Returns a simple text suggestion.
    """
    suggestion = {
        "message": "Focus on tasks due within 3 days with High Importance.",
        "strategy": "Urgency First"
    }
    return JsonResponse(suggestion)
def render_index(request):
    """
    Renders the main index.html file (the frontend).
    """
    return render(request, 'index.html')