import shutil, random, os, urllib.request, time, ctypes
from bs4 import BeautifulSoup as bs

# ---

url = urllib.request.urlopen('https://unsplash.com/')

# ---

def download_image(i,v,temp_path):
    image_name = 'image-{}.jpg'.format(i)
    full_path = '{}\{}'.format(temp_path,image_name)
    urllib.request.urlretrieve(v, full_path)
    print('{} saved.'.format(image_name))

#def seek_image(i,image_path):
    

# ---

image_urls = []
for i in bs(url, 'lxml').findAll('source'):
    image_urls.append(i.get('srcset').split('?',1)[0])
"""
for i in bs(url, 'lxml').findAll('img'):
    image_urls.append(i.get('src'))
"""
temp_path = os.getcwd() + r'\temp'
os.mkdir(temp_path)
try:
    for i,v in enumerate(image_urls):
        download_image(i,v,temp_path)
        print(v,end='\n\n')

except OSError as e:
    print("Error: {}".format(e.strerror))
    time.sleep(1)

# ---

image_path = temp_path + r'\image-{}.jpg'.format(random.randint(0,10))
ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
time.sleep(1)

# ---

try:
    shutil.rmtree(temp_path)
except OSError as e:
    print("Error: {}".format(e.strerror))

