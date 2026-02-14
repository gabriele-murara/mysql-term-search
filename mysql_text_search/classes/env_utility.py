class EnvUtility:

    @staticmethod
    def to_boolean(value):
        if isinstance(value, bool):
            return value

        true_valid_values = [
            '1',
            'true',
            'yes'
        ]

        if str(value).lower() in true_valid_values:
            return True
        return False
