from collections.abc import Iterable
from pathlib import Path

from wexample_helpers.classes.example.example import Example
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.helpers.module import module_load_class_from_file_if_exist
from wexample_helpers.helpers.string import string_to_pascal_case
from wexample_helpers.mixin.with_entrypoint_path_mixin import WithEntrypointPathMixin
from wexample_helpers.service.mixins.registry_container_mixin import RegistryContainerMixin


@base_class
class Executor(WithEntrypointPathMixin, RegistryContainerMixin):
    filters: tuple[str, ...] | None = public_field(
        default=None,
        description="Optional list of substrings to select which examples to run.",
    )

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        self._normalise_filters()
        examples_registry = self.get_registry("examples")
        examples_dir = Path(self.entrypoint_path).parent

        for path in sorted(examples_dir.iterdir()):
            if not path.is_file() or path.suffix != ".py":
                continue
            if path.name in {"__init__.py", "__main__.py"} or path.name.startswith("_"):
                continue

            example_class = module_load_class_from_file_if_exist(
                file_path=path,
                class_name=string_to_pascal_case(path.stem),
            )

            if not isinstance(example_class, type) or not issubclass(
                    example_class, self._get_example_class_type()
            ):
                continue

            examples_registry.register(
                key=path.stem,
                item=example_class(path=path),
            )

    def _get_example_class_type(self) -> type[Example]:
        return Example

    def execute(self) -> None:
        examples_registry = self.get_registry("examples")
        matched = False
        for key, example in examples_registry.get_all().items():
            if not self._should_run_example(key, example):
                continue
            matched = True
            print(f"Running example: {key}")
            example.execute()

        if self.filters and not matched:
            filters = ", ".join(self.filters)
            print(f"No examples matched filters: {filters}")

    def _normalise_filters(self) -> None:
        raw_filters = self.filters

        if raw_filters is None or (isinstance(raw_filters, str) and not raw_filters.strip()):
            self.filters = None
            self._filters_lower: tuple[str, ...] = ()
            return

        if isinstance(raw_filters, str):
            tokens: Iterable[str] = (raw_filters,)
        elif isinstance(raw_filters, Iterable):
            tokens = raw_filters
        else:
            tokens = (str(raw_filters),)

        cleaned = tuple(
            filter(
                None,
                (str(token).strip() for token in tokens),
            )
        )

        self.filters = cleaned or None
        self._filters_lower = (
            tuple(f.lower() for f in cleaned) if cleaned else ()
        )

    def _should_run_example(self, key: str, example: Example) -> bool:
        if not self.filters:
            return True
        key_lower = key.lower()
        class_name = example.__class__.__name__.lower()
        return any(token in key_lower or token in class_name for token in self._filters_lower)
