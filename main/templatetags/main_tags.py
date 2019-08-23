from django import template
from datetime import datetime , time
import jalali_date
register = template.Library()

class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value

        return u""

@register.tag(name='set')
def set_var(parser, token):
    """
    {% set some_var = '123' %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")

    return SetVarNode(parts[1], parts[3])


@register.filter(name='totime')
def totime(value, time=None):
    time = value.time()
    return time



@register.filter(name='todate')
def todate(value,date=None):
    date = value.date()
    return date



@register.filter(name='prime')
def prime(value):
    prim = not value
    return prim


@register.filter(name='tojalali')
def tojalali(value,tojalali=None):
    tojalali = jalali_date.date2jalali(value)
    return tojalali



@register.filter(name='iran')
def iran(value,iran=None):
    iran = time.strftime(value,'%H:%M %p')
    iran = iran.replace('AM','صبح')
    iran = iran.replace('PM','عصر')
    return iran


@register.filter(name='convert_weekday')
def convert_weekday(value,convert_weekday=None):
    if value == 'jome':
        convert_weekday = 'جمعه'
    elif value == 'shanbe':
        convert_weekday = 'شنبه'
    elif value == 'yeshanbe':
        convert_weekday = 'یکشنبه'
    elif value == 'doshanbe':
        convert_weekday = 'دوشنبه'
    elif value == 'seshanbe':
        convert_weekday = 'سه شنبه'
    elif value == 'charshanbe':
        convert_weekday = 'چهارشنبه'
    elif value == 'panjshanbe':
        convert_weekday = 'پنجشنبه'

    return convert_weekday