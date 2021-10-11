class Process:
    @staticmethod
    def check_types(annotations, args):
        for arg in args.keys():
            if not isinstance(args[arg], annotations[arg]):
                raise TypeError(f"{args[arg]} is not of type {annotations[arg].__name__}")