#!/usr/bin/env python

from sys import argv
from google_drive_downloader import GoogleDriveDownloader as gdd

if len(argv) is not 2:
    print("Error: missing ID of file to download")
    exit(1)

gdd.download_file_from_google_drive(file_id=argv[1],
                                    dest_path='/tmp/something.zip',
                                    unzip=True)
