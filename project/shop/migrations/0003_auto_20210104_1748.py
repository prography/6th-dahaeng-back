# Generated by Django 3.0.5 on 2021-01-04 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_jorang'),
    ]

    operations = [
        migrations.RunSQL(
            """
            INSERT INTO shop_jorang_items(useritem_id, jorang_id) 
            SELECT shop_useritem.id, shop_jorang.id
            FROM shop_jorang, shop_item, shop_useritem
            WHERE shop_jorang.profile_id = shop_useritem.profile_id
            AND shop_useritem.item_id = shop_item.id
            AND shop_jorang.color = shop_item.item_detail
            """
        )
    ]
