from tgbot.models import User, Developer, Manager, Owner


def get_or_create_user(telegram: str):
    if Owner.objects.filter(telegram=telegram):
        return Owner.objects.filter(telegram=telegram)[0],'OWNER'
    elif Manager.objects.filter(telegram=telegram):
        return Manager.objects.filter(telegram=telegram)[0], 'MANAGER'
    elif Developer.objects.filter(telegram=telegram):
        return Developer.objects.filter(telegram=telegram)[0], 'DEVELOPER'
    elif User.objects.filter(telegram=telegram):
        return User.objects.filter(telegram=telegram)[0], 'CLIENT'
    else:
        user = User.objects.create(telegram=telegram)
        return user, 'NEW_CLIENT'


def add_user_name(user: User, name: str):
    user.name = name
    user.save()
    return True


def get_user(telegram: str) -> User:
    user = User.objects.get(
        telegram=telegram,
    )

    return user