import colorlog
import logging
import mysql.connector
from nano_logger.nano_logger import NanoLogger
from tqdm import tqdm


from mysql_text_search.classes.match_types import MatchTypes

class ProgressBarLoggingHandler(colorlog.StreamHandler):
    """ Handler for print messages in progressbar context. Loads
    'verbose' format from settings and appends color placeholder

    """

    def __init__(self, level=logging.DEBUG):
        super().__init__(level)

    def emit(self, record):
        try:
            # Loads verbose format from settings and append the color
            # placeholder
            # print(settings.LOGGING)
            colored_format = "%(log_color)s{}".format(
                '[%(asctime)s] %(levelname)s %(message)s - {%(module)s:%(funcName)s:%(lineno)d}'
            )
            # Init a new ColoredFormatter with the colored verbose format
            colored_formatter = colorlog.ColoredFormatter(colored_format)
            # Set the VerboseColoredFormatter to this handler
            self.setFormatter(colored_formatter)
            msg = self.format(record)
            tqdm.write(msg)
            self.flush()
        except Exception:
            self.handleError(record)
            exit(1)

logger = NanoLogger()

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
        # Logging instance

        # Colored handler for console logs messages in progress bar context
        tqdm_handler = ProgressBarLoggingHandler()

        internal_logger = logger._NanoLogger__logger
        internal_logger.addHandler(tqdm_handler)

        logger._NanoLogger__logger = internal_logger


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
            logger.debug("Fetch columns -> {}".format(fetch_query))
            cursor.execute(fetch_query)
            rows = cursor.fetchall()
            if len(rows) > 0:
                match_symbol = "LIKE"
                if case_sensitive:
                    match_symbol = "="

                match_type = self.__match_type
                term_template = MatchTypes.get_search_template(match_type)
                term = term_template.format(value_to_search)

                logger.info("Found {} columns...".format(len(rows)))
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
                logger.warning("No columns found")

        except Exception as e:
            logger.error(f"Errore nella query: {fetch_query}\n{e}")
            exit(1)

        results = []
        query_errors = {}
        # 3. Executing the queries
        for q in tqdm(query_mapping.keys()):
            try:
                query_params = query_mapping[q]
                logger.debug("Search '{}' in `{}`.`{}`".format(
                    value_to_search,
                    query_params['table'],
                    query_params['column']
                ))
                cursor.execute(q)
                rows = cursor.fetchall()
                if len(rows) > 0:
                    msg = "Match '{}' found {} times in `{}`.`{}`".format(
                        value_to_search,
                        len(rows),
                        query_params['table'],
                        query_params['column']
                    )
                    logger.info(msg)
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
