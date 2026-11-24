import pytest
from students import add_student, get_student, average_grade

@pytest.fixture
def conn():
    from students import get_connection
    connection = get_connection()
    with connection.cursor() as cur:
        cur.execute("TRUNCATE TABLE students RESTART IDENTITY")
    connection.commit()

    yield connection

    connection.close()


def test_add_and_get_student(conn):
    add_student(conn, "Amel", 15)
    student = get_student(conn, 1)

    assert student[1] == "Amel"
    assert float(student[2]) == 15.0


def test_get_student_not_found(conn):
    student = get_student(conn, 999)

    assert student is None


def test_moyenne(conn):
    add_student(conn, "Amel", 10)
    add_student(conn, "Karim", 14)

    assert average_grade(conn) == 12.0