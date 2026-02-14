import argparse

from mysql_text_search import settings
from mysql_text_search.classes.match_types import MatchTypes
from mysql_text_search.classes.version import get_version
from mysql_text_search.search import MySQLTextSearch

def main():
    program_name = "Faster database search tool v. {}".format(
        get_version()
    )

    parser = argparse.ArgumentParser(
        description=program_name,
        add_help=False
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {get_version()}",
    )

    parser.add_argument(
        'term',
        type=str,
        help='The term to search'
    )

    parser.add_argument(
        "-n",
        '--database',
        dest='database_name',
        type=str,
        help='The name of the database',
        default=settings.DB_NAME
    )
    parser.add_argument(
        "-h",
        '--host',
        dest='database_host',
        type=str,
        help='The host of the database',
        default=settings.DB_HOST
    )
    parser.add_argument(
        "-p",
        '--port',
        dest='database_port',
        type=int,
        default=3306,
        help='The port of the database'
    )
    parser.add_argument(
        "-u",
        '--user',
        dest='database_user',
        type=str,
        help='The user of the database',
        default=settings.DB_USER
    )
    parser.add_argument(
        "-P",
        '--password',
        dest='database_password',
        type=str,
        help='The password of the database',
        default=settings.DB_PASSWORD
    )
    parser.add_argument(
        "-i",
        '--case_insensitive',
        action="store_true",
        help="Match by case insensitive",
        default=False
    )

    parser.add_argument(
        "-t",
        "--match-type",
        choices=MatchTypes.get_type_names(),
        dest='match_type',
        default="exact",
        help="Matching type to use"
    )

    parser.add_argument(
        "--help",
        action="help",
        help="Show this help message"
    )

    args = parser.parse_args()

    msg = "Start to search term '{}' by case '{}' with match type '{}' "
    msg += "on db: '{}' user: '{}' host: '{}' with  password: "

    case_sensitive_label = "sensitive"
    if args.case_insensitive:
        case_sensitive_label = "in-sensitive"
    msg = msg.format(
        args.term,
        case_sensitive_label,
        args.match_type,
        args.database_name,
        args.database_user,
        args.database_host
    )

    if args.database_password:
        msg += "YES"
    else:
        msg += "NO"
    print(msg)

    search = MySQLTextSearch(
        database_name=args.database_name,
        database_user=args.database_user,
        database_password=args.database_password,
        database_host=args.database_host,
        case_insensitive_search=args.case_insensitive,
        match_type=args.match_type
    )

    results = search.search(args.term)

    print("[+] Match found")
    if len(results) <= 0:
        print("\tNo results")
    for r in results:
        print("\t`{}`.`{}` -> {}".format(
            r['table'], r['column'], r['rows']
        ))

    if len(search.query_errors) > 0:
        print("[-] Errors .................................................: ")
        for q, e in search.query_errors.items():
            msg = "{} -> Query: {}".format(e, q)
            print(msg)
