from flask_httpauth import HTTPTokenAuth


auth = HTTPTokenAuth(scheme='Bearer')


tokens = {
    "mysecrettoken": "john",
    "anothertoken": "jane"
}


def verify_token(token):
    if token in tokens:
        return tokens[token]
    return None
