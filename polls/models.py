from django.db import models
import datetime
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Tag(models.Model):
    tag = models.CharField(max_length=200)

    def __str__(self):
        """Returns the tag"""
        return self.tag


class Question(models.Model):
    """Store questions"""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    views = models.IntegerField(default=0)
    expiry_date = models.DateTimeField(null=True, default=None)
    order_no = models.PositiveIntegerField(default=1)
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)

    def __str__(self):
        """Returns the question"""
        return self.question_text

    def get_absolute_url(self):
        """
        returns a url using reverse function and primary key of the object

        """
        return reverse('polls:detail', kwargs={'pk': self.question_id})

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'published recently?'

    def choices_count(self):
        count_choice = self.choice_set.all().count()
        return count_choice

    @property
    def is_expired(self):
        """Returns false if question is expired else true"""
        now = timezone.now()
        if self.expiry_date > now:
            return False
        else:
            return True

    def choices(self):
        if not hasattr(self, '_choices'):
            self._choices = self.choice_set.all()
        return self._choices


class Choice(models.Model):
    """Stores choices related to model:question"""
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        """Returns the choices"""
        return self.choice_text


class Comment(models.Model):
    """Stores comments related to model:question"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='comments')
    email = models.EmailField(max_length=254, default=None)
    content = models.TextField()

    def __str__(self):
        return f"Comment by:{self.email}"
