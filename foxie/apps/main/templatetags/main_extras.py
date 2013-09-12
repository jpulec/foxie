from django import template
import re

url_regex = re.compile("^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([/\w\.\?=-]*)*\/?$")
youtube_regex = re.compile("^(https?:\/\/)?(www.)?youtube.com\/watch\?v=([/\w-]*)*\/?$")

register = template.Library()

@register.filter
def valid_url(value):
    return True if re.match(url_regex, value) else False

@register.filter
def full_url(value):
    if value.startswith("http"):
        return value
    else:
        return "http://" + value

@register.filter
def is_video(value):
    return True if re.match(youtube_regex, value) else False

@register.filter
def get_query_arg(value, param):
    url, query = value.split("?")
    queries = query.split("&")
    for q in queries:
        par, arg = q.split("=")
        if par == param:
            return arg
    return None

@register.filter
def is_image(value):
    return True if re.search(r'\.(jpg|jpeg|png|gif)$', value) else False
