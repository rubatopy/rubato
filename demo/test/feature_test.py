"""A place to test new WIP features"""
import rubato as rb


class A:

    def replacement(self):
        """wow"""
        pass


@rb.deprecated("1.0.0", "2.0.0", A.replacement)
def test():
    """wow"""
    pass


print(test.__doc__)
test()
print("next thing")
