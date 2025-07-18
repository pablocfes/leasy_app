import json
from datetime import date, datetime
from django import template

register = template.Library()

def custom_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

@register.filter
def jsonify(value):
    return json.dumps(value, default=custom_serializer)