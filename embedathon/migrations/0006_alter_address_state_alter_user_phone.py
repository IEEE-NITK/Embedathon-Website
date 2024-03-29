# Generated by Django 4.1.3 on 2022-11-22 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embedathon', '0005_alter_address_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(choices=[('Andhra Pradesh', 'Andhra Pradesh'), ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'), ('Arunachal Pradesh', 'Arunachal Pradesh'), ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Chandigarh', 'Chandigarh'), ('Chhattisgarh', 'Chhattisgarh'), ('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'), ('Daman and Diu', 'Daman and Diu'), ('Delhi', 'Delhi'), ('Goa', 'Goa'), ('Gujarat', 'Gujarat'), ('Haryana', 'Haryana'), ('Himachal Pradesh', 'Himachal Pradesh'), ('Jammu and Kashmir', 'Jammu and Kashmir'), ('Jharkhand', 'Jharkhand'), ('Karnataka', 'Karnataka'), ('Kerala', 'Kerala'), ('Lakshadweep', 'Lakshadweep'), ('Madhya Pradesh', 'Madhya Pradesh'), ('Maharashtra', 'Maharashtra'), ('Manipur', 'Manipur'), ('Meghalaya', 'Meghalaya'), ('Mizoram', 'Mizoram'), ('Nagaland', 'Nagaland'), ('Odisha', 'Odisha'), ('Puducherry', 'Puducherry'), ('Punjab', 'Punjab'), ('Rajasthan', 'Rajasthan'), ('Sikkim', 'Sikkim'), ('Tamil Nadu', 'Tamil Nadu'), ('Telangana', 'Telangana'), ('Tripura', 'Tripura'), ('Uttar Pradesh', 'Uttar Pradesh'), ('Uttarakhand', 'Uttarakhand'), ('West Bengal', 'West Bengal')], max_length=50, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=20, unique=True, verbose_name='Phone Number'),
        ),
    ]
