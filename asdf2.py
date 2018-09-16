
def split(img):
    def getcol(x):
        return [0 if p >= 200 else 1 for p in i.crop((x, 0, x+1, i.height)).getdata()]

    
