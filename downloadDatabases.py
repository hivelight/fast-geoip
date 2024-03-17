import os, zipfile, glob, shutil
import processGeoIpCsv as geoip
import requests


ZIP_FILENAME = "geolite.zip"
TEMPORAL_EXTRACTED_DIR = "geoip"

def rmtree(directory):
    shutil.rmtree(directory, ignore_errors=True)

# urllib.request.urlretrieve ("https://geoip.maxmind.com/app/geoip_download?edition_id=GeoLite2-City-CSV&suffix=zip&license_key=" + os.environ["MAXMIND_LICENSE_KEY"], ZIP_FILENAME)


# Basic Authentication credentials
username = os.environ["ACCOUNT_ID"]
password = os.environ["MAXMIND_LICENSE_KEY"]

# URL to download the file
url = "https://download.maxmind.com/geoip/databases/GeoIP2-City-CSV/download?suffix=zip"

# Make a GET request with authentication
response = requests.get(url, auth=(username, password))

print("Status code:", response.status_code)

# Get the filename from the response headers
filename = response.headers.get("content-disposition").split("filename=")[-1]

# Save the file
with open(filename, "wb") as f:
    f.write(response.content)

# Extract the downloaded zip file
with zipfile.ZipFile(filename, 'r') as zip_ref:
    zip_ref.extractall(TEMPORAL_EXTRACTED_DIR)

rmtree(geoip.RAW_DATABASE_DIR)

extracted_dir = glob.glob('./'+TEMPORAL_EXTRACTED_DIR+'/GeoLite2-City-CSV_[0-9]*')[0]
os.rename(extracted_dir, geoip.RAW_DATABASE_DIR)

rmtree(TEMPORAL_EXTRACTED_DIR)
