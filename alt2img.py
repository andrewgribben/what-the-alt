import argparse
import requests
from bs4 import BeautifulSoup
import os
import shutil

# User-defined path to the Python virtual environment
virtualenv_path = '/Users/grib/invokeai/.venv'

parser = argparse.ArgumentParser(description='Extract alt text from images on a webpage and generate images using stable diffusion.')
parser.add_argument('url', type=str, help='URL of the webpage')
args = parser.parse_args()

url = args.url
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

counter = 1  # Counter variable to generate numerical names for images
image_data = []  # List to store image data (alt text and generated image name)

with open('alt_text.txt', 'w') as f:
    for img in soup.find_all('img'):
        if img.has_attr('alt') and img['alt'] != '':
            image_name = f'image{counter}.jpg'
            f.write(f'"{img["alt"]}" -S 1950357039 -s 100 -C 20 --fnformat {image_name}\n')
            image_data.append((img['alt'], image_name))
            counter += 1

virtualenv_activate = os.path.join(virtualenv_path, 'bin', 'activate')
invoke_script = os.path.join(virtualenv_path, 'bin/invoke.py')
os.system(f'source {virtualenv_activate}; python {invoke_script} --from_file alt_text.txt')

for alt_text, image_name in image_data:
    output_image_path = os.path.join(virtualenv_path, 'outputs', image_name)
    destination_path = os.path.join(os.getcwd(), image_name)
    shutil.move(output_image_path, destination_path)

def generate_html(image_data):
    with open('output.html', 'w') as html_file:
        html_file.write('<html>\n<body>\n')

        for alt_text, image_name in image_data:
            html_file.write('<figure>\n')
            html_file.write(f'  <img src="{image_name}" alt="{alt_text}">\n')
            html_file.write(f'  <figcaption>{alt_text}</figcaption>\n')
            html_file.write('</figure>\n\n')

        html_file.write('</body>\n</html>')

generate_html(image_data)
