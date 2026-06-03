from django.db import migrations
from django.db import connection


def rename_usuario_table(apps, schema_editor):
    tables = connection.introspection.table_names()
    if 'controle_usuario' in tables and 'usuarios_usuario' not in tables:
        schema_editor.execute("ALTER TABLE controle_usuario RENAME TO usuarios_usuario;")


def reverse_rename_usuario_table(apps, schema_editor):
    tables = connection.introspection.table_names()
    if 'usuarios_usuario' in tables and 'controle_usuario' not in tables:
        schema_editor.execute("ALTER TABLE usuarios_usuario RENAME TO controle_usuario;")


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(rename_usuario_table, reverse_rename_usuario_table),
    ]