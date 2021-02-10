import os.path

alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def getParoleLista(parola):
    count=len(parola)
    flessivocabolario = []
    i=1
    #f = open(os.path.dirname(__file__) + '/Paroliere.txt', 'r')    #for Paroliere.txt
    f = open(os.path.dirname(__file__) + '/Parole_italiane.txt', 'r')    #for Parole_italiane.txt
    lista = f.read().split()
    l = len(lista)
    while i<l:
        if(len(lista[i]) == count or len(lista[i]) == count+1 or len(lista[i]) == count-1):
            flessivocabolario.append(lista[i])
        #i=i+2       #for Paroliere.txt
        i=i+1       #for Parole_italiane.txt
    return flessivocabolario

def generaflessi(parola):
    l = len(parola)
    flessigenerati = []
    parolamod = scomponi(parola)
    ##SOSTITUISCI UNA LETTERA##
    for j in range(l):
        for i in alfabeto:
            parolamod[j] = i
            flessigenerati.append(componi(parolamod))
            parolamod = scomponi(parola)
    ##AGGIUNGI UNA LETTERA##
    for j in range(l+1):
        for i in alfabeto:
            parolamod.insert(j,i)
            flessigenerati.append(componi(parolamod))
            parolamod = scomponi(parola)
    ##SOTTRAI UNA LETTERA##
    for j in range(l):
        del parolamod[j]
        flessigenerati.append(componi(parolamod))
        parolamod = scomponi(parola)

    return flessigenerati

def confronto(parola):
    flessivocabolario = getParoleLista(parola)
    flessigenerati = generaflessi(parola)
    result = []
    for i in flessivocabolario:
        for j in flessigenerati:
            #print(i + ' --> ' + j)
            if(i == j):
                result.append(i)
                break
    return result

def scomponi(parola):
    parolascomposta = []
    for i in range(len(parola)):
        parolascomposta.append(parola[i])
    return parolascomposta

def componi(parola):
    stringa = ""
    for i in range(len(parola)):
        stringa = stringa + parola[i]
    return stringa

if __name__ == '__main__':
    parola = input("Inserire una parola: ")
    
    print('Forse volevi scrivere una di queste parole:')
    for i in confronto(parola):
        print(i, end=', ')
    
    
    
    
