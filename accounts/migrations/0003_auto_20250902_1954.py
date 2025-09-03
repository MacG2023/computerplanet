from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_auto_20250902_1952"),  # replace with your last migration file
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="name",
            field=models.CharField(max_length=150, blank=True, null=True),
        ),
    ]
