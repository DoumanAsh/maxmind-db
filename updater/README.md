# maxmind updater

Simple [script](./maxmind-db-updater.py) to keep maxmind db updated

## Usage

```
usage: maxmind-db-updater [-h] [-o OUTPUT] [--country | --no-country] [--city | --no-city] [--pre-update-hook PRE_UPDATE_HOOK] [--post-update-hook POST_UPDATE_HOOK]

Script to download maxmind DB

options:
  -h, --help            show this help message and exit
  -o, --output OUTPUT   Folder where to to download db files. Defaults to script's folder
  --country, --no-country
                        Specifies whether to download country database
  --city, --no-city     Specifies whether to download city database
  --pre-update-hook PRE_UPDATE_HOOK
                        Specifies script to run before update
  --post-update-hook POST_UPDATE_HOOK
                        Specifies script to run after update
```
