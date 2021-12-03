import sys
from pymongo import MongoClient
import pandas as pd

class ReaderDataSet:

    def open_connection(self, user, pwd, url, db):
        #connection = MongoClient("mongodb://APPLMONDLAKE_CONSULTA:o82hPQmXnZ@10.201.9.237:27017/datalake")
        #return connection;
        s = "mongodb://"+user + ":" + pwd + "@" + url + "/" + db
        connection = MongoClient(s)
        return connection;

    def get_collection(self, connection, db, collection):
        collect = connection[db][collection]
        return collect



    def make_df(self, cursor):
        df = pd.DataFrame(cursor[0]["lessons"])
        return df


    def read(self, hash):
        user = 'ApplClassifSinistro'
        pwd = 'GOIu8Ag0T9'
        url = 'srvmqr01d.tokiomarine.com.br:27017'
        db = 'dbClassifSinistro'
        col = 'ia-vistoria-dataset'
        df = None
        try:
            connection = self.open_connection(user, pwd, url, db)
            coltab = self.get_collection(connection, db, col)
            #query = {'hash': hash, 'processado': 0}
            query = {'hash': hash }
            cursor = coltab.find(query, no_cursor_timeout=True).batch_size(100000)
            s = cursor.count()
            if s == 0:
                raise TypeError ("No lessons found")
            df = self.make_df(cursor)

        except Exception as e:
            print('error ...', e)

        finally:
            connection.close()

        return df


    def readcsv(self, path):
        df = pd.read_csv(path, sep=';')
        return df