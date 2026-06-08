#!/usr/bin/env python
import json
import tarfile
import shutil
import subprocess
from dataclasses import dataclass
from sys import argv, exit
from urllib.request import urlopen, urlretrieve
from pathlib import Path
from argparse import ArgumentParser, BooleanOptionalAction
from os import path

CWD = Path(path.realpath(__file__)).parent
TIMEOUT_SEC = 10
RELEASE_URL = "https://api.github.com/repos/DoumanAsh/maxmind-db/releases/latest"

COUNTRY_DB_TARBALL = "geolite-country.mmdb.tar.gz"
CITY_DB_TARBALL = "geolite-cty.mmdb.tar.gz"

@dataclass
class AssetDetails:
    name: str
    digest: str
    browser_download_url: str

    def get_digest(self) -> str:
        digest = self.digest.split(':')
        return digest[1]


@dataclass
class AssetInfo:
    id: str
    url: str
    name: str

    def fetch_details(self) -> AssetDetails:
        with urlopen(self.url, timeout=TIMEOUT_SEC) as response:
            body = json.load(response)
            return AssetDetails(name=body['name'], digest=body['digest'], browser_download_url=body['browser_download_url'])


def fetch_release_info():
    with urlopen(RELEASE_URL, timeout=TIMEOUT_SEC) as response:
        body = json.load(response)
        assets = body.get('assets', None)
        if assets is None:
            raise Exception(f"{RELEASE_URL}: missing 'assets' field")

        for asset in assets:
            yield AssetInfo(id=asset['id'], url=asset['url'], name=asset['name'])

def download_asset_if_outdated(asset: AssetDetails, output: Path, pre_hook: Path, post_hook: Path):
    output_dest = output.joinpath(asset.name)
    output_dest_checksum = output.joinpath(f"{asset.name}.checksum")
    digest = asset.get_digest()

    try:
        with output_dest_checksum.open('r') as output_dest_checksum_fd:
            if digest.strip() == output_dest_checksum_fd.read().strip():
                print(f"{output_dest_checksum}: Checksum match, skipping...")
                return
    except FileNotFoundError:
        pass

    if not output_dest.is_file():
        print(f"{asset.browser_download_url}: Downloading...")
        urlretrieve(asset.browser_download_url, output_dest)

    if pre_hook.exists():
        subprocess.run(["sh", pre_hook], shell=False, check=False)

    print(f"{asset.browser_download_url}: Extracting...")
    with tarfile.open(output_dest, "r:gz") as output_tar:
        for member in output_tar.getmembers():
            if member.name.endswith("mmdb"):
                data = output_tar.extractfile(member)
                member_file_name = Path(member.name).name
                with output.joinpath(member_file_name).open('wb') as output:
                    shutil.copyfileobj(data, output)

    output_dest.unlink(True)
    with output_dest_checksum.open('w') as output_dest_checksum:
        output_dest_checksum.write(digest.strip())

    if post_hook.exists():
        subprocess.run(["sh", post_hook], shell=False, check=False)


def main(args: list[str]):
    cli = ArgumentParser(prog="maxmind-db-updater", description="Script to download maxmind DB")
    cli.add_argument("-o", "--output", default=CWD, required=False, type=Path, help="Folder where to to download db files. Defaults to script's folder")
    cli.add_argument("--country", action=BooleanOptionalAction, required=False, default=False, help="Specifies whether to download country database")
    cli.add_argument("--city", action=BooleanOptionalAction, required=False, default=False, help="Specifies whether to download city database")
    cli.add_argument("--pre-update-hook", type=Path, required=False, default=CWD.joinpath("pre-update-hook.sh"), help="Specifies script to run before update")
    cli.add_argument("--post-update-hook", type=Path, required=False, default=CWD.joinpath("post-update-hook.sh"), help="Specifies script to run after update")
    args = cli.parse_args(args)

    if not args.output.is_dir():
        print(f"{args.output}: No such folder...")
        exit(1)

    download_list = set()
    if args.country:
        download_list.add(COUNTRY_DB_TARBALL)
    if args.city:
        download_list.add(CITY_DB_TARBALL)

    if not download_list:
        print("You should specify --country/--city to select which database to download")
        exit(1)

    for asset in fetch_release_info():
        if asset.name in download_list:
            download_asset_if_outdated(asset.fetch_details(), args.output, args.pre_update_hook, args.post_update_hook)

if __name__ == "__main__":
    main(argv[1:])
