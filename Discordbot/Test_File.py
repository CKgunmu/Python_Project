from google_images_download import google_images_download
import ssl
ssl._create_default_https_context = ssl._create_unverified_context()

def imageCrawaling(MyKeyword, dir):
    response = google_images_download.googleimagesdownload()
    arguments = {
        "keywords" : MyKeyword,
        "limit" : 20,
        "print_urls":True,
        "no_directory" : True,
        "output_directory":dir
    }
    paths = response.download(arguments)
    print(paths)

imageCrawaling('cat', './Image/')
