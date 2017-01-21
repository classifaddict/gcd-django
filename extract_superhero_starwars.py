from django.db.models import Q
#from django.core import serializers
from apps.gcd.models import Story, Issue

stories = Story.objects.filter(
    Q(issue__series__language__code__in=["fr", "en"]),
    Q(title__icontains="Star Wars") | Q(genre__icontains="superhero")
).exclude(issue__series__publication_type__name="magazine").values("issue").distinct()

# Count as of 19.01.2017: 32327

# data = serializers.serialize('json', [Issue.objects.get(id=story['issue']) for story in stories])

for story in stories:
    issue = Issue.objects.get(id=story['issue'])
