import requests
import hashlib
import sys

# Here we use Pwned Passwords which are 613,584,246 real world passwords previously exposed in data breaches.
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code !=200:
        raise RuntimeError(f'Error fetching: {res.status_code},check the api and try agian')
    return res

# Here count password leak count,means how many time password hack.
def get_password_leak_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h==hash_to_check:
            return count
    return 0



def pwned_api_check(password):
    #check password if it exists in API response
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5],sha1password[5:] 
    response = request_api_data(first5_char)
    return get_password_leak_count(response,tail)
   


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times..... you should probably change your password')
        else:
            print(f'{password} was not found. carry on!')
    return 'Done!'

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))