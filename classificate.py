import math

class Classificator:


    def euclides(list_val_result_croms, list_classif, classif_values):
        predict_list = []
        acerto_total = 0
        idx = 0

        #min list - predict
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

            if int(predict) == int(list_classif[idx]):
                acerto_total = acerto_total + 1
            idx = idx + 1
        return predict_list

