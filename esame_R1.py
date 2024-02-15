from typing import Annotated


class ExamException(Exception):
  pass
class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name=name
        self.anno_min=1949
        self.anno_max=1960
        self.intestazione=""
        #self.riga=[]
        self.lista_completa = [] #inizializzo una lista vuota per salvare i valori
#---------
    def check_data(self,data):
        reverse=False
        data_filtrato=""
        anno=0
        mese=0
        if data!= '':
            if '-' not in data:#se non contiene -
                if data.isdigit()==True:#controllo che stringa abbia solo caratteri numerici
                    if self.anno_min <= int(data) <= self.anno_max:
                        anno=int(data)
                        mese=0
                        data_filtrato=str(anno)+"-0"
                    else:
                        pass#la riga contiene valore numerico non nell'intervallo
                else:
                    pass#la riga contiene lettere o caratteri speciali
            else:
                elem=data.split('-')
                if elem[0].isdigit()==True:#controllo che stringa abbia solo caratteri numerici
                    if self.anno_min <= int(elem[0]) <= self.anno_max:
                        anno=int(elem[0])
                    elif 1 <= int(elem[0]) <= 12:
                        mese=int(elem[0])
                        reverse=True
                else:
                    pass #non è un elemento numerico
                if elem[1].isdigit()==True :#controllo che stringa abbia solo caratteri numerici
                    if 1 <= int(elem[1]) <= 12:
                        mese=int(elem[1])
                    elif self.anno_min <= int(elem[1]) <= self.anno_max and reverse==True:
                        anno=int(elem[1])
                        reverse=False
                    else:
                        mese=0
                        anno=0
                else:
                    pass #non è un elemento numerico
                if mese==-90:
                    anno=0
                if(mese<=9):#font
                    data_filtrato=str(anno)+"-0"+str(mese)
                else:
                    data_filtrato=str(anno)+"-"+str(mese)
            #data=str(anno)+"-"+str(mese)
        else:
            pass#la riga contiene lettere o caratteri speciali
        return data_filtrato
    def check_pass(self,passeggeri):
        passeggeri_filtrato=0
        if passeggeri!= '':
            if passeggeri.isdigit()==True:#controllo che stringa abbia solo caratteri numerici
                if int(passeggeri)>0:
                    passeggeri_filtrato=int(passeggeri)
        else:
            pass#la riga contiene lettere o caratteri speciali
        return passeggeri_filtrato
    
    
#---------
    def get_data(self):
        riga=[]
        try:
            my_file = open(self.name, 'r') #apro e leggo il file, linea per linea
        except:
            raise ExamException('Errore apertura file non riuscita') #se non viene letto alzo un eccezione
        if(my_file.readline() == ''):        #controllo se il file è vuoto
            self.lista_completa=[]
            raise ExamException('File vuoto') #se il file è vuoto alzo un eccezione
        for line in my_file:
            elementi = line.strip().split(',') #faccio lo split di ogni riga sulla virgola
            if elementi[0].lower() != 'date': #se NON sto processando l’intestazione
                data = elementi[0] #salvo elemento 0 in variabile data
                if self.check_data(data) not in ['', '0-00', '0-0']:
                    data=self.check_data(data)
                    if self.check_pass(elementi[1])!=0:
                        passeggeri=self.check_pass(elementi[1]) #salvo elemento 1 in variabile passeggeri
                        riga=[data,passeggeri] #salvo elementi in lista riga
                        self.lista_completa.append(riga)
                    
                else:
                    continue
                
                
            else:
                self.intestazione=[elementi[0],elementi[1]]#salvo intestazione in lista intestazione
        my_file.close()
        return self.lista_completa

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
        media=somma_pass/n_mesi
        db[anno].append(media)#aggiungo media alla fine del dizionario #chiave: [t_passeggeri,n_mesi,media]

    #-----
    arr_anno_media=[]
    #creo un array bidimensionale per salvare anno e media
    for anno, (somma_pass, n_mesi, media) in db.items():
        arr_anno_media.append([anno, media])

    
    print(db.items())
    if first_year in db.keys() and last_year in db.keys():#controlla che i last_year e first_year siano all'interno del dizionario quindi all'interno della lista quindi preenti nel CSV file
        diff_dict = {}
        for i in range(len(arr_anno_media) - 1):
            anno1, media1 = arr_anno_media[i]
            anno2, media2 = arr_anno_media[i + 1]
            if first_year <= anno1 <= last_year and first_year <= anno2 <= last_year:#taglia valori fuori dall intervallo first_year-last_year
                key = f"{anno1}-{anno2}"#calcolo differenza tra medie e le salvo in un dizionario
                diff_dict[key] = round(media1 - media2, 3)

        print(diff_dict.items())
        return diff_dict
    else:
        raise ExamException(f"Errore, first o last year {first_year}, {last_year} presi come parametri dalla funzione non presenti nel CSV File")
        return {}

#main
time_series_file = CSVTimeSeriesFile('data.csv')
time_series = time_series_file.get_data()
print(time_series)
#print(time_series_file.dividi_mese_anno())
print("\n")
print(compute_increments(time_series, "1949", "1958"))