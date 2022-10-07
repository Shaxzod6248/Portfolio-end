from email.policy import default
import uuid
from django.db import models
from users.models import *


class Project(models.Model):
    user = models.ForeignKey(Profil, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(default="default.png")
    demo_link = models.CharField(max_length=400, null=True, blank=True)
    source_link = models.CharField(max_length=400, null=True, blank=True)
    vote_count = models.IntegerField(default=0)
    vote_ratio = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    tag = models.ManyToManyField('Tag', blank=True, related_name="project_tag")

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('user__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.project_review.all()
        upVotes = reviews.filter(value='ijobiy').count()
        totalVotes = reviews.count()
        ratio = (upVotes / totalVotes) * 100

        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()


class Review(models.Model):
    user = models.ForeignKey(Profil, on_delete=models.CASCADE   , null=True, blank=True)
    VOTE_TYPE = (
        ("+", "Ijobiy"),
        ("-", "Salbiy")
    )
    body = models.TextField(default='')
    value = models.CharField(max_length=50, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name="project_review")

    class Meta:
        unique_together = [['user', 'project']]

    def __str__(self) -> str:
        return f"{self.value} {self.project.title}"


class Tag(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self) -> str:
        return self.name

