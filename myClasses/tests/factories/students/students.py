import factory 

from apps.students.models import Student


class StudentFactory(factory.DjangoModelFactory):
    first_name = "Hamza HADDAA"

    class Meta:
        model = Student