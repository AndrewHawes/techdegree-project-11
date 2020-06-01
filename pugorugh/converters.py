class SignedIntConverter:
    regex = r'-?\d+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%d' % value


class StatusConverter:
    regex = r'liked|disliked|undecided'

    def to_python(self, value):
        return str(value)

    def to_url(self, value):
        return '%s' % value
