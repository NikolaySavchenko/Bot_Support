from tgbot.models import User, Developer, Manager, Owner


def get_user_group(telegram: str):
    if Owner.objects.filter(telegram=telegram):
        return Owner.objects.filter(telegram=telegram)[0],'OWNER'
    elif Manager.objects.filter(telegram=telegram):
        return Manager.objects.filter(telegram=telegram)[0], 'MANAGER'
    elif Developer.objects.filter(telegram=telegram):
        return Developer.objects.filter(telegram=telegram)[0], 'DEVELOPER'
    elif User.objects.filter(telegram=telegram):
        return User.objects.filter(telegram=telegram)[0], 'CLIENT'
    else:
        return None, 'NEW_USER'


def create_user(telegram: str):
    user, created = User.objects.get_or_create(
        telegram=telegram,
        state='INPUT_PHONE_NUMBER'
    )
    return created

def create_developer(telegram: str):
    developer, created = Developer.objects.get_or_create(
        telegram=telegram,
        state='INPUT_PHONE_NUMBER'
    )
    return created


def add_user_name(user: User, name: str):
    user.name = name
    user.save()
    return True


def get_user(telegram: str) -> User:
    user = User.objects.get(
        telegram=telegram,
    )

    return user


def add_user_phone(user: User, phone: str):
    user.phone = phone
    user.save()
    return True
