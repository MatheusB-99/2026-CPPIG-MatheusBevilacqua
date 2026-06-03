from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0003_add_fields_state'),
    ]

    operations = [
        migrations.RunSQL(
            sql="DROP TABLE IF EXISTS notificacoes_notificacao;",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
