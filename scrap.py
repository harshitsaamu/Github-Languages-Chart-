import requests
from lxml import html
import matplotlib.pyplot as plt

USERNAME = "username"
PASSWORD = "password"

LOGIN_URL = "https://github.com/login"
URL = "https://github.com/"+USERNAME+"?tab=following"

languages=[]
output=[]
occurence=[]
def main():
    session_requests = requests.session()
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='authenticity_token']/@value")))[0]
    print(authenticity_token)
    # Create payload
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "authenticity_token": authenticity_token
    }

    # Perform login
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # Scrape url
    result = session_requests.get(URL, headers = dict(referer = URL))
    tree = html.fromstring(result.content)
    bucket_names = tree.xpath("//*[@id='js-pjax-container']/div/div[2]/div/div/div/a/span[2]/text()")
    for i in bucket_names:
        print("username:"+i)
        profile(session_requests,i)
    print(languages)
    for i in languages:
        if i not in output:
            output.append(i)
    for i in output:
        occurence.append(languages.count(i))

    #ploting graph
    plt.pie(occurence,labels=output,autopct='%1.1f%%')
    plt.axis('equal')
    plt.show()

def profile(session,username):
    url_git="https://github.com/"
    result=session.get(url_git+username+"?tab=repositories",headers = dict(referer = url_git+username+"?tab=repositories"))
    tree = html.fromstring(result.content)
    bucket_names = tree.xpath("//*[@id='user-repositories-list']/ul/li/div/h3/a/text()")
    lang=tree.xpath("//*[@id='user-repositories-list']/ul/li/div[3]/span[2]/text()")
    for i in bucket_names:
        print(i)
    for i in lang:
        languages.append(i.strip())


if __name__ == '__main__':
    main()
