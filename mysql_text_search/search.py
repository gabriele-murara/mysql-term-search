import mysql.connector
from tqdm import tqdm

from mysql_text_search.classes.match_types import MatchTypes


class MySQLTextSearch:

    def __init__(self, **kwargs):
        self.__database_name = kwargs.get('database_name', None)
        self.__database_host = kwargs.get('database_host', None)
        self.__database_user = kwargs.get('database_user', None)
        self.__database_password = kwargs.get('database_password', None)
        self.__database_port = kwargs.get('database_port', None)
        self.__case_insensitive_search = kwargs.get(
            'case_insensitive_search', None
        )
        self.__match_type = kwargs.get('match_type', None)
        self.__query_errors = {}


    def search(self, value_to_search):

        self.__query_errors = {}
        conn = mysql.connector.connect(
            host=self.__database_host,
            user=self.__database_user,
            password=self.__database_password,
            database=self.__database_name,
        )

        case_sensitive = not self.__case_insensitive_search
        columns = ""

        cursor = conn.cursor()
        queries = []

        fetch_query = """
                SELECT 
                    `table_name`, 
                    `column_name`, 
                    `data_type`, 
                    `character_maximum_length` 
                FROM `information_schema`.`columns` 
                WHERE (`data_type` = 'varchar' OR `data_type` = 'text') 
                AND `table_schema` = '{}'; 
            """

        query_mapping = {}
        try:
            fetch_query = fetch_query.format(self.__database_name)
            print("Fetch columns -> {}".format(fetch_query))
            cursor.execute(fetch_query)
            rows = cursor.fetchall()
            if len(rows) > 0:
                match_symbol = "LIKE"
                if case_sensitive:
                    match_symbol = "="

                match_type = self.__match_type
                term_template = MatchTypes.get_search_template(match_type)
                term = term_template.format(value_to_search)

                print("Found {} columns...".format(len(rows)))
                for r in rows:
                    table_name = r[0]
                    column_name = r[1]

                    q = "SELECT '{}' AS table_name, '{}' AS column_name "
                    q += "FROM `{}` WHERE `{}` {} {};"
                    formatted_query = q.format(
                        table_name,
                        column_name,
                        table_name,
                        column_name,
                        match_symbol,
                        term
                    )
                    queries.append(formatted_query)

                    query_mapping[formatted_query] = {
                        'column': column_name,
                        'table': table_name
                    }
            else:
                print("No columns found")

        except Exception as e:
            print(f"Errore nella query: {fetch_query}\n{e}")
            exit(1)

        results = []
        query_errors = {}
        # 3. Executing the queries
        for q in tqdm(query_mapping.keys()):
            try:
                # print("Eseguo {}".format(q))
                cursor.execute(q)
                rows = cursor.fetchall()
                if len(rows) > 0:
                    query_params = query_mapping[q]
                    results.append({
                        'query': q,
                        'rows': len(rows),
                        'column': query_params['column'],
                        'table': query_params['table'],
                    })
            except Exception as e:
                self.__query_errors[q] = e

        # 5. Clean
        cursor.close()
        conn.close()
        return results

    @property
    def database_name(self):
        return self.__database_name

    @database_name.setter
    def database_name(self, value):
        self.__database_name = value

    @property
    def database_host(self):
        return self.__database_host

    @database_host.setter
    def database_host(self, value):
        self.__database_host = value

    @property
    def database_user(self):
        return self.__database_user

    @database_user.setter
    def database_user(self, value):
        self.__database_user = value

    @property
    def database_password(self):
        return self.__database_password

    @database_password.setter
    def database_password(self, value):
        self.__database_password = value

    @property
    def database_port(self):
        return self.__database_port

    @database_port.setter
    def database_port(self, value):
        self.__database_port = value

    @property
    def case_insensitive_search(self):
        return self.__case_insensitive_search

    @case_insensitive_search.setter
    def case_insensitive_search(self, value):
        self.__case_insensitive_search = value

    @property
    def match_type(self):
        return self.__match_type

    @match_type.setter
    def match_type(self, value):
        self.__match_type = value

    @property
    def query_errors(self):
        return self.__query_errors
