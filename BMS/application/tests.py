from django.test import TestCase

# Create your tests here.
cleaned_data = {"email": "yhei@uwcrobbi.de", "username": "placeholder"}

def clean():
    email_stem, domain = cleaned_data["email"].split("@")

    cleaned_data["username"] = email_stem

    print(email_stem)
    #print(domain)
    print(cleaned_data["username"])

clean()