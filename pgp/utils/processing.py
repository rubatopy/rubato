class Process:
    @staticmethod
    def check_types(func, args):
        for arg in args.keys():
            if arg != "self" and arg[:2] != "__":
                if not isinstance(args[arg], func.__annotations__[arg]):
                    raise TypeError(f"{args[arg]} is not of type {func.__annotations__[arg].__name__}")