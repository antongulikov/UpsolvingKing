from users.models import *

def point(userRating, tagRating, solved):
    import math
    rating = float(userRating * 0.7 + tagRating * 0.3)
    solved = float(solved)
    f1_value = 1.0 / (1.0 + math.e ** (-rating / float(300) + 5.0))
    f2_value = math.log(solved / float(100) + 1.0)
    result = 1.0 / (1.0 + math.e ** (math.sqrt(f1_value * rating / float(3000) + f2_value * solved / float(2000))))
    return result

def rating_by_power(x):
    try:
        x = float(x)
    except:
        return 0
    return 3000 * x / (20. + x)

def update_user_tag_relationship(USERNAME, TAG, SOLVED):
    tag_object = Tag.objects.get(name = TAG)
    user = UpUser.objects.get(username = USERNAME)
    userRating = user.rating
    usertag = None
    try:
        usertag = UserTag.objects.get(tag = tag_object, user = user)
    except:
        usertag = UserTag.objects.create(tag = tag_object, user = user)
    power = usertag.power
    delta = point(userRating, rating_by_power(power), SOLVED)
    usertag.power = power + delta
    usertag.save()
