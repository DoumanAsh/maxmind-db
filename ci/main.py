import requests
from requests.auth import HTTPBasicAuth

from sys import exit
from os import path, mkdir, environ
from datetime import datetime, timezone

SCRIPT_DIR = path.dirname(__file__)
DB_DIR = path.join(SCRIPT_DIR, "..", "db")
DOWNLOAD_LIST = [
    #("geolite-cty.csv.zip", "https://download.maxmind.com/geoip/databases/GeoLite2-City-CSV/download?suffix=zip"),
    ("geolite-cty.mmdb.tar.gz", "https://download.maxmind.com/geoip/databases/GeoLite2-City/download?suffix=tar.gz"),
    #("geolite-country.csv.zip", "https://download.maxmind.com/geoip/databases/GeoLite2-Country-CSV/download?suffix=zip"),
    ("geolite-country.mmdb.tar.gz", "https://download.maxmind.com/geoip/databases/GeoLite2-Country/download?suffix=tar.gz"),
]

def main():
    now = datetime.now(timezone.utc);

    user_name = environ.get("MAXMIND_ACCOUNT_ID", None)
    if user_name is None:
        print("env::MAXMIND_ACCOUNT_ID is not specified")
        exit(1)
    password = environ.get("MAXMIND_LICENSE_KEY", None)
    if password is None:
        print("env::MAXMIND_LICENSE_KEY is not specified")
        exit(1)

    if not path.isdir(DB_DIR):
        print("{}: Does not exists, creating...".format(DB_DIR))
        mkdir(DB_DIR)

    session = requests.session();
    session.auth = HTTPBasicAuth(user_name, password)

    for item in DOWNLOAD_LIST:
        output_file = path.join(DB_DIR, item[0])
        print("{}: Downloading from {}".format(output_file, item[1]))
        with session.get(item[1], stream=True) as request:
            request.raise_for_status()
            with open(output_file, "wb") as output_fd:
                for chunk in request.iter_content(chunk_size=16384):
                    output_fd.write(chunk)

    timestamp_record = path.join(DB_DIR, "timestamp")
    with open(timestamp_record, "w") as timestamp_fd:
        timestamp_fd.write(now.isoformat("T"))

if __name__ == "__main__":
    main()
