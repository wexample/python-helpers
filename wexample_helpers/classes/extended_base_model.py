from wexample_helpers.classes.mixin.printable_mixin import PrintableMixin
from wexample_helpers.classes.unique_base_model import UniqueBaseModel


class ExtendedBaseModel(PrintableMixin, UniqueBaseModel):
    pass
