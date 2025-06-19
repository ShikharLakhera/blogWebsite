from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def create_superuser(request):
    User = get_user_model()

    if User.objects.filter(is_superuser=True).exists():
        return JsonResponse({'error': 'Superuser already exists'}, status=400)

    # Replace these with desired credentials
    username = "Chut"
    email = "admin@example.com"
    password = "selmonbhoi123"

    User.objects.create_superuser(username=username, email=email, password=password)
    return JsonResponse({'success': 'Superuser created successfully'})
