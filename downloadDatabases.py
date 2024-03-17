import urllib.request, os, zipfile, glob, shutil
import processGeoIpCsv as geoip
from base64 import b64encode

ZIP_FILENAME = "geolite.zip"
TEMPORAL_EXTRACTED_DIR = "geoip"

def rmtree(directory):
    shutil.rmtree(directory, ignore_errors=True)

# urllib.request.urlretrieve ("https://geoip.maxmind.com/app/geoip_download?edition_id=GeoLite2-City-CSV&suffix=zip&license_key=" + os.environ["MAXMIND_LICENSE_KEY"], ZIP_FILENAME)


# Basic Authentication credentials
username =  os.environ["ACCOUNT_ID"]
password =  os.environ["MAXMIND_LICENSE_KEY"]

# Encode username and password in base64
credentials = f"{username}:{password}".encode('ascii')
base64_credentials = b64encode(credentials).decode('ascii')

# URL with basic auth
url = f"https://download.maxmind.com/geoip/databases/GeoLite2-City-CSV/download?suffix=zip"
request = urllib.request.Request(url)
request.add_header('Authorization', f'Basic {base64_credentials}')

# Download the file
with urllib.request.urlopen(request) as response, open(ZIP_FILENAME, 'wb') as out_file:
    shutil.copyfileobj(response, out_file)

# Extract the downloaded zip file
with zipfile.ZipFile(ZIP_FILENAME, 'r') as zip_ref:
    zip_ref.extractall(TEMPORAL_EXTRACTED_DIR)

rmtree(geoip.RAW_DATABASE_DIR)

extracted_dir = glob.glob('./'+TEMPORAL_EXTRACTED_DIR+'/GeoLite2-City-CSV_[0-9]*')[0]
os.rename(extracted_dir, geoip.RAW_DATABASE_DIR)

rmtree(TEMPORAL_EXTRACTED_DIR)
