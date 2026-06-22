import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
print(json.dumps(list(User.objects.values('username', 'is_staff', 'is_superuser', 'is_active'))))
