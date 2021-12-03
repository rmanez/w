import reader as rd
import model as mod

import mongo_repository as mr

import cromossomo_generator as cg
import filter_attrs as filat
import filter_classif as filcf
import multiply as mply
from datetime import datetime
#from random import randrange
#from random import random


def print_bag_cromos(bag_cromos, total_rows):
    for cr in bag_cromos:
        cr.print(total_rows)



def calc_fit_pct(cromo_bag, total):
    for cr in cromo_bag:
        fit = cr.fit
        fit['fit_pct'] = fit['fit']/total
        fit['fit_pct_total'] = total
        #print(fit['fit_pct'])



def gen_classif_values(data_set_lessons):
    classif_values = []
    c0 = []
    c1 = []
    for v in data_set_lessons['CLASSIF_TARGET'].unique():
        vs = str(v).replace(",", ".")
        df = data_set_lessons.loc[data_set_lessons['CLASSIF_TARGET'] == v]
        qtde = df.shape[0]
        c0.insert(len(c0), float(vs))
        c1.insert(len(c1), qtde)
    classif_values.insert(0, c0)
    classif_values.insert(1, c1)
    return classif_values


def main():
    CROMOS_QTDE = 8
    SUN_SIZE = 4
    versao = 'dataset-012'
    hash = 'c6118d2b-ce2d-42a5-8f9e-e12a86903a0c'

    rr = rd.ReaderDataSet()
    data_set_lessons = rr.read(hash)
    total_rows = data_set_lessons.shape[0]
    attrs = filat.FilterAttrs.filter(data_set_lessons)
    genes_size = len(attrs)
    classif_values = gen_classif_values(data_set_lessons)
    bag_cromos = cg.CromosGenerator.gen(classif_values, genes_size, CROMOS_QTDE)
    list_classif = filcf.FilterClassif.filter_classif(data_set_lessons)

    df = mply.Mult.mult(data_set_lessons, bag_cromos, attrs, classif_values, list_classif)
    # START NEW GEN
    total = sum([cr.fit['fit'] for cr in bag_cromos])
    calc_fit_pct(bag_cromos, total)

    all_cromos = [] + bag_cromos

    for i in range(4):
        print(i)
        start_idx = (CROMOS_QTDE)+i*SUN_SIZE
        new_genes = cg.CromosGenerator.new_generation(bag_cromos, total, SUN_SIZE)
        new_cromos = cg.CromosGenerator.new_gen(classif_values, new_genes, start_idx)
        cg.CromosGenerator.cross_over(bag_cromos)

        df = mply.Mult.mult(data_set_lessons, new_cromos, attrs, classif_values, list_classif)
        total = sum([cr.fit['fit'] for cr in new_cromos])
        calc_fit_pct(new_cromos, total)

        all_cromos = all_cromos + new_cromos
        n = 2
        bag_cromos = cg.CromosGenerator.takeout_n_worst(bag_cromos, n) + cg.CromosGenerator.pickup_n_best(new_cromos, n)


    best = cg.CromosGenerator.pickup_n_best(all_cromos, 1)[0]
    best.print(total_rows)

    morepo = mr.MongoRepository()
    modelo = mod.Model('Genetic-Algorithm-2', hash, classif_values[0], best)
    morepo.save(modelo)
    morepo.set_processed(hash)

    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    df.to_csv('C:\_app\dataset\genetics\\' + versao + '-res-crs-' + date_time + '.csv', sep=';', index=False)

    print('fim')



main()



