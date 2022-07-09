def email_user_authentication_rule(user):
    return user is not None and user.is_active and user.verified
