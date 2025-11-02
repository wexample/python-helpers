from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.mixin.with_path_mixin import WithPathMixin
from wexample_helpers.service.registry import RegistrableType


@base_class
class Example(WithPathMixin, RegistrableType):

    def execute(self) -> None:
        # TODO
        print('execute')
