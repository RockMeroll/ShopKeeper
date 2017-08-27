# coding=utf-8
from django import template
from Utils import utils

register = template.Library()


@register.filter(name='key')
def key(d, key_name):
    if key_name == 'VisitingInfo:LastVisit':
        value = d[key_name].value
    elif key_name == "VisitingInfo:VisitCycle":
        value = utils.second_to_time(d[key_name].value)
    elif key_name == "VisitingInfo:StayInTime":
        value = utils.second_to_time(d[key_name].value)
    elif key_name == "VisitingInfo:Liveness":
        value = utils.liveness_tran(d[key_name].value)

    else:
        value = 0

    return value


@register.filter(name='key_for_config')
def key_for_config(d, key):
    try:
        value = d[key]
    except KeyError:
        value = 0
    return value
