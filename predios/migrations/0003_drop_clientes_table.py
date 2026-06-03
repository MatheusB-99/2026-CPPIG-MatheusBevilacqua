from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predios', '0002_alter_predio_options'),
    ]

    operations = [
        migrations.RunSQL(
            sql="DROP TABLE IF EXISTS clientes_cliente;",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
