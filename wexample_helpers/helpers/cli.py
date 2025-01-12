def cli_make_clickable_path(path: str) -> str:
    # \033]8;;file://{path}\033\\  : début du lien
    # \033]8;;\033\\              : fin du lien
    return f"\033]8;;file://{path}\033\\{path}\033]8;;\033\\"
