from users.models import *
import random

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
    return 3000 * x / (10. + x)

def update_user_tag_relationship(user, tag_object, SOLVED):
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

def dist(a, b):
    n = len(a)
    sumq = 0
    for i in xrange(n):
        sumq += (a[i] - b[i]) * (a[i] - b[i])
    return sumq

class Point():

    def __init__(self, who, coord, id, cluster = 0):
        self.who = who
        self.coordinates = coord
        self.ide = id
        self.cluster = cluster

    def len(self):
        import math
        xx = 0
        for x in self.coordinates:
            xx += x * x
        return math.sqrt(xx)

    def nearest(self, centroids):
        maxdist = 10**(18 * len(centroids))
        for centroid in centroids:
            distance = dist(self.coordinates, centroid.coordinates)
            if distance < maxdist:
                maxdist = distance
                self.cluster = centroid.cluster



def k_mean_iteration(data, centroids):
    """Implementation of k-means"""
    n = len(centroids) + 1
    cnt = [0] * n

    for x in data:
        x.nearest(centroids)
        cnt[x.cluster] += 1

    newCentroids = []
    for i in xrange(n):
        value = [0] * len(centroids[0].coordinates)
        for x in data:
            for t in xrange(len(x.coordinates)):
                value[t] = value[t] + x.coordinates[t]
        value = [float(y) / float(cnt[i] + 1) for y in value]
        newCentroids.append(Point(1, value, -1, i))
    return data, newCentroids


def generate_problems(username, *tags):
    user = UpUser.objects.get(username= username)
    tags = list(tags)
    problems = Problem.objects.exclude(users__in=[user.id])
    curTags = []
    for tag in tags:
        if len(Tag.objects.filter(name=tag)):
            curTags.append(Tag.objects.filter(name=tag)[0])
    if len(curTags) == 0:
        return problems[:5]
    else:
        us = []
        for tag in curTags:
            usertag = 1
            try:
                usertag = UserTag.objects.get(tag = tag, user = user)
            except:
                usertag = UserTag.objects.create(tag = tag, user = user)
            us.append(rating_by_power(usertag.power) + 0.7 * user.rating)
        rbp = rating_by_power(usertag.power)
        centroids = [Point(0, us, user.id, 1)]
        data = [Point(0, us, user.id, 1)]
        for num in range(10):
            newc = []
            for l in range(len(us)):
                valrand = random.randint(100, 200)
                randkoef = random.randint(-1,1)
                newc.append(us[l] + valrand * randkoef)
            centroids.append(Point(1, newc, -1, num + 2))
        dictq = {}
        # for each problem create a vector of coordinates
        for problem in problems:
            dictq[problem.id] = [0.] * len(curTags)
        for i in range(len(curTags)):
            prob = Problem.objects.exclude(users__in=[user.id]).filter(tag__in = [curTags[i].id])
            for problem in prob:
                tagpr = None
                try:
                    tagpr = TagProblem.objects.get(tag=curTags[i], problem=problem)
                except:
                    tagpr = TagProblem.objects.create(tag=curTags[i], problem=problem)
                dictq[problem.id][i] = point(user.rating,rbp,tagpr.cnt_solved) * 20000.0

        for problem in problems:
                if sum(dictq[problem.id]) > 0:
                    data.append(Point(2, dictq[problem.id],problem.id))

        for x in data:
            print x.coordinates

        for k_mean_iter in range(10):
            print k_mean_iter
            data, centroids = k_mean_iteration(data, centroids)
        cluster = -1
        userPoint = None
        for x in data:
            if x.who == 0:
                cluster = x.cluster
                userPoint = x
                break
        data = [x for x in data if x.cluster == cluster]
        data = sorted(data, key=lambda x: dist(x.coordinates, userPoint.coordinates))
        data = data[2:12]
        result = []
        for x in data:
            result.append(Problem.objects.get(id=x.ide))
        return result