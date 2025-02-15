from django.db import migrations

def migrate_video_ratings(apps, schema_editor):
    VideoRating = apps.get_model('home', 'VideoRating')
    VideoInteraction = apps.get_model('recomendacao', 'VideoInteraction')

    for rating in VideoRating.objects.all():
        VideoInteraction.objects.create(
            user=rating.user,
            video=rating.video,
            rating=rating.rating,
            method="unknown", 
            timestamp=rating.updated_at
        )

class Migration(migrations.Migration):
    dependencies = [
        ('recomendacao', '0002_videointeraction'), 
        ('home', '0002_videorating_updated_at'),  
    ]

    operations = [
        migrations.RunPython(migrate_video_ratings),
    ]
