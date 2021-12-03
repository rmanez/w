from pymongo import MongoClient
import json

class MongoRepository:

    def open_connection(self, user, pwd, url, db):
        # connection = MongoClient("mongodb://APPLMONDLAKE_CONSULTA:o82hPQmXnZ@10.201.9.237:27017/datalake")
        # return connection;
        s = "mongodb://" + user + ":" + pwd + "@" + url + "/" + db
        connection = MongoClient(s)
        return connection;


    def get_collection(self, connection, db, collection):
        collect = connection[db][collection]
        return collect


    def save(self, obj):
        user = 'ApplClassifSinistro'
        pwd = 'GOIu8Ag0T9'
        url = 'srvmqr01d.tokiomarine.com.br:27017'
        db = 'dbClassifSinistro'
        col = 'ia-modelos'
        connection = self.open_connection(user, pwd, url, db)
        coltab = self.get_collection(connection, db, col)
        jsonStr = json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        d = json.loads(jsonStr)
        coltab.drop()
        coltab.insert(d, check_keys=False)
        connection.close()


    def set_processed(self, hash):
        user = 'ApplClassifSinistro'
        pwd = 'GOIu8Ag0T9'
        url = 'srvmqr01d.tokiomarine.com.br:27017'
        db = 'dbClassifSinistro'
        col = 'ia-vistoria-dataset'
        try:
            connection = self.open_connection(user, pwd, url, db)
            coltab = self.get_collection(connection, db, col)
            query = {'hash': hash}
            newvalues = {"$set": {"processado": "1"}}
            coltab.update_one(query, newvalues)

        except:
            print("error ...")
        finally:
            connection.close()

