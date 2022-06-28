from datetime import timedelta
from django.utils import timezone
from core.models import (Visitor, Viewer)


def datedelta(**kwrgs):
    return (timezone.now() - timedelta(**kwrgs))

def get_stats(user, slug):
    """
    Returns a dictionary with the following keys:
    - views: total number of views for the link
    - visitors: total number of unique views for the link
    """
    stats = {}
    context = {
        'total': None,
        'year': datedelta(days = 365),
        'month': datedelta(days = 30),
        'week': datedelta(days = 7),
        'yesterday': datedelta(days = 1),
        'today': timezone.now().replace(hour = 0, minute = 0, second = 0),
        'hour': datedelta(hours = 1),
    }

    visitors = Visitor.objects.filter(
                    views__link__user = user,
                    views__link__slug = slug
                    ).distinct()
    viewers = Viewer.objects.filter(
                    link__user = user,
                    link__slug = slug
                    )

    for obj, name in zip([visitors, viewers], ['visitors', 'views']):
        for key, value in context.items():
            if not name in stats:
                stats[name] = {}

            if value is None:
                stats[name][key] = obj.count()
                continue

            kwargs = {'views__viewed_at__gte' if name == 'visitors' else 'viewed_at__gte': value}
            stats[name][key] = obj.filter(**kwargs).count()

    return stats
