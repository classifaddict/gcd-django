import json
from django.db.models import Q
#from django.core import serializers
from apps.gcd.models import Story, Issue

stories = Story.objects.filter(
    Q(issue__series__language__code__in=["fr", "en"]),
    Q(title__icontains="Star Wars") | Q(genre__icontains="superhero")
).exclude(issue__series__publication_type__name="magazine").values("issue").distinct()

# Count as of 19.01.2017: 32327

# data = serializers.serialize('json', [Issue.objects.get(id=story['issue']) for story in stories])

data = []
for story in stories:
    id=story['issue']
    issue = Issue.objects.get(id=id)
    data.append{
        'id': id,
        'lang': issue.series.language.code,
        'genre': issue.story_set.first().genre,
        'short_name': issue.short_name(),
        'full_name': issue.full_name(),
        'gcd_url': issue.get_absolute_url(),
        'page_count': page_count,
        'price': price,
        'publication_date': publication_date,
        'barcode': barcaode,
        'valid_isbn': valid_isbn,
        'isbn': isbn
    }) 

json.dumps(data, indent=4)