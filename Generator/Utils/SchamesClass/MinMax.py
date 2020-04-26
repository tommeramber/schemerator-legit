class MinMax:
    def __init__(self, minimum: int=(2**64)-1, maximum: int=0):
        self.minimum = minimum
        self.maximum = maximum

    def append(self, new_number):
        """
        This method get new number to append MinMax object by him.

        :param new_number: number must not be None!
        """
        self.minimum = min(self.minimum, new_number)
        self.maximum = max(self.maximum, new_number)

    def expand_integer_sizes(self):
        """
        This method expand the sizes to be in integer sizes.

        for example if you have minimum number that he between 0-255 he change him to 0.
        and if he between 255-65535 he change him to be 255.
        and if you have maximum value between 0-255 he change him to 255 and so on..
        """
        self.minimum = max([i for i in MinMax.expand_integer_sizes.SIZES_OF_INT if i <= self.minimum])
        self.maximum = min([i for i in MinMax.expand_integer_sizes.SIZES_OF_INT if i >= self.maximum])

    expand_integer_sizes.SIZES_OF_INT = [0, (2 ** 8) - 1, (2 ** 16) - 1, (2 ** 32) - 1, (2 ** 64) - 1]

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __ne__(self, other):
        return vars(self) != vars(other)

