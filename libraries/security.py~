import hashlib

def sha1(password):
    sha1_salt_value = 'd0be2dc421be4fcd0172e5afceea3970e2f3d940'
    sha1_iterations = 5

    value = password
    sha1 = hashlib.sha1()
    for i in range(sha1_iterations):
        sha1.update(sha1_salt_value)
        sha1_salt_value = sha1.hexdigest()
        sha1.update(value + sha1_salt_value)
        value = sha1.hexdigest()

    return value
