import ftplib
import io
import csv


class ChimolaFTP:

    def __init__(self, hostname, username, password):
        self._username = username
        self._password = password
        self._hostname = hostname
        self._ftp = ftplib.FTP()

    def upload_asTXT(self, filename, feed):
        print("The feed has {} itmes to upload as '{}'...".format(
            feed.size(), filename))
        self._ftp.connect(self._hostname)
        print("login into {} as {} via FTP...".format(
            self._hostname, self._username))
        response = self._ftp.login(self._username, self._password)
        print(response)
        try:
            print("changing directory to {}...".format(self._ftp.pwd()))
            response = self._ftp.cwd("public_html")
            print(response)
            out = io.BytesIO()
            csv_out = io.TextIOWrapper(out, encoding='utf-8')
            ChimolaFTP.__writefeed(csv_out, feed)
            csv_out.flush()
            out.flush()
            out.seek(0)
            print("Uploading {}...".format(filename))
            response = self._ftp.storlines("STOR " + filename, out)
            print(response)
        except Exception as ex:
            print(ex)
            raise
        finally:
            print("closing output file...")
            out.close()
            print("Output succesfully closed!")

    def upload(self, filepath):
        self._ftp.connect(self._hostname)
        print("login into {} as {} via FTP...".format(
            self._hostname, self._username))
        response = self._ftp.login(self._username, self._password)
        print(response)
        try:
            print("changing directory to {}...".format(self._ftp.pwd()))
            response = self._ftp.cwd("public_html")
            print(response)
            fileh = filepath.split('/')
            filename = fileh[len(fileh)-1]
            print("Uploading {}...".format(filename))
            response = self._ftp.storlines(
                "STOR " + filename, open(filepath, 'rb'))
            print(response)
        except Exception as ex:
            print(ex)
            raise

    @staticmethod
    def __writefeed(csv_out, feed):
        csvwriter = csv.writer(csv_out, delimiter='\t')
        line = feed.header()
        print("Writting header: '{}'...".format(line))
        csvwriter.writerow(line)
        print("Header OK.")
        for item in feed.items:
            line = item.to_row()
            print("Writting line: '{}'...".format(line))
            csvwriter.writerow(line)
            print("Line OK.")
