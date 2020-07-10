from django.db import models
from core.models import Profile

class Item(models.Model):
    item_name = models.CharField(max_length=100, null=True)
    item_type = models.CharField(max_length=100, null=True)
    item_detail = models.CharField(max_length=100, null=True)
    item_price = models.PositiveIntegerField()
    released_at = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('item_type', 'item_detail')
        ordering = ['-released_at']

    def __str__(self):
        return "[%d]%s (%s)" % (self.id, self.item_type, self.item_detail)

class UserItem(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    is_worn = models.BooleanField(default=False)

    def __str__(self):
        return "[%s] %s(%s) [%s]" % (self.profile, self.item.item_name, self.item.item_detail, self.is_worn)

    class Meta:
        unique_together = ('profile', 'item')
