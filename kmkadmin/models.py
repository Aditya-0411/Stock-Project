from django.db import models
import uuid
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from django.utils import timezone
# Create your models here.

class Stock(models.Model):
        stock_risks = [
                ('Low', 'Low'),
                ('Medium', 'Medium'),
                ('High', 'High')
                ]
        id = models.UUIDField(default=uuid.uuid4,
                        unique=True,
                        editable=False,
                        primary_key=True)

        created = models.DateTimeField(auto_now_add=True)
        stock_name = models.CharField(max_length=200,
                                null=True,
                                blank=True)
        stock_symbol = models.CharField(max_length=20,
                                        null=True,
                                        blank=True,
                                        unique=False)
        stock_exchange = models.CharField(max_length=7,
                                        null=True,
                                        blank=True)
        stock_scrip_code = models.IntegerField(null=True,
                                        blank=True,
                                        unique=False)
        stock_industry = models.CharField(max_length=200,
                                        null=True,
                                        blank=True)
        market_cap = models.FloatField(null=True,
                                blank=True)
        no_of_shares = models.BigIntegerField(null=True,
                                        blank=True)
        live_price = models.FloatField(null=True,
                                blank=True)
        upside_left = models.FloatField(null=True,
                                        blank=True)
        expected_returns = models.FloatField(null=True,
                                        blank=True)
        time_left = models.IntegerField(null=True,
                                        blank=True)
        risk = models.CharField(max_length=50,
                                choices=stock_risks,
                                null=True,
                                blank=True)
        tag1 = models.CharField(max_length=50,
                                default='Active',
                                null=False,
                                blank=False)
        tag2 = models.CharField(max_length=50,
                                null=True,
                                blank=True)
        exit_price = models.FloatField(null=True, blank=True)
        exit_date = models.DateField(null=True, blank=True)
        free_stock = models.BooleanField(default=False)

        permissions=[('can_add_stock', 'Can add stock'),
                     ('can_delete_stock', 'Can delete stock'),
                     ('can_edit_stock', 'Can edit stock'),
                     ('can_view_stock', 'Can view stock'),]
        
        def __str__(self):
                return self.stock_name


class StockTarget(models.Model):
        stock_status = [
            ('Active', 'Active'),
            ('Active - Target Met', 'Active - Target Met'),
            ('Inactive - Target Met', 'Inactive - Target Met'),
            ('Inactive - Partial Profit Booked', 'Inactive - Partial Profit Booked'),
            ('Inactive - Loss Booked', 'Inactive - Loss Booked')
            ]
        stock_actions = [
            ('BUY', 'BUY'),
            ('HOLD', 'HOLD'),
            ('SELL', 'SELL')
            ]
        id = models.UUIDField(default=uuid.uuid4,
                          unique=True,
                          editable=False,
                          primary_key=True)
        created = models.DateTimeField(auto_now_add=True)

        stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
        entry_price = models.FloatField(null= True, blank=True)
        target_price = models.FloatField(null=True,
                                         blank=True)
        
        target_met = models.DateField(null=True,blank=True),
        
        target_date = models.DateField(null=True,
                                       blank=True)
        gain_loss = models.DecimalField(decimal_places=2,
                                        max_digits=5,
                                        null=True,
                                        blank=True)
        target_action = models.CharField(max_length=4, default='BUY',
                                         choices= stock_actions)
        target_status = models.CharField(max_length=50,
                                         choices= stock_status,
                                         null=True,
                                         blank=True)
        class Meta:
                ordering = ['-created']

                def __str__(self):
                        return str(self.stock)



#STORE USER INSTANCES PERFORMED ON ANY STOCK
class Stocklog(models.Model):
    ACTION_CHOICES = [
        ('Stock Added', 'Stock Added'),
        ('Stock Deleted', 'Stock Deleted'),
        ('Stock Edited', 'Stock Edited'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.UUIDField()
    main_data = models.CharField(max_length=30)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"





#FOR USERS TO UPLOAD REPORT OF A STOCK
class StockReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    report_file = models.FileField(upload_to='stock_reports/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock.stock_name} - Report {self.id}"



#REPORTLOG MODEL TO STORE USER INSTANCES WHENEVER A REPORT IS ADDED OR DELETED
class StockReportLog(models.Model):
    ACTION_CHOICES = [
        ('Stock Report Added', 'Stock Report Added'),
        ('Stock Report Deleted', 'Stock Report Deleted'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_id = models.UUIDField()  # Store the UUID of the deleted StockReport instance
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.stock_id}"

    def get_report_link(self):
        return f"/media/{self.stock_id}.pdf"  # Assuming PDF extension, update it accordingly




class Blogs(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    permissions=[('can_add_blogs', 'Can add blogs'),
                   ('can_delete_blogs', 'Can delete blogs'),
                    ('can_edit_blogs', 'Can edit blogs'),
                    ('can_delete_blogs', 'Can delete blogs'),
                 ]
    def __str__(self):
      return f"{self.title}"
