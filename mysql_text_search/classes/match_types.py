class MatchTypes:

    EXACT = 'exact'
    CONTAINS = 'contains'
    STARTS_WITH = 'starts_with'
    ENDS_WIDTH = 'ends_width'

    @staticmethod
    def get_type_names():
        return [
            MatchTypes.EXACT,
            MatchTypes.CONTAINS,
            MatchTypes.STARTS_WITH,
            MatchTypes.ENDS_WIDTH,
        ]

    @staticmethod
    def get_mapping():
        return {
            MatchTypes.EXACT: "'{}'",
            MatchTypes.CONTAINS: "'%{}%'",
            MatchTypes.STARTS_WITH: "'{}%'",
            MatchTypes.ENDS_WIDTH: "'%{}'",
        }

    @staticmethod
    def get_search_template(type_name):
        if type_name not in MatchTypes.get_type_names():
            raise ValueError(
                "Type name for -> '{}' not found".format(type_name)
            )
        return MatchTypes.get_mapping()[type_name]


    