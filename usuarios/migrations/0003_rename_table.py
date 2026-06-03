from django.db import migrations
from django.db import connection


def rename_usuario_if_exists(apps, schema_editor):
    tables = connection.introspection.table_names()
    if 'controle_usuario' in tables and 'usuarios_usuario' not in tables:
        schema_editor.execute("ALTER TABLE controle_usuario RENAME TO usuarios_usuario;")


def reverse_rename_usuario_if_exists(apps, schema_editor):
    tables = connection.introspection.table_names()
    if 'usuarios_usuario' in tables and 'controle_usuario' not in tables:
        schema_editor.execute("ALTER TABLE usuarios_usuario RENAME TO controle_usuario;")


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alter_usuario_table'),
    ]

    operations = [
        migrations.RunPython(rename_usuario_if_exists, reverse_rename_usuario_if_exists),
    ]