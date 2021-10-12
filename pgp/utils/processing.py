def check_types(func, args):
    for arg in args.keys():
        if arg != "self" and arg[:2] != "__":
            try:
                if func.__annotations__[arg] == any:
                    continue
                elif isinstance(func.__annotations__[arg], str):
                    if args[arg].__class__.__name__ != func.__annotations__[arg]:
                        raise TypeError(f"{args[arg]} is not of type {func.__annotations__[arg]} in {func.__name__}")
                elif not isinstance(args[arg], func.__annotations__[arg]):
                    raise TypeError(f"{args[arg]} is not of type {func.__annotations__[arg]} in {func.__name__}")
            except KeyError:
                raise SyntaxError(f"The argument {arg} does not have a type annotation. (Use any to bypass this)")
