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

    def get_table_records(self, tableName):
        cursor = self.connection.cursor()
        if tableName is None:
            print("Input file not structured correctly")
            return
        cursor.execute(
            f"SELECT * FROM {tableName}")
        columns = [col[0] for col in cursor.description]
        cursor.rowfactory = lambda *args: dict(zip(columns, args))
        for record in cursor:
            yield record
