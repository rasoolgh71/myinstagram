#from django import template
#register = template.Library()
from django import template
import re
import os
import datetime
import time
register=template.Library()



@register.filter(name='time_convert')
def time_convert(value, arg=""):
    list1=[]
    print("value",value)
    print(value.year)
    print(value.second)
    print(value.month)
    t = datetime.datetime(value.year,value.month,value.day, value.hour,value.minute,value.second)
    time1=time.mktime(t.timetuple())*1000
    print(time1)
    return time1


