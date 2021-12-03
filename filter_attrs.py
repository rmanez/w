from random import random

class FilterAttrs:

    def filter(dfds):
        l = dfds.columns.values.tolist()
        attrs = []
        for i in range(len(l)):
            if ('IDN' != l[i]) and ('CLASSIF_TARGET' != l[i]):
                attrs.insert(len(attrs), i)
        return attrs

