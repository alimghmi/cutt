import random
import string

ALL_CHARACTERS = string.ascii_letters

def random_slug(lenght):
    slug = ''.join(
        random.choice(ALL_CHARACTERS) for _ in range(lenght)
                )
    return slug

def generate_shorten_link(model, lenght=1):
    slug = random_slug(lenght)

    if model.objects.filter(slug=slug).exists():
        return generate_shorten_link(model, lenght+1)

    return slug

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

