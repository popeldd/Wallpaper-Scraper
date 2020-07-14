import shutil, random, os, platform, urllib.request, time, ctypes
from bs4 import BeautifulSoup as bs

# ---

url = urllib.request.urlopen('https://www.unsplash.com') # main url
url_imagenameserver = 'https://images.unsplash.com/photo-' # image server url

# ---

def check_temp_path():
    while os.path.isdir(temp_path):
        remove_temp_path()
def make_temp_path():
    global temp_path, temp_path_full
    if user_platform == 'windows':
        temp_path = os.getcwd() + r'\temp'
        temp_path_full = '{}\{}'
        check_temp_path()
        os.mkdir(temp_path)
    elif user_platform == 'linux':
        temp_path = os.getcwd() + '/temp'
        temp_path_full = '{}/{}'
        check_temp_path()
        os.mkdir(temp_path)
    elif user_platform == 'debian':
        return
    else:
        print('Error: Unknown platform: {}'.format(user_platform))

def remove_temp_path():
    try:
        shutil.rmtree(temp_path)
    except OSError as e:
        print('Error: {}'.format(e.strerror))

def download_image(i,temp_path):
    image_name = 'image-{}.jpg'.format(image_count)
    full_path = temp_path_full.format(temp_path,image_name)
    urllib.request.urlretrieve(i, full_path)
    print('Item {} has successfully saved as {}.'.format(n+1,image_name))

def set_wallpaper(x):
    if user_platform == 'windows':
        image_path = temp_path + r'\image-{}.jpg'.format(x)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
        time.sleep(1)
        remove_temp_path()
    elif user_platform == 'linux':
        image_path = temp_path + '/image-{}.jpg'.format(x)
        os.system('gsettings set org.gnome.desktop.background picture-uri {}'.format(image_path))
    elif user_platform == 'darwin':
        return
    else:
        print('Error: Unknown platform: {}'.format(user_platform))
    print('{}: Wallpaper set to image-{}.jpg.'.format(user_platform.capitalize(), x))

# ---

if __name__ == '__main__':
    user_platform = platform.system().lower()
    make_temp_path()

    image_urls = []
    for i in bs(url, 'lxml').findAll('img'):
        image_urls.append(i.get('src').split('&w=',1)[0])

    try:
        image_count = 0
        for n,i in enumerate(image_urls):
            if url_imagenameserver in i:
                image_count += 1
                download_image(i,temp_path)
            else:
                print('Item {} did not match url_imagenameserver specifications.'.format(n+1))
            print(i,end='\n\n')

    except OSError as e:
        print("Error: {}".format(e.strerror))
        time.sleep(1)

# ---

    set_wallpaper(random.randint(1,image_count))

# ---
