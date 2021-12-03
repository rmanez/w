
class Cromossomo:

    def __init__(self, idx, gens, fit):
        self.idx = idx
        self.gens = gens
        self.fit = fit
        self.fitCR = 0


    def print(self, total_rows):
        print('============================================================================================')
        if self.fit['acerto_total'] >= int(total_rows * 0.95):
            print('        >=95  ', self.fit['acerto_total'], self.fit['acerto_total'] * 100 / total_rows)
            print(self.fit)
            #print(self.fitCR)
            print(self.gens)
        else:
            if self.fit['acerto_total'] >= int(total_rows * 0.75):
                print('        >=75  ', self.fit['acerto_total'], self.fit['acerto_total'] * 100 / total_rows)
                print(self.fit)
                #print(self.fitCR)
                print(self.gens)
        print('============================================================================================')

