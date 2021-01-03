from random import choice
from core.ERROR.error_cases import GlobalErrorMessage401
from shop.models import Item


def random_color() -> Item:
    """
        추후 조랭이 색깔을 정하기 위해서 사용이 되는 함수이다.
        조랭이 컬러 추가에 대응하기 위해 RGB string 선택에서 Item선택으로 변경했다.
    """
    colors = Item.objects.all().filter(item_type="jorang_color")
    if colors:
        return choice(colors)
    raise GlobalErrorMessage401("아이템이 없습니다.")
