from rest_framework import serializers
from .models import Student, Course, Enrollment


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "first_name", "age", "last_name", "email", "created_at"]

    def validate(self, attrs):
        first_name = attrs.get("first_name", self.instance.first_name if self.instance else "")
        last_name = attrs.get("last_name", self.instance.last_name if self.instance else "")
        age = attrs.get("age", self.instance.age if self.instance else None)
        email = attrs.get("email", self.instance.email if self.instance else "")

        if first_name.lower() == last_name.lower():
            raise serializers.ValidationError(
                "Ім'я та прізвище не можуть бути однаковими."
            )

        full_name = first_name + last_name
        if len(full_name) < 5:
            raise serializers.ValidationError(
                "Ім'я та прізвище разом повинні містити щонайменше 5 символів."
            )

        if age is not None and age < 18 and email.endswith("@company.com"):
            raise serializers.ValidationError(
                "Студенти молодше 18 років не можуть використовувати корпоративну пошту."
            )

        return attrs


class CourseSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "description", "duration", "students"]

    def validate(self, attrs):
        title = attrs.get("title", self.instance.title if self.instance else "").lower()
        description = attrs.get("description", self.instance.description if self.instance else "").lower()

        if title and description and description.count(title) > 2:
            raise serializers.ValidationError(
                "Назва курсу занадто часто повторюється в описі."
            )

        return attrs


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "student", "course", "enrollment_date"]
