class MissingThreshold(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'MissingThreshold, {0} '.format(self.message)
        else:
            return 'MissingThreshold has been raised'


class ThresholdOutOfRange(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'ThresholdOutOfRange, {0} '.format(self.message)
        else:
            return 'ThresholdOutOfRange has been raised'


class QTableNotSet(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'QTableNotSet, {0} '.format(self.message)
        else:
            return 'QTableNotSet has been raised'


class PlayerIndexOutOfRange(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'PlayerIndexOutOfRange, {0} '.format(self.message)
        else:
            return 'PlayerIndexOutOfRange has been raised'
