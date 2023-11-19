"""
Calls Google domains api to update dynamic dns entry

https://support.google.com/domains/answer/6147083
"""

import requests


def main(username, password, domain, email):
    url = (
        f"https://{username}:{password}@domains.google.com/nic/update?hostname={domain}"
    )
    headers = {
        "User-Agent": f"requests/2.31.0 {email}",
    }

    response = requests.get(url=url, headers=headers)
    print(response.status_code)
    print(response.text)
