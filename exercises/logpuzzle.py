
import os
import re
import sys
import urllib.request



def url_sort_key(url):
  match = re.search(r'-(\w+)-(\w+)\.\w+', url)
  if match:
    return match.group(2)
  else:
    return url


def read_urls(filename):
  
  underbar = filename.index('_')
  host = filename[underbar + 1:]

  
  url_dict = {}

  with open(filename) as f:
    for line in f:
      
      match = re.search(r'"GET (\S+)', line)
      

      if match:
        path = match.group(1)
        
        if 'puzzle' in path:
          url_dict['http://' + host + path] = 1

    return sorted(url_dict.keys(), key=url_sort_key)



def download_images(img_urls, dest_dir):
 
  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

  index = open(os.path.join(dest_dir, 'index.html'), 'w')
  index.write('<html><body>\n')

  i = 0
  for img_url in img_urls:
    local_name = 'img%d' % i
    print('Retrieving...', img_url)
    urllib.request.urlretrieve(img_url, os.path.join(dest_dir, local_name))

    index.write('<img src="%s">' % (local_name,))
    i += 1

  index.write('\n</body></html>\n')
  index.close()


def main():
  args = sys.argv[1:]

  if not args:
    print('usage: [--todir dir] logfile ')
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print('\n'.join(img_urls))

if __name__ == '__main__':
  main()
