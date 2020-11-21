from record.models import Post
from datetime import date

def get_id_of_today_post(profile) :
    post_id = None

    try:
        post = Post.objects.get(profile=profile, created_at=date.today())
        post_id = post.id
    except Post.DoesNotExist:
        post_id = -1

    return post_id
    