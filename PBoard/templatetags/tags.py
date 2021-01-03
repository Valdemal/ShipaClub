from django import template
from django.db.models import Avg
from PBoard.models import Post, Rubric, Estimation
import math

register = template.Library()

@register.filter
def post_estimations_average(pk):
    return Estimation.objects.filter(post_id=pk).aggregate(Avg('value'))['value__avg']

@register.filter
def round(n):
    if n != None:
        n = str(math.floor(n * 10) / 10).replace(",",".")
        if n[-1] == '0':
            return n[0:-2]
        return n