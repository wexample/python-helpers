from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path


def render_template(
    name: str,
    context: dict[str, Any] | None = None,
    search_paths: list[Path] | None = None,
) -> str:
    """Render a Jinja2 template by name, resolving across an ordered list of `search_paths`.

    The first path wins on direct lookup; `{% extends %}` falls through the remaining ones.
    Lets callers ship a default packaged template and let projects override it surgically:

        render_template(
            name="rules.j2",
            context={"app": ..., "agent": ...},
            search_paths=[
                app_workdir / ".wex/ai/prompts",                      # app override (optional)
                Path(package.__file__).parent / "resources/prompts",  # packaged default
            ],
        )

    The app override may itself do `{% extends "rules.j2" %}` — the ChoiceLoader hands it the
    packaged default since the first match (the app's own file) is excluded from the inheritance
    chain by Jinja's normal extends resolution.
    """
    from jinja2 import ChoiceLoader, Environment, FileSystemLoader

    paths = [p for p in (search_paths or []) if p.is_dir()]
    env = Environment(
        loader=ChoiceLoader([FileSystemLoader(p) for p in paths]),
        keep_trailing_newline=True,
        autoescape=False,
    )
    return env.get_template(name).render(**(context or {}))
