import secrets

base_set = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
base = [c for c in base_set]

def create_random_slug(length=16):
    slug = ""
    for i in range(0, length):
        slug += secrets.choice(base)

    return slug