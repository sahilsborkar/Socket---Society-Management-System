from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class SocietyMembership(models.Model):
    member = models.ForeignKey(User, related_name='society_membership', on_delete=models.CASCADE)
    society = models.ForeignKey('Society', related_name='society_membership', on_delete=models.CASCADE)
    is_leader = models.BooleanField(default=False)


class Society(models.Model):
    name = models.CharField(max_length = 200, unique=False)
    description = models.TextField()
    members = models.ManyToManyField(
        User,
        verbose_name=("Members"),
        related_name='societies',
        through='SocietyMembership'
    )

    @property
    def leaders(self):
        return self.society_membership.filter(is_leader=True)

    def user_is_leader(self, user: User):
        return self.society_membership.filter(is_leader=True, member=user).exists()

    def is_member(self, user: User):
        return self.members.filter(pk=user.id).exists()

    def __str__(self):
        return f"{self.name}"

    def enroll(self, user: User, as_leader: bool = False):
        # Django >= 2.2, which it should be in July 2020
        self.members.add(user, through_defaults={"is_leader": as_leader})

    def promote(self, user: User) -> bool:
        try:
            society_membership = self.society_membership.get(member=user)
        except SocietyMembership.DoesNotExist:
            return False

        society_membership.is_leader = True
        society_membership.save()
        return True

    def demote(self, user: User) -> bool:
        try:
            society_membership = self.society_membership.get(member=user)
        except SocietyMembership.DoesNotExist:
            return False

        society_membership.is_leader = False
        society_membership.save()
        return True

    def kick(self, user: User):
        self.society_membership.filter(member=user).delete()

    @classmethod
    def create(cls, **kwargs):
        society = cls.objects.create(
            name=kwargs['name'],
            description=kwargs['description']
        )
        return society

class SocPost(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'society_id':self.society.id, 'pk':self.pk})

class SocietyProfile(models.Model):
    society = models.OneToOneField(Society, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='default.jpg', upload_to='society_profile_pics')

    def __str__(self):
        return f"{self.society.name} Info"