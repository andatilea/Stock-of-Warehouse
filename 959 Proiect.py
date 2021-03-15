"""
    Avem aplicatia care tine stocul unui depozit (Cap 5-6). Efectuati urmatoarele imbunatatiri:
	
	Este necesar rezolvati minim 5 din punctele de mai jos:

1. Implementati o solutie care sa returneze o proiectie grafica a intrarilor si iesirilor intr-o
anumita perioada, pentru un anumit produs;	--pygal--

2. Implementati o solutie care sa va avertizeze automat cand stocul unui produs este mai mic decat o 
limita minima, predefinita per produs. Limita sa poata fi variabila (per produs). Preferabil sa 
transmita automat un email de avertizare;

3. Creati o metoda cu ajutorul careia sa puteti transmite prin email diferite informatii(
de exemplu fisa produsului) ; 	--SMTP--

4. Utilizati Regex pentru a cauta :
    - un produs introdus de utilizator;
    - o tranzactie cu o anumita valoare introdusa de utilizator;	--re--

5. Creati o baza de date care sa cuprinda urmatoarele tabele:	--pymysql--  sau --sqlite3--
    Categoria
        - idc INT NOT NULL AUTO_INCREMENT PRIMARY KEY (integer in loc de int in sqlite3)
        - denc VARCHAR(255) (text in loc de varchar in sqlite3)
    Produs
        - idp INT NOT NULL AUTO_INCREMENT PRIMARY KEY
        - idc INT NOT NULL
        - denp VARCHAR(255)
        - pret DECIMAL(8,2) DEFAULT 0 (real in loc de decimal)
        # FOREIGN KEY (idc) REFERENCES Categoria.idc ON UPDATE CASCADE ON DELETE RESTRICT
    Operatiuni
        - ido INT NOT NULL AUTO_INCREMENT PRIMARY KEY
        - idp INT NOT NULL
        - cant DECIMAL(10,3) DEFAULT 0
        - data DATE

6. Imlementati o solutie cu ajutorul careia sa populati baza de date cu informatiile adecvate.

7. Creati cateva view-uri cuprinzand rapoarte standard pe baza informatiilor din baza de date. --pentru avansati--

8. Completati aplicatia astfel incat sa permita introducerea pretului la fiecare intrare si iesire.
Pretul de iesire va fi pretul mediu ponderat (la fiecare tranzactie de intrare se va face o medie intre
pretul produselor din stoc si al celor intrate ceea ce va deveni noul pret al produselor stocate).
Pretul de iesire va fi pretul din acel moment;  

9. Creati doua metode noi, diferite de cele facute la clasa, testatile si asigurativa ca functioneaza cu succes;


"""  #
import pygal
import smtplib
import re
from datetime import datetime
from prettytable import PrettyTable


