## maxmind db

This repo contains script to download and update maxmind database via provided [release](https://github.com/DoumanAsh/maxmind-db/releases/tag/latest)

### Databases

Following databases are stored repo's release:

- [geolite-country.mmdb.tar.gz](https://github.com/DoumanAsh/maxmind-db/releases/download/latest/geolite-country.mmdb.tar.gz) - GeoLite2 database with country database which provides near perfect accuracy
- [geolite-cty.mmdb.tar.gz](https://github.com/DoumanAsh/maxmind-db/releases/download/latest/geolite-cty.mmdb.tar.gz) - GeoLite2 database with city information. While country information has high accuracy, city information, depending on country, might not be reliable.


### Update script

Following [script](https://github.com/DoumanAsh/maxmind-db/blob/master/updater) can be used to keep database up to date

It expects to have write permission in folder where database is downloaded and extracted.

Alongside the database file it shall create `<file name>.checksum` in order to detect new release.
Deleting this file allows script to re-download database again
