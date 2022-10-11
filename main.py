import mysql.connector
import math
import random
import time

yhteys = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='lentopeli',
    user='root',
    password='MiksiRikoit56Lamppua?',
    autocommit=True
)

def nimea_pelaaja(nimi: str):
    sql = f'INSERT INTO peli(name) VALUES ("{nimi}");'
    kursori = yhteys.cursor()
    kursori.execute(sql)

def paivita_kakka():
    global kakatut_kakat, pelaajan_nimi
    sql = f'UPDATE peli SET kakatut_kentat = {kakatut_kakat} WHERE name = "{pelaajan_nimi}";'
    kursori = yhteys.cursor()
    kursori.execute(sql)

def paivita_lahjat():
    global lasten_saamat_lahjat, pelaajan_nimi

    sql = f'UPDATE peli SET lahjat_annettu = {lasten_saamat_lahjat} WHERE name = "{pelaajan_nimi}";'
    kursori = yhteys.cursor()
    kursori.execute(sql)

def paivita_highscore():
    global pelaajan_nimi, lasten_saamat_lahjat

    tahanastinen = f'SELECT highscore FROM peli WHERE name = "{pelaajan_nimi}";'
    kursori = yhteys.cursor(buffered=True)
    kursori.execute(tahanastinen)
    paras_tahanasti = kursori.fetchone()[0]
    if lasten_saamat_lahjat > paras_tahanasti:
        paivita_hs = f'UPDATE peli SET highscore = {lasten_saamat_lahjat} WHERE name = "{pelaajan_nimi}";'
        kursori2 = yhteys.cursor(buffered=True)
        kursori2.execute(paivita_hs)

def tulosta_highscore():
    sql = f'SELECT name, lahjat_annettu FROM peli WHERE lahjat_annettu = (SELECT MAX(lahjat_annettu) FROM peli);'
    kursori = yhteys.cursor()
    kursori.execute(sql)
    maximi = kursori.fetchall()
    return maximi

def luo_lentokenttalista():
    sql = 'SELECT name FROM airport;'
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()

    # tehdään lista, jossa on vain lentokenttien nimet niin että ne ei ole osana tuplea (ei tule sulkuja ympärille)
    lentokenttalista = []
    for kentta in tulos:
        lentokenttalista.append(kentta[0])

    return lentokenttalista

def ottaa_aikaa():
    global aloita_ajastin
    return time.time() - aloita_ajastin

# Miten randomisoidaan lentokoneiden sijainti lentokentilla
def lentokoneet_kentalla():
    global kaikki_lentokentat
    # jotta demonstroitaessa ei tarvii hakata pelii läpi, iso prosenttiosuus
    prosenttiosuus = random.randint(50, 67)
    onko_kone = []
    kentat_konemaarat = {}
    for i in range(prosenttiosuus):
        onko_kone.append(1)
    for i in range(100 - prosenttiosuus):
        onko_kone.append(0)
    random.shuffle(onko_kone)

    # lisätään sanakirjaan arvot listoilta kaikki_lentokentat ja konemaarat_kentilla
    for i in range(len(kaikki_lentokentat)):
        kentat_konemaarat[kaikki_lentokentat[i]] = onko_kone[i]

    return kentat_konemaarat

def randomisoi_viisi_kenttaa(sanakirja: dict):
    lentokentat_koneet = sanakirja
    vaihtoehdot = []

    for i in range(5):
        lentokentta = random.choice(list(lentokentat_koneet.items()))
        vain_nimi = lentokentta[0]
        vaihtoehdot.append(vain_nimi)

    for i in range(5):
        print(f"{chr(i+97)}. {vaihtoehdot[i]}")
    print("\n")

    return vaihtoehdot

# lähtöarvot
lahjamaara = 0
kakatut_kakat = 0
pukkialussa = ""
kakatut_lentokentat = []
pisteet = 0

# tehdään lista kaikkien lentokenttien nimistä kutsumalla luo_lentokenttalista()-funktiota
kaikki_lentokentat = luo_lentokenttalista()
lentokonesanakirja = lentokoneet_kentalla()

# Vaihe 1 alkaa
lopeta_ajastin = 30  # näin monta sekuntia ajastin tulee olemaan päällä

from termcolor import colored

