import sys
import pandas as pd
import math
from datetime import datetime
import cromossomo as crom
from pymongo import MongoClient
import json


def open_connection(user, pwd, url, db):
    s = "mongodb://" + user + ":" + pwd + "@" + url + "/" + db
    connection = MongoClient(s)
    return connection;


def get_collection(connection, db, collection):
    collect = connection[db][collection]
    return collect


def getCursor(user, pwd, url, db, col, hash):

    connection = open_connection(user, pwd, url, db)
    coltab = get_collection(connection, db, col)
    # query = {'hash': hash, 'processado': 0}
    query = {'hash': hash}
    cursor = coltab.find(query, no_cursor_timeout=True).batch_size(100000)
    connection.close()
    c = cursor[0]
    return c

def get_cromossomo(c):
    dict = c['value_object']
    json_string = json.dumps(dict)
    obj = json.loads(json_string)
    c = crom.Cromossomo(obj['idx'], obj['gens'], obj['fit'])
    cromos = []
    cromos.insert(len(cromos), c)
    return cromos


def get_classif_values(c):
    return c['classif_values']


def euclides(list_val_result_croms, classif_values):
    predict_list = []

    for v in list_val_result_croms:
        min = -1
        predict  = -1
        for c in classif_values:
            dist = math.sqrt(math.pow(c - v, 2))
            if min == -1:
                min = dist
                predict = c
            else:
                if dist <= min:
                    min = dist
                    predict = c
        predict_list.insert(len(predict_list), predict)

    return predict_list


def mult(dfds, bag_cromos, idxattrs, classif_values):

    df = dfds.copy()

    for idxcroms in range(len(bag_cromos)):
        #fit = bag_fit[idxcroms]
        cr = bag_cromos[idxcroms]
        list_val_result_croms = []

        for j, row in df.iterrows():
            sum = 0
            for k in range(len(idxattrs)):
                v = row[idxattrs[k]] * cr.gens[k]
                sum = sum + v
            list_val_result_croms.insert(len(list_val_result_croms), sum)

        # . to ,
        lvs = []
        for f in list_val_result_croms:
            vs = str(f).replace('.', ',')
            lvs.insert(len(lvs), vs)

        list_predict = euclides(list_val_result_croms, classif_values)
        df['cr-' + str(idxcroms)] = list_predict
        return df


def filter(dfds):
    l = dfds.columns.values.tolist()
    attrs = []
    for i in range(len(l)):
        if ('IDN' != l[i]) and ('CLASSIF_TARGET' != l[i]):
            attrs.insert(len(attrs), i)
    return attrs


def create_data(idn, binary_values):
    dic = { 'IDN':[idn] }
    for i in range(len(binary_values)):
        dic[str(i)] = [int(binary_values[i])]
    dic['CLASSIF_TARGET'] = [-1]
    df = pd.DataFrame(dic)
    return df


def filter(dfds):
    l = dfds.columns.values.tolist()
    attrs = []
    for i in range(len(l)):
        if ('IDN' != l[i]) and ('CLASSIF_TARGET' != l[i]):
            attrs.insert(len(attrs), i)
    return attrs


def classific(idn, binary_values):
    user = 'ApplClassifSinistro'
    pwd = 'GOIu8Ag0T9'
    url = 'srvmqr01d.tokiomarine.com.br:27017'
    db = 'dbClassifSinistro'
    col = 'ia-modelos'
    hash = 'c6118d2b-ce2d-42a5-8f9e-e12a86903a0c'

    cursor = getCursor(user, pwd, url, db, col, hash)
    bag_cromos = get_cromossomo(cursor)
    classif_values = get_classif_values(cursor)
    data_vistoria = create_data(idn, binary_values)
    total_rows = 1
    attrs = filter(data_vistoria)

    if len(bag_cromos[0].gens) != len(attrs):
        raise Exception('Error', 'estrutura inválida')

    df = mult(data_vistoria, bag_cromos, attrs, classif_values)
    ret = df['cr-0'][0]
    print( '--> ', ret)
    return str(ret)

#classific(21577000104, '0000000000000000000000000000000')
