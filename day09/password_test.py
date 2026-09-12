from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

my_pass = "mypassword123"
hash_pass = password_hash.hash(my_pass)  # create a password hash

correct = password_hash.verify(my_pass, hash_pass)  # check a password against a stored hash

wrong = password_hash.verify("cjcdsjchsjk", hash_pass)

print(f"Hashed password: {hash_pass}")
print(f"Correct password: {correct}")
print(f"Wrong password: {wrong}")