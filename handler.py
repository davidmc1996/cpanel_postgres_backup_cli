import requests

class Handler:
    def __init__(self, conn):
        self.cookies = []
        self.response = None
        self.conn = conn
        self.base_url = f"https://{conn['hostname']}:2083"
        self.error_msg = None
        self.output = "download"
        self.what = "structureanddata"
        self.d_format = "copy"
        self.sd_format = "copy"

    def login(self):
        data = {"user": self.conn["username"], "pass": self.conn["password"]}
        headers = {
            "Accept": "*/*",
            "Accept-Language": "es-PE,es-419;q=0.9,es;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-type": "application/x-www-form-urlencoded",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/logout/?locale=en",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
        }
        try:
            response = requests.post(
                f"{self.base_url}/login/?login_only=1", data=data, headers=headers
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            self.error_msg = str(err)
            return False

        cpsession_cookie = response.cookies.get("cpsession")
        if not cpsession_cookie:
            self.error_msg = "No se encontró la cookie 'cpsession' en la respuesta."
            return False

        self.cookies = {"name": "cpsession", "value": cpsession_cookie}
        self.response = response.json()
        return True

    def export(self):
        data = {
            "d_format": self.d_format,
            "what": self.what,
            "sd_format": self.sd_format,
            "output": self.output,
            "action": "export",
            "subject": "database",
            "server": "/var/run/postgresql:5432:allow",
            "database": self.conn["database"],
            "loginServer": "/var/run/postgresql:5432:allow",
            "loginUsername": self.conn["username"],
            "loginPassword_deffb85a7cd9c543c9dfb5d5c1bb2c45": self.conn["password"],
            "loginDefaultDB": "",
            "loginSubmit": "Autenticar",
        }
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "es-PE,es-419;q=0.9,es;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": f"_ga=GA1.3.268843399.1668628303; session_locale=en; _gid=GA1.3.1076989255.1672262314; timezone=America/Bogota; {self.cookies['name']}={self.cookies['value']}; PPA_ID=cc04c58b02bcf338b8d5a61864109b94;",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/cpsess4470850214/3rdparty/phpPgAdmin/database.php?subject=database&action=export&server=%2Fvar%2Frun%2Fpostgresql%3A5432%3Aallow&database={self.conn['database']}",
            "Sec-Fetch-Dest": "frame",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
        }
        try:
            response = requests.post(
                f"{self.base_url}{self.response['security_token']}/3rdparty/phpPgAdmin/dbexport.php",
                data=data,
                headers=headers,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            self.error_msg = str(err)
            return False

        return response.content if self.output == "gzipped" else response.text

    def logout(self):
        headers = {"Cookie": "cpsession=closed"}
        try:
            response = requests.get(
                f"{self.base_url}/logout/?locale=en", headers=headers
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            self.error_msg = str(err)
            return False

        return True

    def get_error_msg(self):
        return self.error_msg

    def set_conn(self, conn):
        self.conn = conn

    def set_output(self, output):
        if output == "plain":
            self.output = "download"
        elif output == "zip":
            self.output = "gzipped"
        else:
            self.output = "download"

    def set_what(self, what):
        if what == "data":
            self.what = "dataonly"
        elif what == "structure":
            self.what = "structureonly"
        elif what == "structuredata":
            self.what = "structureanddata"
        else:
            self.what = "structureanddata"

    def set_format(self, format):
        if format == "sql":
            self.d_format = "sql"
            self.sd_format = "sql"
        elif format == "copy":
            self.d_format = "copy"
            self.sd_format = "copy"
        else:
            self.d_format = "copy"
            self.sd_format = "copy"
