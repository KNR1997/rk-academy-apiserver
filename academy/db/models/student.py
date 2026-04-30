# Django imports
from django.db import models

# Module imports
from .base import BaseModel


class Student(BaseModel):
    user = models.OneToOneField('db.User', on_delete=models.CASCADE)
    exam_year = models.IntegerField()
    student_number = models.CharField(max_length=20, unique=True)
    # Current academic information
    current_grade = models.ForeignKey(
        'db.GradeLevel', on_delete=models.PROTECT, related_name='current_students'
    )
    current_academic_year = models.ForeignKey(
        'db.AcademicYear', on_delete=models.PROTECT, related_name='current_students'
    )

    # Student personal information
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(
        ('male', 'Male'),
        ('female', 'Female'),
    ), blank=True, null=True)

    # Contact information
    parent_guardian_name = models.CharField(max_length=100, blank=True, null=True)
    parent_guardian_phone = models.CharField(max_length=15, blank=True, null=True)
    parent_guardian_email = models.EmailField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True, null=True)

    # Academic status
    enrollment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['student_number']

    def __str__(self):
        return f"{self.student_number}"

    def save(self, *args, **kwargs):
        if not self.student_number:
            # Get last two digits of exam year (e.g., 2026 -> 26)
            exam_year_short = str(self.exam_year)[-2:]

            # Find the last student with the same exam_year to get the next sequence number
            last_student = Student.objects.filter(
                exam_year=self.exam_year
            ).order_by('-student_number').first()

            if last_student and last_student.student_number:
                # Extract the sequence number from the last student_number
                # Assuming format like s26001, s26002, etc.
                try:
                    last_sequence = int(last_student.student_number[3:])  # Skip first 3 digits ('s' and year)
                    new_sequence = last_sequence + 1
                except (ValueError, IndexError):
                    # If parsing fails, start from 1
                    new_sequence = 1
            else:
                new_sequence = 1

            # Format: 's' + YY + 3-digit sequence with leading zeros (001, 002, etc.)
            self.student_number = f"s{exam_year_short}{new_sequence:03d}"

        super().save(*args, **kwargs)
