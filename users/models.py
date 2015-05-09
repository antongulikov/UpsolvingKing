from django.db import models

# Create your models here.

class Problem(models.Model):

    class Meta():
        db_table = 'problem'
        unique_together = (('contest_id', 'problem_id'),)

    def __unicode__(self):
        return self.problem_name

    problem_name = models.CharField(max_length=300, null=False)
    contest_id = models.IntegerField(null=False)
    problem_id = models.CharField(max_length=1, null=False)
    site = models.CharField(max_length=200, default="codeforces")
    solved = models.IntegerField(default=0)

    def get_url(self):
        if self.site == "codeforces":
            x = int(self.contest_id)
            if x < 10000:
                return 'http://www.codeforces.com/problemset/problem/{}/{}'.format(str(self.contest_id), str(self.problem_id))
            else:
                return 'http://www.codeforces.com/gym/{}'.format(self.contest_id)
        else:
            return "http://google.com/"



class UpUser(models.Model):

    class Meta():
        db_table = 'upuser'

    def __unicode__(self):
        return self.username


    username = models.CharField(max_length=200, unique=True)
    rating = models.IntegerField(null=False)
    watched = models.IntegerField(default=0)

    def get_rating(self):
        if self.rating < 0:
            return 0
        if self.rating > 3000:
            return 3000
        return self.rating


class UserTag(models.Model):

    class Meta():
        db_table = 'usertag'
        unique_together = (('user', 'tag'), )

    def __unicode__(self):
        return self.user.username + ' ' + self.tag.name + ' = ' + str(self.power)


    user = models.ForeignKey(UpUser)
    tag = models.ForeignKey('Tag')
    power = models.FloatField(default=0)

class Tag(models.Model):

    class Meta():
        db_table = 'tag'

    def __unicode__(self):
        return self.name


    name = models.CharField(max_length=50, null=False)
    problems = models.ManyToManyField(Problem)

class TagProblem(models.Model):

    class Meta():
        db_table = 'tagproblem'
        unique_together = (('tag', 'problem'), )

    def __unicode__(self):
        return self.cnt_solved


    tag = models.ForeignKey(Tag)
    problem = models.ForeignKey(Problem)
    cnt_solved = models.IntegerField(default=0)