
####### Problem 3 #######

test_cases = [('book', 'back'), ('kookaburra', 'kookybird'), ('elephant', 'relevant'), ('AAAGAATTCA', 'AAATCA')]
alignments = [('book', 'back'), ('kookaburra', 'kookybird-'), ('relev-ant','-elephant'), ('AAAGAATTCA', 'AAA---T-CA')]
def MED(S, T):
    # TO DO - modify to account for insertions, deletions and substitutions
    if (S == ""):
        return (len(T))
    elif (T == ""):
        return (len(S))
    else:
        if (S[0] == T[0]):
            return (MED(S[1:], T[1:]))
        else:
            return (1 + min(MED(S, T[1:]), MED(S[1:], T), MED(S[1:], T[1:])))

def fast_MED(S, T, MED={}):
    if (S, T) in MED:
        return MED[(S, T)]
    if (S == ""):
        return len(T)
    elif (T == ""):
        return len(S)
    else:
        if (S[0] == T[0]):
            result = fast_MED(S[1:], T[1:], MED)
        else:
            result = 1 + min(fast_MED(S, T[1:], MED), fast_MED(S[1:], T, MED))
        MED[(S, T)] = result
        return result


def fast_align_MED(S, T, MED={}, align_S="", align_T=""):
    if (S, T) in MED:
        return (MED[(S, T)], align_S, align_T)
    elif (S == ""):
        align_S += "-" * len(T)
        align_T += T
        result = len(T)
    elif (T == ""):
        align_S += S
        align_T += "-" * len(S)
        result = len(S)
    else:
        if (S[0] == T[0]):
            result, align_S, align_T = fast_align_MED(S[1:], T[1:], MED, align_S + S[0], align_T + T[0])
        else:
            insertion, align_S1, align_T1 = fast_align_MED(S, T[1:], MED, align_S + "-", align_T + T[0])
            delete, align_S2, align_T2 = fast_align_MED(S[1:], T, MED, align_S + S[0], align_T + "-")
            substitute, align_S3, align_T3 = fast_align_MED(S[1:], T[1:], MED, align_S + S[0], align_T + T[0])
            if insertion <= delete and insertion <= substitute:
                result, align_S, align_T = insertion, align_S1, align_T1
            elif delete <= insertion and delete <= substitute:
                result, align_S, align_T = delete, align_S2, align_T2
            else:
                result, align_S, align_T = substitute, align_S3, align_T3
    MED[(S, T)] = result
    return (result, align_S, align_T)


def test_MED():
    for S, T in test_cases:
        assert fast_MED(S, T) == MED(S, T)


def test_align():
    for i in range(len(test_cases)):
        S, T = test_cases[i]
        align_S, align_T = fast_align_MED(S, T)
        assert (align_S == alignments[i][0] and align_T == alignments[i][1])


s1 = 'kitten'
s2 = 'sitting'
print(MED(s1, s2))
print(fast_MED(s1, s2))
print(fast_align_MED(s1, s2))
