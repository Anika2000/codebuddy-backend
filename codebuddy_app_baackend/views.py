# Create your views here.
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CollaborationSession
import uuid
import json
import tempfile
import subprocess
import os

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
            elif language == 'javascript':
                result = subprocess.run(['node', '-e', code], capture_output=True, text=True, timeout=10)
                return JsonResponse({'output': result.stdout + result.stderr})
            elif language == 'java':
                with tempfile.NamedTemporaryFile(suffix=".java", delete=False) as temp_source:
                    temp_source.write(code.encode('utf-8'))
                    source_file_name = temp_source.name

                compile_result = subprocess.run(['javac', source_file_name], capture_output=True, text=True)
                if compile_result.returncode != 0:
                    return JsonResponse({'output': compile_result.stdout + compile_result.stderr}, status=400)

                class_file_name = source_file_name[:-5]  # Remove .java extension

                result = subprocess.run(['java', '-cp', os.path.dirname(source_file_name), os.path.basename(class_file_name)], capture_output=True, text=True, timeout=10)
                os.remove(source_file_name)
                os.remove(class_file_name + ".class")
                return JsonResponse({'output': result.stdout + result.stderr})


            elif language == 'c':
                with tempfile.NamedTemporaryFile(suffix=".c", delete=False) as temp_source:
                    temp_source.write(code.encode('utf-8'))
                    source_file_name = temp_source.name

                binary_file_name = source_file_name[:-2]  # Remove .c extension

                compile_result = subprocess.run(['gcc', source_file_name, '-o', binary_file_name, '-lm'], capture_output=True, text=True)
                if compile_result.returncode != 0:
                    return JsonResponse({'output': compile_result.stdout + compile_result.stderr}, status=400)

                result = subprocess.run([binary_file_name], capture_output=True, text=True, timeout=10)
                os.remove(source_file_name)
                os.remove(binary_file_name)
                return JsonResponse({'output': result.stdout + result.stderr})

            elif language == 'cpp':
                with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False) as temp_source:
                    temp_source.write(code.encode('utf-8'))
                    source_file_name = temp_source.name

                binary_file_name = source_file_name[:-4]  # Remove .cpp extension

                compile_result = subprocess.run(['g++', source_file_name, '-o', binary_file_name, '-lm'], capture_output=True, text=True)
                if compile_result.returncode != 0:
                    return JsonResponse({'output': compile_result.stdout + compile_result.stderr}, status=400)

                result = subprocess.run([binary_file_name], capture_output=True, text=True, timeout=10)
                os.remove(source_file_name)
                os.remove(binary_file_name)
                return JsonResponse({'output': result.stdout + result.stderr})

            else:
                return JsonResponse({'output': 'Unsupported language'}, status=400)

            
        except subprocess.TimeoutExpired:
            return JsonResponse({'output': 'Code execution timed out'}, status=400)
        except Exception as e:
            return JsonResponse({'output': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
