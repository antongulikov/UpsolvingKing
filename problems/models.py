from django.db import models
from users.models import UpUser

# Create your models here.

class Problem(models.Model):

    class Meta():
        db_table = 'problem'
        unique_together = (('contest_id', 'problem_id'),)

    problem_name = models.CharField(max_length=300, null=False)
    contest_id = models.IntegerField(null=False)
    problem_id = models.CharField(max_length=1, null=False)
    kings = models.ManyToManyField(UpUser)



    def get_url(self):
        x = int(self.contest_id)
        if x < 10000:
            return 'http://www.codeforces.com/problemset/problem/{}/{}'.format(str(self.contest_id), str(self.problem_id))
        else:
		    return 'http://www.codeforces.com/gym/{}'.format(self.contest_id)

