import classificate as classif
import cromossomo as crms


class Mult:

    def mult(dfds, bag_cromos, idxattrs, classif_values, list_classif):

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

            list_predict = classif.Classificator.euclides(list_val_result_croms,list_classif, classif_values[0])
            df['cr-' + str(idxcroms)] = list_predict

            idk = 0
            acerto_total = 0
            for v in list_predict:
                if int(list_predict[idk]) == int(list_classif[idk]):
                    vs = str(v).replace(",", ".")
                    cr.fit['acerto_' + str(float(vs))] = int(cr.fit['acerto_' + str(float(v))] + 1)
                    acerto_total = acerto_total + 1
                idk=idk+1

            cr.fit['acerto_total'] = acerto_total

        for cr in bag_cromos:
            for v in classif_values[0]:
                vs = str(v).replace(",", ".")
                cr.fit['pct_' + str(float(vs))] = cr.fit['acerto_' + str(float(vs))] / cr.fit['qtde_' + str(float(v))]
                cr.fit['fit'] = cr.fit['fit']  + cr.fit['pct_' + str(float(vs))]
                cr.fitCR = cr.fitCR  + cr.fit['pct_' + str(float(vs))]

        return df

