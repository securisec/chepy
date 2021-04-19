from chepy import Chepy

DB_FILE = "tests/files/test.db"


def test_sqlite_get_columns():
    assert len(Chepy(DB_FILE).sqlite_get_columns("customers").o) == 13


def test_sqlite_get_tables():
    assert len(Chepy(DB_FILE).sqlite_get_tables().o) == 13


def test_sqlite_dump_table():
    assert len(Chepy(DB_FILE).sqlite_dump_table("customers").o) == 59

def test_sqlite_query():
    assert len(Chepy(DB_FILE).sqlite_query("select * from customers where company is not null").o) == 10
