from collector.models import *


def global_vars(request):
    return {
        'CONTEST': Contest.objects.first(),
        'REGIONS': Region.objects.all(),
    }