from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserFollow , Relationship

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        UserFollow.objects.create(user=instance)

@receiver(post_save, sender=Relationship)
def post_save_add_to_follower(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.followed_user.add(receiver_.user)
        receiver_.followed_user.add(sender_.user)
        sender_.save()
        receiver_.save()

@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_from_follower(sender, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    sender.followed_user.remove(receiver.user)
    receiver.followed_user.remove(sender.user)
    sender.save()
    receiver.save()
