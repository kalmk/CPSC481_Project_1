from probability4e import *
T, F = True, False


class Diagnostics:

    def __init__(self):

        self.bn = BayesNet([

            ('VisitAsia', '', 0.01),
            ('Smoking', '', 0.5),

            ('TB', 'VisitAsia', {T: 0.05, F: 0.01}),
            ('Cancer', 'Smoking', {T: 0.1, F: 0.01}),
            ('Bronchitis', 'Smoking', {T: 0.6, F: 0.3}),

            ('TBorCancer', 'TB Cancer',
             {
                 (T, T): 1.0,
                 (T, F): 1.0,
                 (F, T): 1.0,
                 (F, F): 0.0
             }),

            ('Xray', 'TBorCancer', {T: 0.99, F: 0.05}),

            ('Dyspnea', 'TBorCancer Bronchitis',
             {
                 (T, T): 0.9,
                 (T, F): 0.7,
                 (F, T): 0.8,
                 (F, F): 0.1
             })
        ])

    def diagnose(self, asia, smoking, xray, dyspnea):

        evidence = {}

        if asia != "NA":
            evidence['VisitAsia'] = (asia == "Yes")

        if smoking != "NA":
            evidence['Smoking'] = (smoking == "Yes")

        if xray != "NA":
            evidence['Xray'] = (xray == "Abnormal")

        if dyspnea != "NA":
            evidence['Dyspnea'] = (dyspnea == "Present")

        tb = enumeration_ask('TB', evidence, self.bn)[T]
        cancer = enumeration_ask('Cancer', evidence, self.bn)[T]
        bronchitis = enumeration_ask('Bronchitis', evidence, self.bn)[T]

        probs = {
            "tb": tb,
            "cancer": cancer,
            "bronchitis": bronchitis
        }

        disease = max(probs, key=probs.get)
        probability = round(probs[disease], 3)

        return [disease, probability]
