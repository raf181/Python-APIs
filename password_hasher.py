from passlib.hash import bcrypt

password = "password2"
hashed_password = bcrypt.using(rounds=12).hash(password)
print(hashed_password)