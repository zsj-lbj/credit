from django import template

register = template.Library()#创建模板对象


@register.simple_tag()
# 这里最好使用simple_tag(),使用tag会很复杂
def add(v1,v2):
    return v1+v2

@register.filter()
def reversal(v1):
    return v1[::-1]

#相当于由@register.inclusion_tag完成render(request,'zujian.html',{'data':v1})的功能
@register.inclusion_tag('zujian.html')
def show(v1):
    return {'data':v1}