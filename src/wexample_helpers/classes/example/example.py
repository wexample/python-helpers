from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.mixin.with_path_mixin import WithPathMixin


@base_class
class Example(WithPathMixin):
    def execute(self) -> None:
        pass
