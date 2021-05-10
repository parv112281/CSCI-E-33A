# Generated by Django 3.1.6 on 2021-05-08 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patent_id', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Protein',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seq_id', models.CharField(max_length=10)),
                ('sequence', models.CharField(max_length=5000)),
                ('patent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sequences', to='epitope_extraction_tool.patent')),
            ],
        ),
        migrations.CreateModel(
            name='PatentFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.FileField(upload_to='')),
                ('patent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='file', to='epitope_extraction_tool.patent')),
            ],
        ),
        migrations.AddField(
            model_name='patent',
            name='protein',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patents', to='epitope_extraction_tool.protein'),
        ),
        migrations.CreateModel(
            name='Epitope',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='epitopes', to='epitope_extraction_tool.patent')),
                ('sequence', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='epitope', to='epitope_extraction_tool.sequence')),
            ],
        ),
    ]