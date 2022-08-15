import tkinter as tk
from collections import namedtuple

Punkt = namedtuple('Punkt', 'x, y')
LAENGE_SCHLANGE = 2
START_POS_X = 155
START_POS_Y = 155

class Spiel(tk.Frame):

    def __init__(self, master, breite, hoehe) :

        super(Spiel, self).__init__(master)

        self.master = master
        self.breite = breite
        self.hoehe = hoehe
        self.neues_spiel = True
        self.schlange = []
        self.schlange_koord = []
        self.kopf_img = tk.PhotoImage(file='images/kopf.png')
        self.koerper_img = tk.PhotoImage(file='images/koerper.png')
        self.futter_img = tk.PhotoImage(file='images/futter.png')

        # Spielfeld
        self.canvas = tk.Canvas(self.master, bg='black', bd=5, relief='sunken')
        self.canvas.place(x=15, y=10, height= self.hoehe, width=self.breite)

        # weitere Atribute

        self.kopf = tk.Label(self.canvas, bg='black', image=self.kopf_img)
        self.futter = tk.Label(self.canvas, bg='black', image=self.futter_img)
        self.x_richtung = 1
        self.y_richtung = 0
        self.punkte = 0
        self.starten = False

        # Rahmen der Steuerung
        self.frame_strg = tk.Frame(self.master, bg='grey')
        self.frame_strg.place(x=20, y=(self.hoehe+10), height=95, width=(self.breite-10))

        # def für die Beschriftungs-for
        self.label_besch_links = ['Punkte:', 'Rekord:', 'Spielzeit:']
        self.i = 0

        for beschriftung in self.label_besch_links:

            # Label links
            self.label_l = tk.Label(self.frame_strg, bg ='white', text=beschriftung, font=('arial', 12, 'normal'), anchor='w')
            self.label_l.place(x=5, y=(self.i*30+5), width=80, height=25)

            # Label mitte mit infos
            self.label_m = tk.Label(self.frame_strg, bg ='white', text='0', font=('arial', 12, 'normal'), relief='sunken')
            self.label_m.place(x=95, y=(self.i*30+5), width=50, height=25)

            self.i= self.i +1

        # Label Geschwingigkeit
        self.label_r = tk.Label(self.frame_strg, bg='white', text='Geschwindigkeit:', font=('arial', 12, 'normal'))
        self.label_r.place(x=170, y=5, width=150, height=25)

        # Scale
        self.geschwindigkeit = tk.IntVar(None, 200)
        self.geschwindigkeit_regler = tk.Scale(self.frame_strg, orient='horizontal', variable=self.geschwindigkeit, from_=10, to=450, sliderlength=10, tickinterval=100, bg='white', troughcolor='red', resolution=10, width=10, relief='sunken')
        self.geschwindigkeit_regler.place(x=170, y=35, width=150, height=55)

        # Buttons
        self.button_start = tk.Button(self.frame_strg, text="START", font=('arial', 12, 'bold'), bg='grey', relief='raised', command=self.starte_spiel)
        self.button_start.place(x=345, y=35, width=75, height=25)

        self.button_ende = tk.Button(self.frame_strg, text="ENDE", font=('arial', 12, 'bold'), bg='grey', relief='raised', command=self.master.destroy)
        self.button_ende.place(x=345, y=65, width=75, height=25)

    def erzeuge_schlange(self):

        if (self.neues_spiel == True):
            self.schlange_koord.append(Punkt(START_POS_X, START_POS_Y))
            self.schlange.append(self.kopf)
            self.schlange[0].place(x=START_POS_X, y=START_POS_Y, width=25, height=25) # hier ist doch was falsch

            for i in range(LAENGE_SCHLANGE):
                self.schlange_koord.append(Punkt(START_POS_X, START_POS_Y))
                self.schlange.append(tk.Label(self.canvas, bg='black', image=self.koerper_img))
                self.schlange[-1].place(x=START_POS_X-i*25-25, y=START_POS_Y, width=25, height=25)

            self.neues_spiel = False

    def links(self, event):
        """ Setzt die Richtungswerte für die linke Pfeiltaste.
            :param event: wird nicht verwendet
        """
        if self.x_richtung != 1:
            self.x_richtung = -1
            self.y_richtung = 0
            print("links")

    def rechts(self, event):
        """ Setzt die Richtungswerte für die rechte Pfeiltaste.
            :param event: wird nicht verwendet
        """
        if self.x_richtung != -1:
            self.x_richtung = 1
            self.y_richtung = 0
            print("rechts")

    def hoch(self, event):
        """ Setzt die Richtungswerte für die hoch Pfeiltaste.
            :param event: wird nicht verwendet
        """
        if self.y_richtung != 1:
            self.y_richtung = -1
            self.x_richtung = 0
            print("hoch")

    def runter(self, event):
        """ Setzt die Richtungswerte für die runter Pfeiltaste.
            :param event: wird nicht verwendet
        """
        if self.y_richtung != -1:
            self.y_richtung = 1
            self.x_richtung = 0
            print("runter")

    def tasten_funktionen(self):
        self.master.bind('<Left>', self.links)
        self.master.bind('<Right>', self.rechts)
        self.master.bind('<Up>', self.hoch)
        self.master.bind('<Down>', self.runter)

    def starte_spiel(self):
        self.starten = True

    def bewege_schlange(self):
         # Bewegt die Schlange weiter und prüft auf Kollisionen.

            kopf_x = self.schlange_koord[0].x
            kopf_y = self.schlange_koord[0].y

            if self.x_richtung == 1:
                x = kopf_x + 25
                y = kopf_y
            elif self.x_richtung == -1:
                x = kopf_x - 25
                y = kopf_y
            elif self.y_richtung == 1:
                x = kopf_x
                y = kopf_y + 25
            elif self.y_richtung == -1:
                x = kopf_x
                y = kopf_y - 25

            for i in range(len(self.schlange_koord)):
                x_old = kopf_x
                y_new = kopf_y
                if i == 0:
                    self.schlange_koord[i] = Punkt(x, y)
                    self.schlange[i].place(x=x_old, y=y_new, width=25, height=25)
                else:
                    self.master.destroy

    def aktualisiere(self):
    # Aktualisiert das GUI und führt die Spiellogik aus.
        if self.starten:
            self.bewege_schlange()
        self.after(500, self.aktualisiere)




