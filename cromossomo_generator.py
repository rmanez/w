from operator import attrgetter
from random import random

import cromossomo as crom


def sort_two_cr(cromo_bag):
    parents = []
    for parent in range(2):
        m = -1
        while m == -1 and not (m in parents):
            start = 0
            finish = 0
            before = 0
            sorteio = random()
            for i in range(len(cromo_bag)):
                fit = cromo_bag[i].fit
                finish = start + fit['fit_pct']
                before = before + fit['fit_pct']
                if start <= sorteio and sorteio <= finish:
                    m = i
                    parents.insert(len(parents), m)
                    break
                else:
                    start = start + fit['fit_pct']
    return parents


class CromosGenerator:

    def gen(classif_values, genes_size, cromossomos_size):
        cromos = []

        for i in range(cromossomos_size):
            fit = {}
            idx = 0
            for v in classif_values[0]:
                vs = str(v).replace(",", ".")
                fit['acerto_' + str(float(vs))] = int(0)
                fit['qtde_' + str(float(v))] = int(classif_values[1][idx])
                fit['fit'] = 0
                fit['idx'] = i
                idx = idx + 1
            gens = []
            for g in range(genes_size):
                gens.insert(len(gens), -1 + 2 * random())
            c = crom.Cromossomo(i, gens, fit)
            cromos.insert(len(cromos), c)
        return cromos



    def new_gen(classif_values, genes, start_idx):
        cromos = []
        idx = start_idx #errado
        for i in range(len(genes)):
            fit = {}
            k = 0
            for v in classif_values[0]:
                vs = str(v).replace(",", ".")
                fit['acerto_' + str(float(vs))] = int(0)
                fit['qtde_' + str(float(v))] = int(classif_values[1][k])
                k = k + 1
            fit['fit'] = 0
            fit['idx'] = idx
            c = crom.Cromossomo(i, genes[i], fit)
            cromos.insert(len(cromos), c)
            idx = idx + 1
        return cromos


    def cross_over(bag_cromos):
        parents = sort_two_cr(bag_cromos)
        pct = random()
        part = int(len(bag_cromos[parents[0]].gens)*pct)
        cr1 = bag_cromos[parents[0]]
        cr2 = bag_cromos[parents[1]]
        g1p1 = cr1.gens[0:part]
        g1p2 = cr1.gens[part:]
        g2p1 = cr2.gens[0:part]
        g2p2 = cr2.gens[part:]
        g1c = g1p1 + g2p2
        cr1.gens = g1c
        g2c = g2p1 + g1p2
        cr2.gens = g2c


    def takeout_n_worst(bag_cromos, n):
        for i in range(n):
            mincr = min(bag_cromos, key=attrgetter('fitCR'))
            bag_cromos.remove(mincr)
        return bag_cromos


    def pickup_n_best(new_cromos, n):
        l = []
        for i in range(n):
            maxcr = max(new_cromos, key=attrgetter('fitCR'))
            new_cromos.remove(maxcr)
            l.insert(len(l), maxcr)
        return l



    def new_generation(cromo_bag, total, suns_size):
        parents = sort_two_cr(cromo_bag)

        new_gens = []
        rp = []

        while len(new_gens) != suns_size:     #for sun in range(suns_size):
            pct = random()
            part = int(len(cromo_bag[parents[0]].gens)*pct)
            if not part in rp:
                new_gens.insert(len(new_gens), cromo_bag[parents[0]].gens[0:part] + cromo_bag[parents[1]].gens[part:])
                rp.insert(len(rp), part)

        return new_gens

