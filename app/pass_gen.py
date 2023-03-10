import streamlit_authenticator as stauth

hashed_passwords = stauth.Hasher(['Pandas2020!']).generate()

print(hashed_passwords)