import oracledb


class Database:
    def __init__(self, host, sid):
        db = f"""(DESCRIPTION =
        (ADDRESS = (PROTOCOL = TCP)(HOST = {host})(PORT = 1521))
        (CONNECT_DATA =
            (SID = {sid})
        ))"""
        self.connection = oracledb.connect(
            user="pap325", password="ftSFH8N3t8S", dsn=db)
    
    def get_connection(self):
        return self.connection
