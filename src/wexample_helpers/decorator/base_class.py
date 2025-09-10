from typing import Callable, Optional, Type

import attrs


def base_class(_cls: Optional[Type] = None, *, slots: bool = False) -> Callable:
    def wrap(cls: Type) -> Type:
        return attrs.define(kw_only=True, slots=slots)(cls)

    if _cls is None:
        # usage: @base_class(slots=True)
        return wrap
    else:
        # usage: @base_class
        return wrap(_cls)
