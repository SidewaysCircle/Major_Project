from django import template
from django.contrib.auth.models import Group 

register = template.Library()

@register.filter(name='no_group')
def no_group(user, group_name): 
    group = Group.objects.get(name=group_name)
    return False if group in user.groups.all() else True
