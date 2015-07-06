from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='lookup')
def cut(value, arg):
    return value[arg]
