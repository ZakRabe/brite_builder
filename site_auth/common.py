def user_to_json(user):
    return {
        "user_id":user.id,
        'username':user.username,
        "profile": user.profile.to_json()
    }
