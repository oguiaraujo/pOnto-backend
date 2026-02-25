from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()

with open('.env', 'w') as f:
    f.write(f'DJANGO_SECRET_KEY={secret_key}\n')
    f.write('DJANGO_DEBUG=False\n')

print('.env criado com sucesso!')