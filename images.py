import requests
import shutil
import os.path

def main():
    r = requests.get('https://commons.wikimedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Commons_featured_widescreen_desktop_backgrounds&cmlimit=500&cmtype=file&format=json')
    for item in r.json()['query']['categorymembers']:
        r2 = requests.get('https://commons.wikimedia.org/w/api.php?action=query&pageids={}&prop=imageinfo&iiprop=url&format=json'.format(item['pageid']))
        url = r2.json()['query']['pages'][str(item['pageid'])]['imageinfo'][0]['url']
        path = '/Users/nschaaf/Pictures/Feed/' + ''.join(item['title'].split(':')[1:])
        if os.path.isfile(path):
            continue
        print(url)
        print(path)
        r3 = requests.get(url, stream=True)
        with open(path, 'wb') as f:
            shutil.copyfileobj(r3.raw, f)
        f.close()


if __name__ == '__main__':
    main()
