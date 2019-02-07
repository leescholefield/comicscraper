from time import time
from hashlib import md5
import requests
import config
from models import Issue

base_url = "https://gateway.marvel.com/v1/public"


def upcoming_collections():
    """
    Gets all collections that have been, or are going to be, released this month.
    """
    res = __send_request("/comics?formatType=collection&dateDescriptor=thisMonth")
    __parse_response(res.json())


def upcoming_issues():
    """
    Gets all single issues that have been, or are going to be, released this month.
    """
    res = __send_request("/comics?format=comic&formatType=comic&dateDescriptor=thisMonth")
    __parse_response(res.json())


def __send_request(endpoint=str) -> requests.Response:
    """
    Sends an HTTP request to the url constructed from appending the endpoint onto the base_url.

    :param endpoint: contains additional search params. For instance, the release date.
    :return: a requests.Response object
    :except if we receive anything other than a 200 response
    """
    url = base_url + endpoint
    res = requests.get(url, params=__generate_payload())
    if __response_ok(res):
        return res
    else:
        reason = "Error occurred: status code = {}, message = {}".format(res.json()['code'], res.json()['message'])
        raise Exception(reason)


def __generate_payload() -> dict:
    """
    Generates the payload that will be sent with the request to Marvel to enable authentication.
    This must include: the public API key, a timestamp, and a md5 md5_hash of the timestamp + public key + private key.
    :return: dict
    """
    now = int(time())
    hash_string = str(now) + config.marvel_private_key + config.marvel_public_key
    md5_hash = md5(hash_string.encode("utf-8")).hexdigest()

    return {'apikey': config.marvel_public_key, 'ts': now, 'hash': md5_hash}


def __response_ok(response: requests.Response) -> bool:
    """
    :return: false if
    """
    return response.status_code == 200


def __parse_response(json):
    """
    Parses the json response and constructs a list of Issue's.
    """
    data = json['data']['results']

    for r in data:
        if r['format'] == 'Comic':
            __parse_issue(r)
        else:
            print("is NOT a comic")


def __parse_issue(data):
    for key, val in data.items():
        if key == 'creators':
            print(val)
    # return Issue(title=data['title'], )


def __get_creators(data):
    pass



if __name__ == '__main__':
    upcoming_issues()
