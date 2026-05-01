from django.db import migrations


def seed_grade_levels(apps, schema_editor):
    GradeLevel = apps.get_model('db', 'GradeLevel')

    GradeLevel.objects.update_or_create(
        level='6',
        name='Grade 6',
    )

    GradeLevel.objects.update_or_create(
        level='7',
        name='Grade 7',
    )

    GradeLevel.objects.update_or_create(
        level='8',
        name='Grade 8',
    )

    GradeLevel.objects.update_or_create(
        level='9',
        name='Grade 9',
    )

    GradeLevel.objects.update_or_create(
        level='10',
        name='Grade 10',
    )

    GradeLevel.objects.update_or_create(
        level='11',
        name='Grade 11',
    )

    GradeLevel.objects.update_or_create(
        level='12',
        name='Grade 12',
    )

    GradeLevel.objects.update_or_create(
        level='13',
        name='Grade 13',
    )

    GradeLevel.objects.update_or_create(
        level='14',
        name='Grade 14',
    )


class Migration(migrations.Migration):
    dependencies = [
        ('db', '0014_conversation_message_conversation_latest_message_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_grade_levels),
    ]
