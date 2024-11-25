"""
Functions that allow for communication with the search_gov database.
"""

import os

from pymysql import connect, Connection


def search_gov_db_connection(**extra_db_args) -> Connection:
    """Create connection to search_gov database"""

    return connect(
        host=os.environ["SEARCH_GOV_DB_HOST"],
        port=int(os.environ["SEARCH_GOV_DB_PORT"]),
        user=os.environ["SEARCH_GOV_DB_USER"],
        password=os.environ["SEARCH_GOV_DB_PASSWORD"],
        database=os.environ["SEARCH_GOV_DB_NAME"],
        **extra_db_args,
    )


def user_is_authorized(email: str) -> bool:
    """
    Query search_gov db to determine if this user is an active admin and thus authorized to
    access the UI.
    """

    query = (
        "SELECT email "
        "FROM   users "
        "WHERE  is_affiliate_admin = true "
        "AND    approval_status = 'approved' "
        "AND    email = %s"
    )

    with search_gov_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (email,))
            result_count = cursor.rowcount

    return bool(result_count)


print(user_is_authorized("admin@gsa.gov"))  # true  - email in db with proper values
print(user_is_authorized("non-admin@gsa.gov"))  # false - invalid is_affiliate_email
print(user_is_authorized("not-approved@gsa.gov"))  # false - invalid approval_status
print(user_is_authorized("knock-knock@nobodys.home"))  # false - email not in db
