class NameGenerator:
    NAME_NUMBER = 0
    FORMAT_STRING = "{name} {number}"

    @classmethod
    def get_name(cls, name: str) -> str:
        """
        Generates names with a counter
        """
        cls.NAME_NUMBER += 1
        return cls.FORMAT_STRING.format(name=name, number=cls.NAME_NUMBER)
