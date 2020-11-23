# coding=utf-8

def camel_to_underline(camel_format):
    """
        驼峰命名格式转下划线命名格式
    """
    underline_format = ''
    if isinstance(camel_format, str):
        for _s_ in camel_format:
            underline_format += _s_ if _s_.islower() else '_' + _s_.lower()
    return underline_format


def underline_to_camel(underline_format):
    """
        下划线命名格式转驼峰命名格式
    """
    camel_format = ''
    if isinstance(underline_format, str):
        for _s_ in underline_format.split('_'):
            camel_format += _s_.capitalize()
    return camel_format


def underline_to_lower_camel(underline_format):
    """
        下划线命名格式转驼峰命名格式(小)
    """
    camel_format = ''
    if isinstance(underline_format, str):
        for _s_ in underline_format.split('_'):
            camel_format += _s_.capitalize()
    return camel_format[0].lower() + camel_format[1:]
