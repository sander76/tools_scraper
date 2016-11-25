import argparse
from ftplib import FTP
import os


def walker(source_folder):
    src = source_folder
    for root, dirs, files in os.walk(source_folder):
        rel = os.path.relpath(root, src)
        for file in files:
            if os.path.splitext(file) == 'pdf':
                pass
        print(rel)


class FtpUploader:
    def __init__(self, address, ftp_folder, user, passwd, pdf_source_folder):
        self.ftp = FTP(address)
        self.ftp.login(user, passwd)
        self.ftp_folder = ftp_folder
        self.pdf_source_folder = pdf_source_folder

    def searchpdf(self):
        for root, dirs, files in os.walk(self.pdf_source_folder):
            rel = os.path.relpath(root, self.pdf_source_folder)
            for file in files:
                ext = os.path.splitext(file)
                if ext[1] == '.pdf':
                    # found a pdf. Upload it !
                    rel_path = self.create_ftp_path(rel)
                    source_path = os.path.join(root, file)
                    self.upload(source_path, rel_path, file)
                    # print(rel)

    def upload(self, source, target, file):
        # change to the appropriate ftp folder.
        self.ftp.cwd(target)
        with open(source, 'rb') as fl:
            self.ftp.storbinary('STOR {}'.format(file), fl)
        print(self.ftp.retrlines('LIST'))

    def create_ftp_path(self, rel_path):
        return os.path.join(self.ftp_folder, rel_path)


parser = argparse.ArgumentParser()
parser.add_argument("ftp_address")
parser.add_argument("ftp_folder")
parser.add_argument("user")
parser.add_argument("passwd")
parser.add_argument("pdf_source_folder")

if __name__ == "__main__":
    args = parser.parse_args()
    upl = FtpUploader(args.ftp_address, args.ftp_folder, args.user, args.passwd, args.pdf_source_folder)
    upl.searchpdf()
    # walker(args.source_folder)
