from random import randint
from calendar import monthrange
from datetime import date

from core.models import UserCoin
from core.ERROR.error_cases import GlobalErrorMessage

from record.models import Post, Question, UserQuestion


def pick_question_pk_number():
    """
        question 들중 하나를 선택을 하기위해서, 만든 함수입니다.
    """
    count = Question.objects.all().count()
    if count < 1:
        return 0
    return randint(1, count)


def calculate_continuity_and_reward(profile_pk: int, created_at: date, today: date, tomorrow: date):
    """

    :param profile_pk: Profile 의 primary 객체이다.
    :param created_at: 사실상 yesterday 를 input 으로 받아서, 어제 객체를 생성을 하냐 안하냐 같은 정도
    :param today: 오늘 date
    :param tomorrow: 내일 date
    :return continuity: Post 객체를 얼마나 연속으로 만드는 지 체크하는 용도
    :return: reward: continuity 에 대한 보상
    """
    try:
        last_post = Post.objects.get(profile=profile_pk, created_at=created_at)
        continuity = last_post.continuity + 1
    except Post.DoesNotExist:
        continuity = 1

    if continuity == 7:  # 7일 연속 기록 보상
        reward = 20
    elif continuity == 17:  # 17일 연속 기록 보상
        reward = 30
    elif continuity == 27:  # 27일 연속 기록 보상
        reward = 50
    elif continuity == monthrange(today.year, today.month)[1]:  # 한 달 연속 기록 보상
        reward = 100
    else:  # 기본 기록 보상
        reward = 10
    if today.month != tomorrow.month:  # 매 달 연속 기록 체크 초기화
        continuity = 0
    return continuity, reward


def update_user_coin_with_reward(user_coin: UserCoin, reward: int, today: date):
    """
    user_coin 에 reward 를 추가를 해주는 작업이다.

    :param user_coin: UserCoin 객체
    :param reward: calculate_continuity_and_reward 을 통해 얻은 보상
    :param today: date
    :return:
    """
    coin = user_coin.coin
    if user_coin.last_date is None:  # 첫 일기 기록 보상
        coin = 100
    elif user_coin.last_date != today:  # 하루 보상 제공 1회 제한
        coin += reward

    user_coin.coin = coin
    user_coin.last_date = today
    user_coin.save()
    return coin


def get_question_of_user_question(profile_pk):
    try:
        return UserQuestion.objects.get(profile=profile_pk).question
    except UserQuestion.DoesNotExist:
        raise GlobalErrorMessage("유저에게 오늘의 질문을 할당을 해주세요.")


def fix_image_name(image_name):
    if image_name.count('"') == 1:
        image_name = image_name.replace('"', '')
    return image_name
