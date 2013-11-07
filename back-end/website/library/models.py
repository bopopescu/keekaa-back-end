from django.db import models
from django.utils.timezone import now
from mptt.models import MPTTModel
from website.users.models import User


class DujourDefaultModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if hasattr(self, 'updated_time'):
            self.updated_time = now()
        super(DujourDefaultModel, self).save(*args, **kwargs)

    def delete(self):
        self.is_active = False
        self.save()
        return

    def obj_type(self):
        return type(self).__name__.lower()

    def __unicode__(self):
        return unicode(self.pk)

    def user_voted(self, user_id):
        userProfile = User.objects.get(pk=user_id).get_profile()
        return self.vote_set.filter(owner=userProfile.id,
                                    is_active=True).exists()

    def total_votes(self):
        return self.vote_set.filter(is_active=True).count()

    def total_comments(self):
        return self.comment_set.filter(is_active=True).count()

    def total_favorites(self):
        return self.favorite_set.filter(is_active=True).count()


class DujourDefaultModel_MPTT(MPTTModel):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if hasattr(self, 'updated_time'):
            self.updated_time = now()
        super(DujourDefaultModel_MPTT, self).save(*args, **kwargs)

    def delete(self):
        self.is_active = False
        self.save()
        return

    def obj_type(self):
        return type(self).__name__.lower()

    def __unicode__(self):
        return unicode(self.pk)

    def user_voted(self, user_id):
        userProfile = User.objects.get(pk=user_id).get_profile()
        return self.vote_set.filter(owner=userProfile.id,
                                    is_active=True).exists()

    def total_votes(self):
        return self.vote_set.filter(is_active=True).count()

    def total_comments(self):
        return self.comment_set.filter(is_active=True).count()

    def total_favorites(self):
        return self.favorite_set.filter(is_active=True).count()
