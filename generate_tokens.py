# Version: 0.02
import secrets
import string

def generate_token(length=24):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == '__main__':
    tokens = [generate_token() for _ in range(3)]
    token_string = ','.join(tokens)
    
    print("\n--- Eye Token Generator ---")
    print("Kopeeri see rida oma .env faili:\n")
    print(f"ACCESS_TOKENS={token_string}")
    print("\n---------------------------")
