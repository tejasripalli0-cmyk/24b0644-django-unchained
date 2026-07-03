from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Bounty


def get_bounty_list_cache_key(user_id):
    """
    Builds the cache key used for a given user's bounty list endpoint.
    Shared helper so views.py and signals.py always agree on the key format.
    """
    return f'bounty_list_user_{user_id}'


def invalidate_bounty_cache(owner_id):
    """
    Invalidates the cached bounty list for a specific owner.
    """
    cache.delete(get_bounty_list_cache_key(owner_id))


@receiver(post_save, sender=Bounty)
def bounty_saved(sender, instance, **kwargs):
    """
    Invalidate the cache whenever a Bounty is created or updated.
    """
    invalidate_bounty_cache(instance.owner_id)


@receiver(post_delete, sender=Bounty)
def bounty_deleted(sender, instance, **kwargs):
    """
    Invalidate the cache whenever a Bounty is deleted.
    """
    invalidate_bounty_cache(instance.owner_id)
