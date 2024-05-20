# Create your views here.
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CollaborationSession
import uuid
import json

import subprocess

def index(request):
    return JsonResponse({'message': 'Hello, world!'})


@csrf_exempt 
def generate_room_id(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')  # Get user ID from the request body
            
            if not user_id:
                return JsonResponse({'error': 'User ID is required'}, status=400)

            # Generate a unique room ID
            room_id = str(uuid.uuid4())

            # Create a collaboration session instance
            collaboration_session = CollaborationSession.objects.create(
                room_id=room_id,
                created_by=user_id  # Set the created_by field to the provided user ID
            )

            # Return the room ID in the response
            return JsonResponse({'room_id': room_id}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        # Return error for unsupported HTTP methods
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def run_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        language = data.get('language')
        print(language)
        code = data.get('code')

        try:
            if language == 'python':
                result = subprocess.run(['python', '-c', code], capture_output=True, text=True, timeout=10)
                return JsonResponse({'output': result.stdout + result.stderr})
            # Add other languages here
            else:
                return JsonResponse({'output': 'Unsupported language'}, status=400)

            return JsonResponse({'output': result.stdout + result.stderr})
        except subprocess.TimeoutExpired:
            return JsonResponse({'output': 'Code execution timed out'}, status=400)
        except Exception as e:
            return JsonResponse({'output': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
