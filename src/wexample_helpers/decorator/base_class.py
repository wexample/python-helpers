import attrs


def base_class(cls):
    return attrs.define(kw_only=True)(cls)
