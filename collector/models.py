from django.db import models
from collector.separatedvaluesfield import SeparatedValuesField
from django.forms import widgets
import re


class Contest(models.Model):
    name = models.CharField(max_length=255)
    probs_names = SeparatedValuesField(max_length=511)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


class Region(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, default="", null=True, blank=True)

    exp_links = models.TextField(null=True, blank=True, default="")
    res_links = models.TextField(null=True, blank=True, default="")

    def status(self):
        if self.result_set.exists():
            return 1
        if self.res_links:
            return 2
        if self.exp_links:
            return 3
        return 0

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    def __lt__(self, other):
        return self.name < other.name

    def href(self):
        return '/region/{}/'.format(self.slug)

    def href_csv(self):
        return '/{}.csv'.format(self)


class MassRegionResults(models.Model):
    region = models.ForeignKey(Region)
    contest = models.ForeignKey(Contest, default=1, editable=False)
    raw = models.TextField()
    applied = models.BooleanField(default=False)

    def apply(self):
        if self.applied:
            raise Exception("Already applied")
        import io
        import csv
        csv_reader = csv.reader(io.StringIO(self.raw))
        for line in csv_reader:
            if len(line) != 10:
                raise Exception("Bad format")
            if '' in line:
                raise Exception("Bad format")
            Result.objects.create(
                name=line[0],
                grade=line[1],
                region=self.region,
                probs_scores=line[2:],
                mass=self,
            )
        self.applied = True
        self.save()

    def __unicode__(self):
        return str(self.region) + ('[Ожидает]' if not self.applied else '')

    def __str__(self):
        return self.__unicode__()


class ProbsWidget(widgets.MultiWidget):
    def __init__(self, attrs=None, summorize=True, cnt=8):
        self.cnt = cnt
        self.summorize = summorize
        _widgets = tuple(widgets.TextInput for i in range(cnt))
        super(ProbsWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        print(value)
        if not value:
            value = []
        while len(value) < self.cnt:
            value.append('0')
        return value

    def format_output(self, rendered_widgets):
        print(rendered_widgets)
        rend = u''.join(rendered_widgets)
        if self.summorize:
            def widgetid(src):
                return re.search('id="(?P<id>.*?)"', src).groupdict()['id']
            names = list(map(widgetid, rendered_widgets))
            wids = names[0][:names[0].rindex('_')]
            JS_SRC = "<script> var {}_inputs1 = [\n".format(wids)
            for name in names[:len(names)//2]:
                JS_SRC += "document.getElementById('{}'),\n".format(name)
            JS_SRC += "];\nvar {}_inputs2 = [\n".format(wids)
            for name in names[len(names)//2:]:
                JS_SRC += "document.getElementById('{}'),\n".format(name)
            JS_SRC += """];
            function {wids}_sumIt1() {{
                var sum1 = Array.prototype.reduce.call({wids}_inputs1, function (a, b) {{
                    return a + parseFloat(b.value);
                }}, 0);
                var sum2 = Array.prototype.reduce.call({wids}_inputs2, function (a, b) {{
                    return a + parseFloat(b.value);
                }}, 0);
                document.getElementById('{wids}_sum1').innerText = sum1;
                document.getElementById('{wids}_sum').innerText = sum1+sum2;
            }}

            Array.prototype.forEach.call({wids}_inputs1, function (input) {{
                input.addEventListener("keyup", {wids}_sumIt1, false);
            }});

            function {wids}_sumIt2() {{
                var sum1 = Array.prototype.reduce.call({wids}_inputs1, function (a, b) {{
                    return a + parseFloat(b.value);
                }}, 0);
                var sum2 = Array.prototype.reduce.call({wids}_inputs2, function (a, b) {{
                    return a + parseFloat(b.value);
                }}, 0);
                document.getElementById('{wids}_sum2').innerText = sum2;
                document.getElementById('{wids}_sum').innerText = sum1+sum2;
            }}

            Array.prototype.forEach.call({wids}_inputs2, function (input) {{
                input.addEventListener("keyup", {wids}_sumIt2, false);
            }});
            {wids}_sumIt1(); {wids}_sumIt2();
            </script>
            """.format(wids=wids)
            rend += "<span>[<span id='{wids}_sum1'></span>+<span id='{wids}_sum2'></span>=<span id='{wids}_sum'></span>]</span>".format(wids=wids)
            rend += JS_SRC
        return rend

    def value_from_datadict(self, data, files, name):
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        while datelist and not datelist[-1]:
            datelist.pop()
        return ','.join(datelist)


class Result(models.Model):
    name = models.CharField(max_length=255)
    contest = models.ForeignKey(Contest, default=1, editable=False)
    region = models.ForeignKey(Region)
    grade = models.CharField(max_length=255, blank=True, null=True)
    probs_scores = SeparatedValuesField(max_length=511)
    score = models.IntegerField(editable=False)
    mass = models.ForeignKey(MassRegionResults, blank=True, null=True)

    def valid(self):
        if len(self.probs_scores) != 8:
            return False
        if '' in self.probs_scores:
            return False
        return True

    def save(self, *args, **kwargs):
        self.score = sum(map(int, self.probs_scores))
        super(Result, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{name} [{grade}] ({region}): {score}".format(
            name=self.name,
            region=self.region,
            score=self.score,
            grade=self.grade,
        )

    def normalize(self):
        self.name = ' '.join(list(filter(None, self.name.split(' '))))
        #while len(self.probs_scores) != 8:
        #    self.score.append(0)
        self.save()

    def __str__(self):
        return self.__unicode__()

    def __lt__(self, other):
        return (-self.score, self.name, self.region) < (-other.score, other.name, other.region)

from django.db.models.signals import post_save, pre_save


def invalidate(sender, **kwargs):
    from django.core.cache import cache
    print(type(cache))
    cache.clear()

pre_save.connect(invalidate, sender=Result)
pre_save.connect(invalidate, sender=Region)
pre_save.connect(invalidate, sender=Contest)
