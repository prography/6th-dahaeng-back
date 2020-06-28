from django.db import models
from cored.models import Profile

class Items(models.Model):
    item_type = models.CharField(max_length=100)
    item_detail = models.CharField(max_length=100)
    item_price = models.PositiveIntegerField()
    released_at = models.DateField(auto_now=True, auto_now_add=True)

    class Meta:
        unique_together = ('item_type', 'item_detail')
        ordering = ('-released_at')

class UserItems(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    is_worn = models.BooleanField(default=False)