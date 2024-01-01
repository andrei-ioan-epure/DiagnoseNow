from itertools import product


class DempsterShafer:

    def add_missing_rules(self, ipoteze, reguli):
        for simptom in reguli:
            reguli_existente = []
            sum_reguli = 0
            for regula in reguli[simptom]:
                reguli_existente = [*reguli_existente, *list(regula[0])]
                sum_reguli = sum_reguli + regula[1]

            print(reguli_existente)
            reguli[simptom].append((frozenset(ipoteze), 1 - sum_reguli))

    def intersect(self,reguli):
        simptoame = []
        for simptom in reguli:
            smp = []
            for regula in reguli[simptom]:
                smp.append((list(regula[0]), regula[1]))
            simptoame.append(smp)

        intersectia = product(*simptoame)
        # print(list(intersectia))
        to_return = []
        for members in list(intersectia):
            p = members[0][1]
            intersect = frozenset(members[0][0])
            for i in range(1, len(members)):
                p = p * members[i][1]
                intersect = intersect.intersection(frozenset(members[i][0]))

            # print(f'{members[0], members[1]} -> {intersect} {p}')
            to_return.append((intersect, p))

        return to_return

    def denominator(self,intersect):
        denominator = 0
        for element in intersect:
            if len(element[0]) == 0:
                denominator += element[1]
        return 1 - denominator

    def BBA(self,intersect, numitor):
        bba = {}

        for element in intersect:
            if len(element[0]) == 0:
                continue
            if bba.keys().__contains__(element[0]):
                bba[element[0]] += element[1]
            else:
                bba[element[0]] = element[1]

        for key, value in bba.items():
            bba[key] = value / numitor
        return bba

    def belief(self,intersect):
        elemente_calculate = []
        bel = {}

        for a_set, a_value in intersect.items():
            if a_set in elemente_calculate:
                continue
            bel[a_set] = a_value

            for b_set, b_value in intersect.items():
                if a_set == b_set:
                    continue
                if b_set.issubset(a_set):
                    bel[a_set] += b_value

            elemente_calculate.append(a_set)

        return bel

    def plauzibilitatea(self,bel):
        Pl = {}
        for a_set, a_value in bel.items():
            neg_set = frozenset()
            neg_value = 0
            for b_set, b_value in bel.items():
                if a_set == b_set:
                    continue
                if a_set.intersection(b_set) == frozenset():
                    if len(neg_set) < len(b_set):
                        neg_set = b_set
                        neg_value = b_value
            # print(f'Negativ pentru {a_set} e {neg_set}')
            Pl[a_set] = 1 - neg_value
        return Pl
