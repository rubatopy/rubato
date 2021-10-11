def check_types(func, args):
    for arg in args.keys():
        if arg != "self" and arg[:2] != "__":
            try:
                if func.__annotations__[arg] == any:
                    continue
                if not isinstance(args[arg], func.__annotations__[arg]):
                    raise TypeError(f"{args[arg]} is not of type {func.__annotations__[arg].__name__}")
            except KeyError:
                raise SyntaxError(f"The argument {arg} does not have a type annotation. (Use any to bypass this)")