ekan_vaiheen_intro = colored("Olet porollaan lentävä pukki.\nTänään on 23. joulukuuta, ja menet mielenosoitukseen lentokoneilla lentämistä vastaan!\nPorosi tehtävä on kakata lentokoneiden päälle. Lennätte kuitenkin niin korkealla, ettette näe, millä lentokentillä on lentokoneita. Toivotaan parasta!\nJokaisesta koneesta, jonka päälle porosi kakkaa onnistuneesti, saat yhden lahjan, joita myöhemmin jakaa lapsille.\n", "red")
print(ekan_vaiheen_intro)
pelaajan_nimi = input("Mikä on nimesi? ")
if pelaajan_nimi == "":
    print("Ei sitten.")
else:
    nimea_pelaaja(pelaajan_nimi)
    varoitus = colored("\nAikaa on 30 sekuntia! Yritä osua ainakin 10 koneeseen.\n", "red")
    print(varoitus)

# peli alkaa
    aloita_peli = input('Paina Enter aloittaaksesi.')


    if aloita_peli == "":
        aloita_ajastin = time.time()
        while ottaa_aikaa() < lopeta_ajastin:
            # tässä tapahtuu vaihe 1
            vaihtoehdot = randomisoi_viisi_kenttaa(lentokonesanakirja)
            lentokentta = input('Anna lentokentän kirjain (a-e), jonne haluat kakata: ')
            for i in range(5):
                if lentokentta.casefold() == chr(i + 97):
                    kakatut_kakat += 1
                    paivita_kakka()
                    if lentokonesanakirja[vaihtoehdot[i]] == 1:
                        pisteet += 1
                        kakka_success = colored("\nOsuma! Hahaa!", "green")
                        print(kakka_success)
                    else:
                        kakka_fail = colored("\nEt osunut koneeseen :(", "red")
                        print(kakka_fail)
                    print(f"Olet kakannut {kakatut_kakat} kertaa, ja osunut lentokoneeseen {pisteet} kertaa.\n")

    # kakkosvaiheen aloitus
        lahjamaara = pisteet

        luo_lentokenttalista()
        uusi_lista = luo_lentokenttalista()
        luovutetut_lahjat = 0
        lasten_saamat_lahjat = 0

        if pisteet >= 10:
            toka_vaihe_intro = colored('\nHienosti kakattu. Nyt on 24. joulukuuta, ja siispä on tullut aika pelin toisen vaiheen, jossa tiputat lahjoja lapsille.\n', 'green')
            print(toka_vaihe_intro)
            time.sleep(5)
            lentokonesanakirja = lentokoneet_kentalla()

            while lahjamaara > 0:
                vaihtoehdot = randomisoi_viisi_kenttaa(lentokonesanakirja)
                lapset = input('Anna lentokentän kirjain (a-e), jonne haluat jakaa lahjan: ')
                for i in range(5):
                    if lapset.casefold() == chr(i + 97):
                        luovutetut_lahjat += 1
                        if lentokonesanakirja[vaihtoehdot[i]] == 1:
                            lasten_saamat_lahjat += 1
                            paivita_lahjat()
                            lapsi_success = colored("\nLahja jaettu! Teit juuri lapsen onnelliseksi <3", "green")
                            print(lapsi_success)
                            lahjamaara -= 1
                        else:
                            lapsi_fail = colored("\nKentällä ei ollut lasta! Tuhlasit lahjan >:(", "red")
                            print(lapsi_fail)
                            lahjamaara -= 1
                        print(f"Olet jakanut {luovutetut_lahjat} lahjaa. Lahjoja jäljellä: {pisteet - luovutetut_lahjat}\n")
            pelastit_joulun = colored(f'Sait jaettua lahjoja {lasten_saamat_lahjat} lapselle. Pelastit heidän joulunsa!', 'green')
            print(pelastit_joulun)
            paivita_highscore()
            paras = tulosta_highscore()
            print(f'Paras ennätys on {paras[0][1]} ja sen on saanut pelaaja "{paras[0][0]}".')

        else:
            pilasit_joulun = colored(f"Sinun olisi pitänyt saada yli 10 lahjaa, mutta saitkin vain {pisteet}. Pilasit joulun. :(", "red")
            print(pilasit_joulun)

    else:
        print("Tyhmä")
