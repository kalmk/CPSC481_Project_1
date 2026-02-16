from probability4e import *

T, F = True, False

class Diagnostics:
    """ Use a Bayesian network to diagnose between three lung diseases """

    def __init__(self):
        # Create the Bayesian network
        self.bn = BayesNet([
            ('Asia', '', 0.01),
            ('Smoking', '', 0.5),
            ('TB', 'Asia', {(T,): 0.05, (F,): 0.01}),
            ('Cancer', 'Smoking', {T: 0.6, F: 0.3}),
            ('Bronchitis', 'Smoking', {T: 0.6, F: 0.3}),
            ('TBorC', 'TB Cancer', {(T, T): T, (T, F): T, (F, T): T, (F, F): F}),
            ('Xray', 'TBorC', {T: 0.99, F: 0.05}),
            ('Dyspnea', 'TBorC Bronchitis', {(T, T): 0.9, (T, F): 0.7, (F, T): 0.8, (F, F): 0.1})
        ])

    def diagnose(self, asia, smoking, xray, dyspnea):
        # Convert string inputs to Boolean/None
        def convert(val, positive):
            if val == "NA":
                return None
            elif val == positive:
                return T
            else:
                return F

        evidence = {}
        a = convert(asia, "Yes")
        if a is not None:
            evidence['Asia'] = a
        s = convert(smoking, "Yes")
        if s is not None:
            evidence['Smoking'] = s
        x = convert(xray, "Abnormal")
        if x is not None:
            evidence['Xray'] = x
        d = convert(dyspnea, "Present")
        if d is not None:
            evidence['Dyspnea'] = d

        # Compute probability for each disease
        diseases = ['TB', 'Cancer', 'Bronchitis']
        probs = {}
        for disease in diseases:
            Q = enumeration_ask(disease, evidence, self.bn)
            probs[disease] = Q[T]

        # Find disease with maximum probability
        max_disease = max(probs, key=probs.get)
        return [max_disease, probs[max_disease]]
