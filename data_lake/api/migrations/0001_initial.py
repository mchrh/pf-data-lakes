# Generated by Django 4.2.16 on 2024-11-21 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Campaign",
            fields=[
                (
                    "campaign_id",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("total_clicks", models.IntegerField(default=0)),
                ("total_cost", models.DecimalField(decimal_places=2, max_digits=10)),
                ("unique_users", models.IntegerField(default=0)),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
            ],
            options={
                "ordering": ["-start_date"],
            },
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "transaction_id",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("customer_id", models.CharField(max_length=100)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("transaction_date", models.DateTimeField()),
                ("is_high_value", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ["-transaction_date"],
            },
        ),
        migrations.CreateModel(
            name="WebLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField()),
                ("year", models.IntegerField()),
                ("month", models.IntegerField()),
                ("day", models.IntegerField()),
                ("hour", models.IntegerField()),
                ("request_count", models.IntegerField()),
                ("error_count", models.IntegerField()),
                ("total_bytes", models.BigIntegerField()),
            ],
            options={
                "ordering": ["-timestamp"],
                "indexes": [
                    models.Index(
                        fields=["year", "month", "day", "hour"],
                        name="api_weblog_year_a47ba7_idx",
                    )
                ],
            },
        ),
    ]