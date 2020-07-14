import shutil, random, os, platform, urllib.request, time, ctypes
from bs4 import BeautifulSoup as bs

# --- for user input

url = urllib.request.urlopen('https://www.unsplash.com') # main url
url_imageserver = 'https://images.unsplash.com/photo-' # image server url

# ---

def download_image(i,temp_path):
    image_name = 'image-{}.jpg'.format(image_count)
    full_path = '{}\{}'.format(temp_path,image_name)
    urllib.request.urlretrieve(i, full_path)
    print('Item {} has successfully saved as {}.'.format(n+1,image_name))

def remove_temp_path():
    try:
        shutil.rmtree(temp_path)
    except OSError as e:
        print("Error: {}".format(e.strerror))

def set_wallpaper(x):
    if user_platform == 'Windows': #windows support
        image_path = temp_path + r'\image-{}.jpg'.format(x)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
        print('Windows: Wallpaper set to image-{}.jpg.'.format(x))
    elif user_platform == 'Linux': #gnome gui support: I will fix this soon
        os.system('/usr/bin/gsettings set org.gnome.desktop.background picture-uri' + image_path)
    elif user_platform == 'Darwin': #mac support: I will fix this soon
        return
    else:
        print("Error: Unknown platform: {}".format(user_platform))
    time.sleep(1)



# ---

user_platform = platform.system()
temp_path = os.getcwd() + r'\temp'
while os.path.isdir(temp_path):
    remove_temp_path()

os.mkdir(temp_path)

"""
for i in bs(url, 'lxml').findAll('source'):
    image_urls.append(i.get('srcset').split('?',1)[0])
for i in bs(url, 'lxml').findAll('img'):
    image_urls.append(i.get('src').split('&w=',1)[0])
"""
image_count = 0
image_urls = []
for i in bs(url, 'lxml').find_all('img'):
    image_urls.append(i.get('src').split('&w=',1)[0])

try:
    for n,i in enumerate(image_urls):
        if url_imageserver in i:
            image_count += 1
            download_image(i,temp_path)
        else:
            print('Item {} did not match url_imageserver specifications.'.format(n+1))
        print(i,end='\n\n')

except OSError as e:
    print("Error: {}".format(e.strerror))
    time.sleep(1)

# ---

set_wallpaper(random.randint(1,image_count))
remove_temp_path()

# ---
