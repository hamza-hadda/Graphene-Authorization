
import pytest
from tests.factories.students.students import StudentFactory

@pytest.mark.django_db
def test_models():
    student_object = StudentFactory()
    assert student_object.id