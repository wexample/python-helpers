def debug_trace() -> None:
    import traceback
    print(''.join(traceback.format_stack()))

def debug_trace_and_die() -> None:
    debug_trace()
    exit()

def dd() -> None:
    debug_trace_and_die()
