from mastodon import Mastodon
import html2text
import requests

mastodon = Mastodon(
    access_token = "token.secret",
    api_base_url = "https://pointless.chat/"
)

mentions = []
h = html2text.HTML2Text()
h.ignore_links = True


def check_mentions():
    try:
        notifications = mastodon.notifications(mentions_only = True)
    except:
        return

    for noti in notifications:
        mentions.append(noti)
        mastodon.notifications_dismiss(noti["id"])
    
    reply_mentions()


def reply_mentions():
    for mention in mentions:
        content = h.handle(mention["status"]["content"]).split()[1:]
        short_url = get_short_url(content[0])

        if short_url != None:
            status = f"단축된 URL은 {short_url} 입니다."

            try:
                mastodon.status_reply(in_reply_to_id=mention["status"]["id"], status=status, to_status=mention["status"])
                print(status + "\n")
            except:
                print("Toot was not found")
        
        mentions.pop(0)


def get_short_url(url):
    api = "https://krll.me/api/urls"
    request = {
        "url": url
    }
    response = requests.post(url=api, json=request)
    data = response.json()
    
    if response.status_code == 200:
        return "https://krll.me/" + data["key"]
    else:
        return None


check_mentions()