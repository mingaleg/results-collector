# Create your views here.

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from collector.models import Result, Region, Contest, MassRegionResults
from django.views.decorators.cache import cache_page
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def generate_results(request, template, region=None, page=None, grade=None, empty=None):
    if region is None:
        reg = None
        obj = Result.objects.order_by('-score', 'name')
    else:
        reg = get_object_or_404(Region, slug=region)
        obj = Result.objects.filter(region=reg).order_by('-score', 'name')

    if grade is not None:
        if grade in ('11', '10'):
            obj = obj.filter(grade=grade)
        elif grade == '9':
            obj = obj.filter(grade__in=['9','8','7','6','5','4','3','2','1'])

    obj = list(obj)
    #obj.sort()

    if not obj and empty:
        return render(request, empty, {'REGION': reg, 'GRADE': grade})

    if obj:
        obj[0].place = 1

    for i in range(1, len(obj)):
        if obj[i-1].score == obj[i].score:
            obj[i].place = obj[i-1].place
        else:
            obj[i].place = i+1

    paginator = Paginator(obj, 100)
    if page is None:
        page = request.GET.get('page')
    try:
        obj = paginator.page(page)
    except PageNotAnInteger:
        obj = paginator.page(1)
    except EmptyPage:
        obj = paginator.page(paginator.num_pages)

    NEEDS = {
        'PARTICIPANT': True,
        'REGION': True,
        'DAY_1': True,
        'DAY_1_SUM': True,
        'DAY_2': True,
        'DAY_2_SUM': True,
        'SUM': True,
        'GRADE': True,
    }
    if request.GET:
        foo = request.GET.dict()
        print(foo)
        for key, val in foo.items():
            if key in NEEDS:
                NEEDS[key] = val not in ('0', 'off', 'false')
    return render(request, template, {'RESULTS': obj, 'NEEDS': NEEDS, 'REGION': reg, 'GRADE': grade})


@cache_page(60*60*24*30)
def glob(request, grade=None):
    return generate_results(request, "semresults.html", grade=grade)


@cache_page(60*60*24*30)
def table_reg(request, reg, page, grade=None):
    return generate_results(request, "table.html", reg, page=page, grade=grade)


@cache_page(60*60*24*30)
def table_glob(request, page, grade=None):
    return generate_results(request, "table.html", page=page, grade=grade)


@cache_page(60*60*24*30)
def regionres(request, reg, grade=None):
    return generate_results(request, "semresults.html", reg, grade=grade, empty="region_links.html")


@cache_page(60*60*24*30)
def globcsv(request):
    return generate_results(request, "olympcsv.html")


@cache_page(60*60*24*30)
def regioncsv(request, reg):
    return generate_results(request, "olympcsv.html", reg)


@cache_page(60*60*24*30)
def regions(request):
    return render(request, 'map.html')


def apply_mass(request, pk):
    foo = get_object_or_404(MassRegionResults, pk=pk)
    try:
        foo.apply()
    except:
        return render(request, "mass_csv_rules.html")
    return redirect('/admin/collector/massregionresults/{}/'.format(pk))