from wexample_helpers.classes.mixin.printable_mixin import PrintableMixin
from wexample_helpers.classes.unique_base_model import UniqueBaseModel


class ExtendedBaseModel(PrintableMixin, UniqueBaseModel):
    """Base model with pragmatic conveniences.

    - Provides a concise AttributeError for missing attributes so that the
      error points to user code instead of deep inside pydantic internals.
    """

    def __getattr__(self, item):
        """Defer to pydantic then reformat the missing-attribute error concisely.

        We first call the parent implementation (BaseModel) so any custom
        behaviour stays intact. If it raises AttributeError, we re-raise a
        short, user-facing message without the pydantic-internals chain.
        """
        try:
            return super().__getattr__(item)
        except AttributeError as e:
            cls_name = type(self).__name__
            new_exc = AttributeError(f"{cls_name} has no attribute '{item}'")
            tb = e.__traceback__
            # Skip the current __getattr__ frame to point to caller site when possible
            if tb is not None and tb.tb_next is not None:
                raise new_exc.with_traceback(tb.tb_next) from None
            raise new_exc from None
