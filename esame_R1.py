from typing import Annotated


class ExamException(Exception):
  pass
class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name=name
        self.data=[]
        #self.riga=[]
        self.lista_completa = [] #inizializzo una lista vuota per salvare i valori
        self.lista_completa_conv = [] 
    def dividi_mese_anno(self,data):
        anno=[]
        mese=[]
        elem=data.split('-')
        anno=int(elem[0])
        mese=int(elem[1])

        if(len(elem[0])<=3 and len(elem[1])==4): #se anno e mese sono invertiti li giro
            anno=int(elem[1])
            mese=int(elem[0])
            #data=str(anno)+"-"+str(mese)
        return [anno, mese]
    def get_data(self):
        riga=[]
        anno_mese=[]
        my_file = open('data.csv', 'r') #apro e leggo il file, linea per linea
        for line in my_file:
            elementi = line.split(',') #faccio lo split di ogni riga sulla virgola
            if elementi[0].lower() != 'date': #se NON sto processando l’intestazione
                data = elementi[0] #salvo elemento 0 in variabile data
                anno_mese=self.dividi_mese_anno(data)
                passeggeri = int(elementi[1]) #salvo elemento 1 in variabile passeggeri
                riga=[data,passeggeri] #salvo elementi in lista riga
                self.lista_completa.append(riga)
                riga_conv=[anno_mese,passeggeri] #salvo elementi in lista riga
                self.lista_completa_conv.append(riga_conv) #aggiungo lista riga come elemento della lista lista_completa
            else:
                intestazione=[elementi[0],elementi[1]]#salvo intestazione in lista intestazione
        my_file.close()
        return self.lista_completa

    def media_passeggeri(self):
        media_passeggeri_anno = {}  #dizionario per salvare la media dei passeggeri per anno
        for elemento in self.lista_completa_conv:
            anno = elemento[0][0]  #memorizzo anno da lista
            passeggeri = elemento[1]  #memorizzo passeggeri da lista

            #se l'anno è già nel dizionario, aggiorna la somma e il conteggio
            if anno in media_passeggeri_anno:
                media_passeggeri_anno[anno][0] += passeggeri
                media_passeggeri_anno[anno][1] += 1#se numero mesi contati 12 top
            else:
                #se l'anno non è nel dizionario, crea una nuova voce
                media_passeggeri_anno[anno] = [passeggeri, 1]
        #calcola media anno e salvo in lista "passeggeri_anno"
        passeggeri_anno = []
        for anno, (somma_pass, n_pass) in media_passeggeri_anno.items(): #chiave: [passeggeri,tot_pass]
            if n_pass>0:
                media = somma_pass / n_pass
                passeggeri_anno.append([anno, media])
        return passeggeri_anno

        





time_series_file = CSVTimeSeriesFile('data.csv')
time_series = time_series_file.get_data()
#print(time_series_file.dividi_mese_anno())
print("\n")
print(time_series_file.media_passeggeri())





def compute_increments(time_series, first_year, last_year):
    first_year=int(first_year)
    last_year=int(last_year)
    
    db={}#creo dizionario per memorizzare passeggeri, n_mesi e media passeggeri
    for elemento in time_series:
        anno,mese=elemento[0].split("-")
        anno=int(anno)
        mese=int(mese)
        passeggeri=int(elemento[1])
        #se l'anno è già nel dizionario, aggiorna la somma e il conteggio
        if anno in db:
            db[anno][0] += passeggeri
            db[anno][1] += 1#se numero mesi contati 12 top
        else:
            #se l'anno non è nel dizionario, crea una nuova voce
            db[anno] = [passeggeri, 1]
        #calcola media anno e salvo in dizionario "db"
    for anno, (somma_pass, n_mesi) in db.items(): #chiave: [t_passeggeri,n_mesi]
        db[anno].append(somma_pass/n_mesi)#aggiungo media alla fine del dizionario #chiave: [t_passeggeri,n_mesi,media]
    #--------
    if first_year in db and last_year in db:
        dizionario={}
        for anno in range(first_year, last_year):
            if anno in db and anno + 1 in db:
                dizionario[f"{anno}-{anno+1}"] = db[anno][2] - db[anno + 1][2]
        return dizionario
    else:
        raise ExamException("first o last year presi come parametri dalla funzione non presenti nel CSV File")
        return {}
print(compute_increments(time_series, "2010", "2014"))