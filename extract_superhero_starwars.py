import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    import json
    import django
    from django.db.models import Q
    #from django.core import serializers
    from apps.gcd.models import Story, Issue

    django.setup()
    stories = Story.objects.filter(
        Q(issue__series__language__code__in=["fr", "en"]), Q(issue__variant_of=None),
        Q(type__name="cover"),
        Q(title__icontains="Star Wars") | Q(genre__icontains="superhero")
    ).exclude(issue__series__publication_type__name="magazine")

    # print stories.values("issue").distinct().count()
    # Count as of 19.01.2017: 25219

    # data = serializers.serialize('json', [Issue.objects.get(id=story['issue']) for story in stories])

    ids = set()
    with open('data.json', 'w') as f:
        f.write("[")
        for story in stories:
            issue = story.issue
            id=issue.id
            if id in ids:
                continue
            ids.add(id)
            data = {
                'lang': issue.series.language.code,
                'country': issue.series.country.code,
                'publisher': issue.series.publisher.name,

                'genre': story.genre,
                'script': story.script,
                'pencils': story.pencils,
                'characters': story.characters,
                'synopsis': story.synopsis,

                'id': str(id),
                'short_name': issue.short_name(),
                'full_name': issue.full_name(),
                'gcd_url': issue.get_absolute_url(),
                'page_count': str(issue.page_count),
                'price': issue.price,
                'publication_date': issue.publication_date,
                'barcode': issue.barcode,
                'valid_isbn': issue.valid_isbn
            }

            f.write(json.dumps(data, indent=4))
        f.write("]")