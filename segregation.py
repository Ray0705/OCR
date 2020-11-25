from itertools import islice

def creating_dict(sentences):
    """Creating dictionary so that the start of the auditor report and start of annexure is stored in start_line and
    for last line we use stop_line dictionary for both"""
    start_line = {}
    stop_line = {}
    for i,sent in enumerate(sentences):
        if sent.split('\n')[0] == "INDEPENDENT AUDITORS’ REPORT":
            start_line[i] = sent.split('\n')[0]
        for position, m in enumerate(sent.split('\n')[0].split()):
            if m == "Membership":
                stop_line[i] = m
            elif m == "Annexure":
                start_line[i] = m
    return start_line,stop_line



# for the getting the nth key
def nth_key(dct, n):
    it = iter(dct)
    next(islice(it, n, n), None)
    return next(it)



# for auditor report
def get_start_and_endAR(dict1,dict2):
    start = next(iter(dict1))
    stop = next(iter(dict2))
    return start,stop


# for annexure
def get_start_and_endAnn(dict1,dict2,stop):
    cal = []
    startann = 0
    for i in dict1:
        cal.append(i-stop)
    for i, j in enumerate(cal):
        if j >0:
            startann = i
            break
    start_ann = nth_key(dict1,startann)
    stop_ann = nth_key(dict2,1)
    return start_ann,stop_ann