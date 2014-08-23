from django.contrib import admin
from collector.models import *
from django import forms


class AdminContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        widgets = {
            'probs_names': ProbsWidget(summorize=False),
        }


class AdminContest(admin.ModelAdmin):
    #fields = ['name', 'probs_names']
    form = AdminContestForm


class AdminResultForm(forms.ModelForm):
    class Meta:
        model = Result
        widgets = {
            'probs_scores': ProbsWidget,
        }


from django.utils.translation import ugettext_lazy as _


class ResultValidFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Valid')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'valid'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('Invalid', _('Invalid')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'Invalid':
            foo = [x.id for x in queryset if not x.valid()]
            return queryset.filter(id__in=foo)


class AdminResult(admin.ModelAdmin):
    form = AdminResultForm

    def normalize(modeladmin, request, queryset):
        for res in queryset: res.normalize()
    normalize.short_description = "Normalize"

    actions = [normalize]
    list_filter = [ResultValidFilter, 'grade', 'region']
    search_fields = ['name', 'region__name', 'region__slug']


class AdminMassRegionResults(admin.ModelAdmin):
    class Media:
        js = ('adminfix.js',)


class AdminRegion(admin.ModelAdmin):
    list_display = ['name', 'slug']

admin.site.register(Contest, AdminContest)
admin.site.register(Region, AdminRegion)
admin.site.register(Result, AdminResult)
admin.site.register(MassRegionResults, AdminMassRegionResults)