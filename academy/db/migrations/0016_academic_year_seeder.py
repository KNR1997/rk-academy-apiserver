from django.db import migrations


def seed_academic_years(apps, schema_editor):
    AcademicYear = apps.get_model('db', 'AcademicYear')

    AcademicYear.objects.update_or_create(
        name='2024-2025',
        start_date='2024-01-01',
        end_date='2025-12-31',
    )
    AcademicYear.objects.update_or_create(
        name='2025-2026',
        start_date='2025-01-01',
        end_date='2026-12-31',
    )


class Migration(migrations.Migration):
    dependencies = [
        ('db', '0015_grade_level_seeder'),
    ]

    operations = [
        migrations.RunPython(seed_academic_years),
    ]
