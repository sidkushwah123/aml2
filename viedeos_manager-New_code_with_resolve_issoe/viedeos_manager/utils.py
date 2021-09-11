import random
import string
from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))




def unique_id_generator_for_VsUsers(instance):
    order_new_id= random_string_generator()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(user_code= order_new_id).exists()
    if qs_exists:
        return unique_id_generator(instance)
    return order_new_id

def unique_id_generator(instance):
    order_new_id= random_string_generator()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(Videos_id= order_new_id).exists()
    if qs_exists:
        return unique_id_generator(instance)
    return order_new_id


def slug_generator_for_category(instance,new_slug=None):
    if new_slug is not None:
        slug= new_slug
    else:
        slug = slugify(instance.Title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(Slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{rendstr}".format(Slug=slug,rendstr=random_string_generator(size=4))
        return slug_generator_for_category(instance,new_slug=new_slug)
    return slug



def slug_generator_for_sub_category(instance,new_slug=None):
    if new_slug is not None:
        slug= new_slug
    else:
        slug = slugify(instance.Title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(Slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{rendstr}".format(Slug=slug,rendstr=random_string_generator(size=4))
        return slug_generator_for_sub_category(instance,new_slug=new_slug)
    return slug


def slug_generator_for_reating_review(instance,new_slug=None):
    if new_slug is not None:
        slug= new_slug
    else:
        slug = slugify(instance.Title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(Slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{rendstr}".format(slug=slug,rendstr=random_string_generator(size=4))
        return slug_generator_for_reating_review(instance,new_slug=new_slug)
    return slug


def slug_generator_for_videos(instance,new_slug=None):
    if new_slug is not None:
        slug= new_slug
    else:
        slug = slugify(instance.Videos_Title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(Videos_Slug=slug).exists()
    if qs_exists:
        new_slug = slug+"-"+random_string_generator(size=4)
        return slug_generator_for_videos(instance,new_slug=new_slug)
    return slug