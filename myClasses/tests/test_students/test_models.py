
import pytest
from apps.students.models import Student

@pytest.mark.django_db
def test_models():
    student_object = Student.objects.create(first_name="hamza")
    assert student_object.id