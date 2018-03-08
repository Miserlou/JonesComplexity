def common_function(param, other):
    value = param + str(other)
    return value

def annotated_function(param: str, other: int) -> str:
    value: str = param + str(other)
    return value
