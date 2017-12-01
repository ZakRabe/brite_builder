def user_to_json(user):
    return {
        "id":user.id,
        'username':user.username,
        "profile": user.profile.to_json()
    }