class Stoc:
    lista_prod = []

    def __init__(self, denp, categ, um='kg', sold=0):
        self.denp = denp
        self.categ = categ
        self.um = um
        self.sold = sold
        self.dict_op = {}
        self.lista_prod.append(denp)

    def genereaza_cheia(self):
        if self.dict_op:
            c = max(self.dict_op.keys()) + 1
        else:
            c = 1
        return c

    def intrari(self, cant, data=str(datetime.now().strftime('%Y%m%d'))):
        cheie = self.genereaza_cheia()
        self.dict_op[cheie] = [data, cant, 0]
        self.sold += cant

    def iesiri(self, cant, data=str(datetime.now().strftime('%Y%m%d'))):
        cheie = self.genereaza_cheia()
        self.dict_op[cheie] = [data, 0, cant]
        self.sold -= cant

    def fisap(self):
        print('Fisa produsului {0}, {1}'.format(self.denp, self.um))
        listeaza = PrettyTable()
        listeaza.field_names = ['Nrc', 'Data', 'Intrare', 'Iesire']
        for k, v in self.dict_op.items():
            listeaza.add_row([k, v[0], v[1], v[2]])
        listeaza.add_row(['------', '----------', '---------', '--------'])
        listeaza.add_row(['Sold', 'final', self.denp, self.sold])
        print(listeaza)

    def produse(self):
        for i in self.lista_prod:
            print(i)


    """
    1. Implementati o solutie care sa returneze o proiectie grafica a intrarilor si iesirilor intr-o
        anumita perioada, pentru un anumit produs;	--pygal--
    """

    def cerinta1(self):
        bar_chart = pygal.Bar(x_title='Perioada de timp', y_title='Cantitate', title_font_size=23)
        bar_chart.title = 'Proiectia grafica a produsului: ' + self.denp
        date = []
        intrari = []
        iesiri = []
        for k, v in self.dict_op.items():
            date.append(v[0])
            intrari.append(v[1])
            iesiri.append(v[2])
        bar_chart.x_labels = date
        bar_chart.add('Intrari', intrari)
        bar_chart.add('Iesiri', iesiri)
        bar_chart.render()
        bar_chart.render_to_file('proiectieGrafica.svg')  # salvare fisier grafic

    """
    2. Implementati o solutie care sa va avertizeze automat cand stocul unui produs este mai mic decat o 
    limita minima, predefinita per produs (10). Limita sa poata fi variabila (per produs). Preferabil sa 
    transmita automat un email de avertizare.
    """

    def cerinta2(self, limita=10):
        self.limita = limita
        if self.sold < limita:
            expeditor = 'andaptilea@gmail.com'
            destinatar = 'andaptilea@gmail.com'
            username = 'andaptilea@gmail.com'
            parola = 'pythonproj3023'
            mesaj = f"""From: Anda <andaptilea@gmail.com>
                       To: Anda <andaptilea@gmail.com>\n
                       Subject: Avertizare: \n
                       Stocul produsului: {self.denp}, este mai mic decat limita minima (10) predefinita!"""
            try:
                smtp_ob = smtplib.SMTP('smtp.gmail.com', 587)
                smtp_ob.starttls()
                smtp_ob.login(username, parola)
                smtp_ob.sendmail(expeditor, destinatar, mesaj)
                print('Mesaj expediat cu succes!')
            except:
                print('Mesajul nu a putut fi expediat!')
            finally:
                smtp_ob.close()
        else:
            print(f'Stocul produsului: {self.denp}, este suficient!')

    """
       3. Creati o metoda cu ajutorul careia sa puteti transmite prin email diferite informatii(
       de exemplu fisa produsului);
    """

    def cerinta3(self):

        expeditor = 'andaptilea@gmail.com'
        destinatar = 'andaptilea@gmail.com'
        username = 'andaptilea@gmail.com'
        parola = 'pythonproj3023'
        mesaj = f"""From: Anda <andaptilea@gmail.com>
                   To: Anda <andaptilea@gmail.com>\n
                   Subject: Detalii produs curent: \n
                   Denumire produs: {self.denp} \n
                   Categorie produs: {self.categ} \n 
                   Sold final: {self.sold}\n
                   Dictionar operatii (data - intrari - iesiri): {self.dict_op.values()}"""
        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.starttls()
            smtpObj.login(username, parola)
            smtpObj.sendmail(expeditor, destinatar, mesaj)
            print('Mesaj expediat cu succes!')
        except:
            print('Mesajul nu a putut fi expediat!')
        finally:
            smtpObj.close()

    """
           4. Utilizati Regex pentru a cauta :
                - un produs introdus de utilizator;
                - o tranzactie cu o anumita valoare introdusa de utilizator;	--re--
    """

    def cerinta4(self):

        str1 = ""
        for elem in self.lista_prod:
            str1 += elem
        print(re.search(input("Introduceti produsul cautat: "), str1))

        intrari = []
        iesiri = []
        for k, v in self.dict_op.items():
            intrari.append(str(v[1]))
            iesiri.append(str(v[2]))
        s = ''.join(intrari)
        s_final = s.join(iesiri)
        print(re.search(input("Introduceti tranzactia cautata: "), s_final))

    """
        9. Creati doua metode noi, diferite de cele facute la clasa, 
           testatile si asigurativa ca functioneaza cu succes;
           
           METODA 1: Metoda ne va ajuta sa verificam daca in spatiul de depozitare (maximul ales: 10000 kg) 
                     mai este loc sa adaugam o noua intrare pentru produsul curent. 
                     Daca noi intrari pot fi adaugate, vom primi o confirmare pe email.
                     Daca nu, suntem anuntati printr-o alerta tot pe email: Spatiul maxim de depozitare a fost atins.
    """

    def depozitare(self, maxim=10000):
        self.maxim = maxim
        intrari = 0
        for k, v in self.dict_op.items():
            intrari += v[1]
            intrari -= v[2]
        if intrari < maxim:
            expeditor = 'andaptilea@gmail.com'
            destinatar = 'andaptilea@gmail.com'
            username = 'andaptilea@gmail.com'
            parola = 'pythonproj3023'
            mesaj = f"""From: Anda <andaptilea@gmail.com>
                                   To: Anda <andaptilea@gmail.com>\n
                                   Subject: Confirmare spatiu de depozitare: \n
                                   Stocul produsului: {self.denp}, este : {self.sold}. 
                                   Mai putem adauga produse pana la maximul de 10000."""
            try:
                smtp_ob = smtplib.SMTP('smtp.gmail.com', 587)
                smtp_ob.starttls()
                smtp_ob.login(username, parola)
                smtp_ob.sendmail(expeditor, destinatar, mesaj)
                print('Mesaj expediat cu succes!')
            except:
                print('Mesajul nu a putut fi expediat!')
            finally:
                smtp_ob.close()
        else:
            expeditor = 'andaptilea@gmail.com'
            destinatar = 'andaptilea@gmail.com'
            username = 'andaptilea@gmail.com'
            parola = 'pythonproj3023'
            mesaj = f"""From: Anda <andaptilea@gmail.com>
                                   To: Anda <andaptilea@gmail.com>\n
                                   Subject: Avertizare!
                                   Spatiul de depozitare al produsului: {self.denp}, este plin! \n'
                                   Nu mai pot fi adaugate alte intrari!"""
            try:
                smtp_ob = smtplib.SMTP('smtp.gmail.com', 587)
                smtp_ob.starttls()
                smtp_ob.login(username, parola)
                smtp_ob.sendmail(expeditor, destinatar, mesaj)
                print('Mesaj expediat cu succes!')
            except:
                print('Mesajul nu a putut fi expediat!')
            finally:
                smtp_ob.close()

    """"
            METODA 2: Metoda ne va ajuta sa decidem care din produsele aflate in stoc trebuie inlocuite.
                      In cadrul fructelor si legumelor, acestea vor expira odata cu trecerea in anul 2021. 
                      Astfel, orice tranzactie a categoriilor fruct/legume, aflata inca in anul 2020, 
                      va transmite un mail sugestiv, anuntand utilizatorul ca produsul este stricat.
                      Restul produselor din alte categorii, vor fi in continuare valabile atat in 2020 cat si in 2021.
    """

    def valabilitate(self):

        date = []
        for k, v in self.dict_op.items():
            date.append(v[0])
        if self.categ == 'fruct' or self.categ == 'legume':
            for i in range(0, len(date)):
                if date[i][0:4] == '2020':
                    expeditor = 'andaptilea@gmail.com'
                    destinatar = 'andaptilea@gmail.com'
                    username = 'andaptilea@gmail.com'
                    parola = 'pythonproj3023'
                    mesaj = f"""From: Anda <andaptilea@gmail.com>
                                                       To: Anda <andaptilea@gmail.com>\n
                                                       Subject: Advertisment - produs stricat: \n
                                                       Produsul curent: {self.denp}, nu mai este valabil."""
                    try:
                        smtp_ob = smtplib.SMTP('smtp.gmail.com', 587)
                        smtp_ob.starttls()
                        smtp_ob.login(username, parola)
                        smtp_ob.sendmail(expeditor, destinatar, mesaj)
                        print('Mesaj expediat cu succes!')
                    except:
                        print('Mesajul nu a putut fi expediat!')
                    finally:
                        smtp_ob.close()
                else:
                    print("Produsul este inca valabil.")
        else:
            print("Produsul este inca valabil.")




mere = Stoc('mere', 'fruct')
mere.__dict__
mere.intrari(1000, '20200925')

mere.valabilitate()

tele = Stoc('televizor', 'electrocasnice')
tele.intrari(100, '20200925')
tele.valabilitate()

mere.intrari(2000)
mere.iesiri(1368)
mere.intrari(10000)
mere.depozitare()
mere.fisap()


pere = Stoc('pere', 'fruct')
pere.intrari(10, '20200925')
pere.valabilitate()

pere.iesiri(2, '20201001')
pere.intrari(34)
pere.iesiri(13)
pere.iesiri(20)
pere.fisap()

mere.cerinta1()

pere.cerinta2()
mere.cerinta2()

mere.cerinta3()
mere.cerinta4()