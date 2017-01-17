
def getfile(mdpath):
    with open(mdpath, 'rb') as f:
        fdata = f.read().decode('utf-8', 'ignore')
    f.close()

    return fdata
