from django import template

register = template.Library()


@register.filter
def scoring(value):
    try:
        value = int(value)
        if value == 100:
            cls = 'solved'
        elif value == 0:
            cls = 'unsolved'
        else:
            cls = 'partially'
        return '<span class="{cls}">{score}</span>'.format(cls=cls, score=value)
    except:
        return ''

@register.filter
def score_class(value):
    try:
        value = int(value)
        if value == 100:
            cls = 'positive'
        elif value == 0:
            cls = 'negative'
        else:
            cls = 'warning'
        return cls
    except:
        return ''

@register.filter
def day(value, arg):
    try:
        arg = int(arg)-1
        foo = value[len(value)//2*arg:len(value)//2*(arg+1)]
        return foo
    except:
        return []

@register.filter
def daysum(value, arg):
    try:
        arg = int(arg)-1
        return sum(map(int, value.probs_scores[len(value.probs_scores)//2*arg:len(value.probs_scores)//2*(arg+1)]))
    except:
        return []

@register.filter
def nobreak(value):
    return str(value).replace(" ", u"\u00A0")

@register.filter
def pages(value, arg):
    pass


@register.filter
def placer(value):
    places = [x+1 for x in range(len(value))]
    for i in range(1, len(value)):
        if value[i-1].score == value[i].score:
            places[i] = places[i-1]
    return [{"place": place, "results": res} for place, res in zip(places,value)]


@register.filter
def linebreaker(value):
    return filter(None, value.split('\n'))