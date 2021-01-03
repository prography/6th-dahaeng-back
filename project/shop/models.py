"""
    Item 의 경우, 관리자가 만들고,
    그후에 UserItem 을 통해서, 실제 User 와 mapping 을 시켜준다.
"""
from django.db import models
from core.models import Profile


class Item(models.Model):
    """
        관리자가 Item 을 만들어준다.
    """
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
    """
        Item 과 User(Profile) 를 mapping 을 시켜주는 작업합니다.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    is_worn = models.BooleanField(default=False)

    def __str__(self):
        return "[%s] %s(%s) [%s]" % (self.profile, self.item.item_name, self.item.item_detail, self.is_worn)

    class Meta:
        unique_together = ('profile', 'item')


class Jorang(models.Model):
    """
        우리의 마스코트 조랭이
        조랭이의 경우, 생성될 때, 유저와 1:1 [OneToOneField] 로 mapping 이 되기 떄문에
        유저 당 딱 한번 밖에 생성이 되지 않는다.
        그렇기에 유의를 할 필요가 있다.
    """
    STATUS_CHOICES = (
        ('0', '알'),
        ('1', '유년기'),
        ('2', '성장기')
    )

    profile = models.OneToOneField(
        Profile, null=True, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    items = models.ManyToManyField(UserItem)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=0)
    title = models.CharField(max_length=100, default="Da:haeng")

    def __str__(self):
        return "[%s] %s (%s)" % (self.profile, self.nickname, self.title)
