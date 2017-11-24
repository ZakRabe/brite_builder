def user_to_json(user):
    return {
        "user_id":user.id,
        'username':user.username,
        "profile": user.profile.all()[0].to_json()
    }
