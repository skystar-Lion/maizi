from django.db import models

# Create your models here.

class search(models.Model):
    """docstring for search"""
    #关键字，查询的频数，查询的日期
    key_word = models.CharField('关键字', max_length = 30)
    times = models.IntegerField('查询次数')
    query_time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return ("{} {}".format(self.key_word, self.times))
        #return self.key_word
    
        