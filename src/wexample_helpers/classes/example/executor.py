from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.helpers.module import module_load_class_from_file_if_exist
from wexample_helpers.helpers.string import string_to_pascal_case
from wexample_helpers.mixin.with_entrypoint_path_mixin import WithEntrypointPathMixin
from wexample_helpers.service.mixins.registry_container_mixin import RegistryContainerMixin


@base_class
class Executor(WithEntrypointPathMixin, RegistryContainerMixin):
    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        registry = self.get_registry('examples')

        self.entrypoint_path = self.entrypoint_path.parent

        for path in self.entrypoint_path.iterdir():
            example_module = module_load_class_from_file_if_exist(
                file_path=path,
                class_name=string_to_pascal_case(path.name)
            )

            if example_module:
                registry.register(
                    key=path.name,
                    item=example_module
                )

    def execute(self) -> None:
        for example in self.get_registry('examples').get_all():
            print(type(example))
