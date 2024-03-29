# Generated by Django 4.1.1 on 2023-01-09 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Competition",
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
                (
                    "name",
                    models.CharField(
                        help_text="Name of the competition.", max_length=200
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Rules of the competition and description of the task,",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("NEW", "In preparation"),
                            ("OPEN", "Open"),
                            ("CLOSED", "Closed"),
                            ("DELETED", "Deleted"),
                        ],
                        default="NEW",
                        max_length=24,
                    ),
                ),
                (
                    "token",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Token for run submissions",
                        max_length=200,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Contest",
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
                (
                    "name",
                    models.CharField(help_text="Name of the contest. ", max_length=200),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Short description of the contest, such as time and place",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("NEW", "In preparation"),
                            ("OPEN", "Open"),
                            ("CLOSED", "Closed"),
                            ("DELETED", "Deleted"),
                        ],
                        default="NEW",
                        max_length=24,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Team",
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
                (
                    "name",
                    models.CharField(
                        help_text="Identifier of the team", max_length=200
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, default="", help_text="Team members and affiliation"
                    ),
                ),
                (
                    "token",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Token for run submissions",
                        max_length=200,
                        unique=True,
                    ),
                ),
                (
                    "contest",
                    models.ForeignKey(
                        help_text="a team belongs to a contest",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contest.contest",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Run",
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
                ("start_time", models.DateTimeField()),
                ("duration", models.IntegerField(blank=True)),
                (
                    "score",
                    models.IntegerField(
                        blank=True, help_text="Assigned by a Judge", null=True
                    ),
                ),
                (
                    "judge_comment",
                    models.CharField(
                        blank=True, help_text="Comment by a Judge", max_length=200
                    ),
                ),
                (
                    "competition",
                    models.ForeignKey(
                        help_text="source competition",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contest.competition",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        help_text="Who performed the run",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contest.team",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="competition",
            name="contest",
            field=models.ForeignKey(
                help_text="Competition is one part of contest.",
                on_delete=django.db.models.deletion.CASCADE,
                to="contest.contest",
            ),
        ),
        migrations.AddField(
            model_name="competition",
            name="runs",
            field=models.ManyToManyField(
                help_text="Competition has more runs from different teams.",
                related_name="runs",
                through="contest.Run",
                to="contest.team",
            ),
        ),
        migrations.CreateModel(
            name="Result",
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
                ("score", models.IntegerField()),
                (
                    "comment",
                    models.TextField(
                        blank=True, default="", help_text="Comment to the participation"
                    ),
                ),
                (
                    "competition",
                    models.ForeignKey(
                        help_text="Competition is one part of contest.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contest.competition",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        help_text="Competition is one part of contest.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contest.team",
                    ),
                ),
            ],
            options={
                "unique_together": {("team", "competition")},
            },
        ),
    ]
