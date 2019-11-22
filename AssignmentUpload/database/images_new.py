from io import BytesIO, TextIOWrapper

from google_images_download import google_images_download
import sys

def url(keyword):
	old_stdout = sys.stdout
	sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
	response = google_images_download.googleimagesdownload()

	arguments = {
	    "keywords": keyword,
	    "limit": 3,
	    "print_urls": True,
	    "size": "large",
	}
	paths = response.download(arguments)

	sys.stdout.seek(0)
	output = sys.stdout.read()

	sys.stdout.close()
	sys.stdout = old_stdout

	for line in output.split("\n"):
	    if line.startswith("Image URL:"):
	        print(line.replace("Image URL: ", ""))
	        break

url("Mysore")
