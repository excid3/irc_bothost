from django import template
from common.models import BOT_TYPES, STATUS_TYPES

register = template.Library()

def split(list):
    """Splits a comma separated list"""
    return [(x.strip(), x.strip()[1:]) for x in list.split(",")]

def status(status):
    return STATUS_TYPES[status][1]
def type(type):
    for t, name in BOT_TYPES:
        if t == type:
            return name
    
register.filter("split", split)
register.filter("status", status)
register.filter("type", type)
