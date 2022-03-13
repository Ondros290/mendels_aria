from tkinter import *
from tkinter import filedialog
from random import choice
import os
import genetic_algo as ga

class grafika:
	def __init__(self):
		self.okno=Tk()
		self.platno=Canvas(self.okno,width=600,height=800)
		self.platno.pack()
		
		self.img=PhotoImage(file="uvod.png") #uvodní pozadí
		self.img2=PhotoImage(file="background.png") #pozadí 
		
		self.pokrocila_nastaveni_done=0 # kontroluje, zda uživatel otevřel pokročilá nastavení (0 = Ne, 1 = Ano)
	
		self.uvod()
		
	def uvod (self):
		### úvodní obrazovka ###
		self.platno.create_image(0,0,image=self.img,anchor=NW)
		
		self.zacit=Button(self.platno,text='Start!',font="Arial 35",command=self.parameters)
		self.zacit.place(x=430,y=690)
		self.zacit.config(bg="#070e1a",fg="#90aff4")
	
		self.about=Button(self.platno,text='About',font="Arial 35",command=self.o_programu)
		self.about.place(x=20,y=690)
		self.about.config(bg="#070e1a",fg="#90aff4")
		
	def o_programu(self):
		### INFO o programu (tlacitko about) ###
		self.nove_pozadi = self.platno.create_image(0,0,image=self.img2,anchor=NW)
		self.about.config(text="Zpět",command=self.zpet)
		self.nadpis2 = self.platno.create_text(300,75,text="About",font="Arial 50 bold",fill="black")
		self.nadpis1 = self.platno.create_text(300,80,text="About",font="Arial 50 bold",fill="#5e84de")
		
	def zpet(self):
		### zpet na uvodni obrazovku z INFO o programu ###
		self.platno.delete(self.nove_pozadi,self.nadpis1,self.nadpis2)
		self.about.config(text="About",command=self.o_programu)
		
	def parameters(self):
		### základní parametry melodie ###
		self.zacit.destroy()
		self.about.destroy()
		
		self.stupnice = {"C":3,"Db":4,"D":5,"Eb":6,"E":7,"F":8,"Gb":9,"G":10,"Ab":11,"A":0,"Bb":1,"B":2}
		
		moznosti = [list(self.stupnice.keys()),list(range(1,7)),["Ano","Ne"],[1,7],[1,300],list(range(2,8)),[1,2,4,8]] # možnosti jednotlivých parametrů
		defaults = ["C",3,"Ne",3,130,4,4] # defaultní hodnoty parametrů
		nadpisy = ["Tónina","Oktáva","Akordy","Délka","Tempo","Takt"] #Názvy parametrů
		self.basic_parametry = [] #seznam, do kterého se uloží nastavení provedené uživatelem
			
		self.platno.create_image(0,0,image=self.img2,anchor=NW)
		self.nota = PhotoImage(file="nota.png") #obrazek ctvrtove noty u parametru Tempo
		self.keyboard=PhotoImage(file="keyboard.png") #obrazek klaviatury u parametru Oktáva po najetí myší na obrázek piana
		self.keyboard_icon=PhotoImage(file="keyboard_icon.png") #obrazek piana u parametru Oktáva
		
		self.platno.create_text(300,40,text='Parametry melodie',font="Arial 40 bold",fill="black") #nadpis
		self.platno.create_text(300,45,text='Parametry melodie',font="Arial 40 bold",fill="#5e84de")
		
		for x in range(3):
			## vytvoří widgety (optionmenu) v levém sloupci pro parametry: TÓNINA, OKTÁVA, AKORDY
			promenna=StringVar(self.platno)
			widget=OptionMenu(self.platno,promenna,*moznosti[x])
			promenna.set(defaults[x])
			widget.place(x=60,y=150 + x*120)
			widget.config(font='Arial 14',bg='#1c46a6',activebackground='#070e1a',activeforeground='white',fg='white')	
			self.basic_parametry.append(promenna)
			self.platno.create_text(110,120+x*120,text=nadpisy[x],font="Arial 25",fill="#5e84de")
		self.platno.create_text(150,170,text='Dur',font='Arial 18',fill='#5e84de')	
		
		for x in range(2):
			## vytvoří widgety (Spinboxy) v pravém sloupci pro parametry: DÉLKA, TEMPO
			promenna2=StringVar(self.platno)
			print(x)
			widget2=Spinbox(self.platno,textvariable=promenna2,from_=moznosti[3+x][0],to=moznosti[3+x][1],width=3)
			promenna2.set(defaults[3+x])
			widget2.place(x=430,y=150 + x*120)
			widget2.config(font='Arial 17',bg='#1c46a6',fg='#90aff4')	
			self.basic_parametry.append(promenna2)
			self.platno.create_text(460,120+x*120,text=nadpisy[3+x],font="Arial 25",fill="#5e84de")
			
		for x in range(2):
			## vytvoří dva widgety pro TAKT 
			promenna3=IntVar(self.platno)
			widget3=OptionMenu(self.platno,promenna3,*moznosti[x+5])
			promenna3.set(defaults[5+x])
			widget3.place(x=390+x*80,y=390)
			widget3.config(font='Arial 14',bg='#1c46a6',activebackground='#070e1a',activeforeground='white',fg='white')	
			self.basic_parametry.append(promenna3)
			self.platno.create_text(460,360,text="Takt",font="Arial 25",fill="#5e84de")
			self.platno.create_text(460,410,text='/',font="Arial 25",fill="#5e84de")

		## AKORDY - nápověda ##	
		self.napoveda1 = Label(self.platno,text='?',font='Arial 8',bg='#5375c6',fg='black')
		self.napoveda1.place(x=140,y=400)		
		self.napoveda1.bind("<Enter>", lambda event: self.show_napoveda(event,"Definovat sled\n akordů, který \n algoritmus vezme\n v úvahu při \ngenerování melodíí?",self.napoveda1))
		self.napoveda1.bind("<Leave>", lambda enter: self.hide_napoveda(enter,self.napoveda1))
		
		## OKTÁVA - klaviatura ##		
		self.piano = Label(self.platno,image=self.keyboard_icon,font='Arial 8',bg='#5375c6',fg='black')
		self.piano.place(x=120,y=280) #https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python			
		self.piano.bind("<Enter>",self.klaviatura)
		self.piano.bind("<Leave>",self.hide_klaviatura)
		
		## POKROČILÁ NASTAVENÍ (rozbalit) ##
		self.nastaveni = Button(self.platno,text='Pokročilá nastavení',font='Arial 15',bg="#90aff4",fg='black',command=self.pokrocila_nastaveni)
		self.nastaveni.place(x=200,y=690)
		
		## POTVRDIT PARAMETRY ##
		tlacitko=Button(self.platno,text="NOVÁ HITPARÁDA!",font='Arial 20',fg='white',bg='#070e1a',activebackground='black',activeforeground='white',command=self.get)
		tlacitko.place(x=160,y=745)
	
	def klaviatura(self,event):
		## ukázat klaviaturu (po najetí kurzoru na ikonku piana)
		self.piano.config(image=self.keyboard) 
		
	def hide_klaviatura(self,enter):
		## schovat klaviaturu (po přesunutí kurzoru z ikonky piana)
		self.piano.config(image=self.keyboard_icon)
	
	def pokrocila_nastaveni(self):
		### zobrazit pokročilá nastavení (pokud uživatel kliknul na tlačítko Pokročilá nastavení) ###
			self.pokrocila_nastaveni_done = 1 #informace, že uživatel spustil pokročilá nastavení
			self.pravdepodobnost_edit = 0 #kontrola, zda uživatel kliknul na tlačítko Edit u parametru pravděpodobnost
			
			self.platno2=Canvas(self.platno,width=560,height=258,bg='#0a101e') 
			self.platno2.place(x=20,y=485)
			
			## MAXIMÁLNÍ POČET GENERACÍ ##
			self.platno2.create_text(160,20,text='Max počet generací',font="Arial 15",fill="#5e84de")
			self.iterations=Spinbox(self.platno2,from_=8, to=100,width=4)
			self.iterations.delete(0)
			self.iterations.insert(0,250)
			self.iterations.place(x=130,y=40)
			self.iterations.config(font='Arial 16',bg='#1c46a6',fg='#90aff4')
			
			self.napoveda2 = Label(self.platno,text='?',font='Arial 8',bg='#5375c6',fg='white')
			self.napoveda2.place(x=220,y=530) #https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
			self.napoveda2.bind("<Enter>", lambda event: self.show_napoveda(event,"Po kolika generacích (cyklech) \n má algoritmus skončit, pokud\n do té doby nenalezne \nuspokojivé řešení ",self.napoveda2))
			self.napoveda2.bind("<Leave>", lambda enter: self.hide_napoveda(enter,self.napoveda2))
			
			## VELIKOST POPULACE ##
			self.platno2.create_text(400,20,text='Velikost populace',font="Arial 15",fill="#5e84de")
			self.platno2.create_text(400,40,text='Zvolte sudé číslo!',font="Arial 10",fill="#5e84de")	
			self.poplength=Spinbox(self.platno2,from_=3, to=1000,width=4)
			self.poplength.delete(0)
			self.poplength.insert(0,200)
			self.poplength.place(x=370,y=55)
			self.poplength.config(font='Arial 16',bg='#1c46a6',fg='#90aff4')
			
			self.napoveda3 = Label(self.platno,text='?',font='Arial 8',bg='#5375c6',fg='white')
			self.napoveda3.place(x=460,y=540)
			self.napoveda3.bind("<Enter>", lambda event: self.show_napoveda(event,"Počet náhodně\nvygenerovaných\nmelodií, z kterých\n se bude vyvíjet\nmelodie finální",self.napoveda3))
			self.napoveda3.bind("<Leave>", lambda enter: self.hide_napoveda(enter,self.napoveda3))
			
			## ZPŮSOB HODNOCENÍ ##
			self.platno2.create_text(100,140,text='Melodie hodnotit',font="Arial 15",fill="#5e84de")	
			self.promenna4 = StringVar()
			self.promenna4.set(1) 
			Radiobutton(self.platno2, text="...automaticky", variable=self.promenna4, value=1,bg='#070e1a',font="Rockwell 14",activebackground='black',activeforeground='white',fg='#5e84de').place(x=30,y=150) 
			Radiobutton(self.platno2, text="...manuálně", variable=self.promenna4, value=0,bg='#070e1a',font="Rockwell 14",activebackground='black',activeforeground='white',fg='#5e84de').place(x=30,y=180) 	
			
			self.napoveda4 = Label(self.platno,text='?',font='Arial 8',bg='#5375c6',fg='white')
			self.napoveda4.place(x=210,y=615)
			self.napoveda4.bind("<Enter>", lambda event: self.show_napoveda(event,"Způsob, kterým\n bude algoritmus \n hodnotit kvalitu\nmelodie. \n Automaticky = Melodie\nhodnotí algoritmus \n Manuálně = Melodie\n hodnotí uživatel",self.napoveda4))
			self.napoveda4.bind("<Leave>", lambda enter: self.hide_napoveda(enter,self.napoveda4))
			
			## NEJKRATŠÍ NOTA ##
			self.platno2.create_text(480,140,text='Nejkratší nota',font="Rockwell 15",fill="#5e84de")
			self.promenna5=IntVar(self.platno2)
			self.promenna5.set(8)
			self.jednotka=OptionMenu(self.platno2,self.promenna5,'2','4','8','16')
			self.jednotka.place(x=450,y=160)
			self.jednotka.config(font='Rockwell 13',bg='#1c46a6',activebackground='#070e1a',activeforeground='white',fg='#90aff4')
			
			self.napoveda5 = Label(self.platno,text='?',font='Arial 8',bg='#5375c6',fg='white')
			self.napoveda5.place(x=530,y=650)			
			self.napoveda5.bind("<Enter>", lambda event: self.show_napoveda(event,"Nejkratší\n možná \ndélka \njedné noty.",self.napoveda5))
			self.napoveda5.bind("<Leave>", lambda enter: self.hide_napoveda(enter,self.napoveda5))
			
			## PRAVDĚPODOBNOST ##
			self.platno2.create_text(310,140,text='Pravděpodobnost',font="Rockwell 15",fill="#5e84de")
			self.platno2.create_text(310,160,text='pauz a dlouhých not',font="Rockwell 10",fill="#5e84de")
			tlacitko=Button(self.platno2,text="Edit",font='Rockwell 12',fg='white',bg='#1c46a6',activebackground='black',activeforeground='white',command=self.pravdepodobnost)
			tlacitko.place(x=285,y=180)
			
			self.napoveda6 = Label(self.platno,text='?',font='Arial 8',bg='#5375c6',fg='white')
			self.napoveda6.place(x=350,y=670)		
			self.napoveda6.bind("<Enter>", lambda event: self.show_napoveda(event,"Pravděpodobnost výskytu pauz,krátkých \na dlouhých not v prvotní populaci.\nautomaticky nastaveno na:\n krátké noty 70% \n dlouhé noty/pauzy 20% \n pauzy 10%",self.napoveda6))
			self.napoveda6.bind("<Leave>", lambda enter: self.hide_napoveda(enter,self.napoveda6))
				
	def show_napoveda(self, event,text,napoveda):
		## ukaž  text nápovědy po najetí kurzoru na Label s otazníčkem ##
		napoveda.config(text=text)		
	
	def hide_napoveda(self,enter,napoveda):
		## nahraď text nápovědy otazníkem po přesunutí kurzoru z Labelu ##
		napoveda.config(text="?")
		
	def pravdepodobnost(self):
		## pokud chce uživatel změnit pravděpodobnost generování různých typů not, klikne na Edit
		## otevře se okno s možností pravděpodobnosti upravit
		self.okno2=Tk()
		self.okno2.configure(background = '#0a101e')
		self.okno2.title('Pravděpodobnost')
		
		titulek = Label(self.okno2,text="Pravděpodobnost výskytu \n v prvotní populaci",font='Arial 14',bg='#0a101e',fg='white')
		titulek.grid(column=1,row=1)
		
		nota = Label(self.okno2,text="nota (%)",font='Arial 14',bg='#0a101e',fg='#90aff4')
		nota.grid(column=1,row=2)
		self.nota_sance=Spinbox(self.okno2,from_=1, to=98,width=2)
		self.nota_sance.delete(0)
		self.nota_sance.insert(0,70)
		self.nota_sance.grid(column=2,row=2)
		self.nota_sance.config(font='Rockwell 14',bg='#1c46a6',fg='#90aff4')
	
		pauza = Label(self.okno2,text="pauza (%)",font='Arial 14',bg='#0a101e',fg='#90aff4')
		pauza.grid(column=1,row=3)
		self.pauza=Spinbox(self.okno2,from_=1, to=98,width=2)
		self.pauza.delete(0)
		self.pauza.insert(0,10)
		self.pauza.grid(column=2,row=3)
		self.pauza.config(font='Rockwell 14',bg='#1c46a6',fg='#90aff4')
		
		dlouha_nota = Label(self.okno2,text="dlouhá nota/\n/dlouhá pauza (%)",font='Arial 12',bg='#0a101e',fg='#90aff4')
		dlouha_nota.grid(column=1,row=4)
		self.dlouha_nota=Spinbox(self.okno2,from_=1, to=98,width=2)
		self.dlouha_nota.delete(0)
		self.dlouha_nota.insert(0,20)
		self.dlouha_nota.grid(column=2,row=4)
		self.dlouha_nota.config(font='Rockwell 14',bg='#1c46a6',fg='#90aff4')
		
		tlacitko=Button(self.okno2,text="OK",font='Rockwell 15',fg='white',bg='#1c46a6',activebackground='black',activeforeground='white',command=self.kontrola_pravdepodobnosti)
		tlacitko.grid(column = 2,row = 5)
		
	def kontrola_pravdepodobnosti(self):
		## kontrola, zda je součet pravděpodobností roven 100 % ##
		self.pravdepodobnost_edit = 1 # informace, že uživatel kliknul na tlačítko OK v okně pravděpodobnost 
		nota=self.nota_sance.get()
		pauza=self.pauza.get()
		dlouha_nota=self.dlouha_nota.get()
		self.pravdepodobnost = []
		if (int(nota) + int(pauza) + int(dlouha_nota)) == 100:
			self.pravdepodobnost = [int(nota),int(pauza),int(dlouha_nota)]
			self.okno2.destroy()
		else:
			upozorneni=Label(self.okno2,text="Součet musí být roven 100%",font='Arial 12',bg='#0a101e',fg='red')
			upozorneni.grid(column=1,row=5)
	
	def kontrola_parametru(self,parametr,nazev,popis,x,y):
		## zkontroluj parametr (zda se jedná o číslici a zda je v platném rozsahu) ##
		if parametr.isdigit() == False:
			self.error(nazev,popis)
			self.kontrola_done = False # informace, že kontrola u parametru neproběhla v pořádku
		else:
			if int(parametr) not in list(range(x,y)):
				self.error(nazev,"Zvolte číslo v rozsahu od "+str(x)+" do "+str(y))
				self.kontrola_done = False
				
	def error(self,nazev,popis):
		## upozorni uživatele na chybu v nastavení ##
		upozorneni = Tk()
		upozorneni.configure(background = '#0a101e')
		Label(upozorneni,text=str(nazev)+"\n"+str(popis),font="Arial 18",bg="#0a101e",fg="red").pack()
		Button(upozorneni,text="OK",font="Arial 16",bg="#1c46a6",fg="white",command=upozorneni.destroy).pack() 
		
	def get (self):
		## spouští se po kliknutí na tlačítko Nová hitparáda (potvrzení parametrů)
		## pošli parametry do funkce kontrola_parametru ke kontrole. Pokud kontrolou projdou, pokračuj 
		self.kontrola_done = True # kotrolní promenna, True = kontrola je v ok, False = chyba v nastavení.
		
		self.pocet_taktu = self.basic_parametry[3].get()
		self.kontrola_parametru(self.pocet_taktu,"Délka","Přirozené číslo!",1,16)
		
		self.root_note = self.stupnice[self.basic_parametry[0].get()]
		
		self.tempo = self.basic_parametry[4].get()
		self.kontrola_parametru(self.tempo,"Tempo","Přirozené číslo!",1,300)
		
		self.oktava = self.basic_parametry[1].get()	
		self.pocet_dob = self.basic_parametry[5].get()
		self.delka_doby = self.basic_parametry[6].get()
		
		if self.pokrocila_nastaveni_done != 0:
			## pokud uživatel otevřel pokročilá nastavení, tak je algoritmus použije 
			## pokud uživatel neotevel pokročilá nastavení, použije implicitní (default) nastavení	
			self.iterations = self.iterations.get()
			self.kontrola_parametru(self.iterations,"Max počet generací","Přirozené číslo!",3,9999)
				
			self.poplength = self.poplength.get()
			self.kontrola_parametru(self.poplength,"Velikost populace","Přirozené sudé číslo!",4,998)
			
			if self.kontrola_done != False: ## pokud žádná hodnota dosud nebyla neplatna, zkontroluj, zda je velikost populace sudá
				if int(self.poplength)%2 != 0:
					self.kontrola_done = False ##pokud není velikost populace sudá, zavolej error (upozornění uživatele)
					self.error("Velikost populace","Zvolte sudé číslo!")
					
			self.typ_fitness = self.promenna4.get()
			self.jednotka = self.promenna5.get()
			if self.pravdepodobnost_edit == 0: #jestliže uživatel needitoval pravděpodobnosti, použij defaultní nastavení
				self.pravdepodobnost = [70,10,20]
		else:
			# pokud uživatel neotevřel pokročilá nastavení, použij defaultní nastavení
			self.iterations = 250
			self.poplength = 200
			self.typ_fitness = 1
			self.jednotka = 8
			self.pravdepodobnost = [70,10,20]
			
		if self.kontrola_done == True: # pokud jsou všechny parametry v pořádku
			self.genlength = ((self.jednotka/self.delka_doby)*int(self.pocet_dob)*int(self.pocet_taktu)) # spočítej délku genomu (závisí na jednotce, délce doby, počtu dob a taktů
			
			self.platno.delete('all')
			self.platno.create_image(0,0,image=self.img2,anchor=NW)
			for widget in self.platno.winfo_children():
				widget.destroy()
		
			if self.basic_parametry[2].get() == "Ano":
				self.definovat_akordy() #pokud uživatel v nastavení uvedl, že che použít akordy, nech uživatele akordy definovat
			else:
				self.skladam = Label(self.platno,text="Skládám...",font="Arial 40",bg='#070e1a',fg="#5e84de")
				self.skladam.place(x=180,y=120)
				self.okno.after(2,lambda:self.spustit(0)) #jinak spusť genetický algoritmus
			
	def spustit(self,akordy):
		## spustit algoritmus ##
		self.app = ga.app()
		self.app.audio=ga.audio(self.app,int(self.root_note),int(self.tempo),int(self.oktava),self.jednotka)
		self.app.fitness=ga.fitness(self.app,self.delka_doby,self.pocet_dob,akordy)	
		self.app.gen=ga.gen(self.app,int(self.iterations),int(self.genlength),int(self.poplength),int(self.typ_fitness),self.pravdepodobnost,int(self.pocet_taktu))
		
		## PŘEHRÁT
		self.tlacitko_prehrat=Button(self.platno,text="Přehrát",font="Arial 30",bg="#5e84de")		
		## ULOŽIT
		self.tlacitko_ulozit = Button(self.platno,text="Uložit",font="Arial 30",bg="#5e84de")
		## UKONČIT
		Button(self.platno,text="Zavřít",font="Arial 30",bg="#5e84de",fg="white",command=lambda:self.okno.quit()).place(x=25,y=700)
		
		self.scale = Scale(self.platno,from_= 0,to = 3,font="Arial 25",orient=HORIZONTAL,bg="#5e84de",cursor="fleur",length=120,width=30) #stupnice pro manuální hodnocení
		self.tlacitko_pokracovat = Button(self.platno, text="Pokračuj", font="Arial 30",command=self.pridej_hodnoceni,bg="#5e84de",fg="white") # pro manuální hodnocení
		
		self.generace = Label(self.platno,text="Generace 0",font='Arial 30',bg='#070e1a',fg="#5e84de")
		self.melodie = Label(self.platno,text="Melodie 0",font="Arial 20",bg='#5e84de')
		
		self.skladam.destroy()
		
		if int(self.typ_fitness) == 1: 
			# použít AUTOMATICKÉ hodnocení
			self.automat()			
			self.generace.place(x=180,y=120) # číslo generace
			self.tlacitko_prehrat.place(x=210,y=300) # tlačítko pro přehrání melodie
			self.tlacitko_ulozit.place(x=225,y=500) # tlačítko pro uložení melodie
		else:
			# použít MANUÁLNÍ hodnocení
			self.scale.place(x=230,y=290) # stupnice pro manuální hodnocení
			self.tlacitko_prehrat.place(x=210,y=510) # tlačítko pro přehrání melodie
			self.tlacitko_pokracovat.place(x=200,y=390) #tlačítko pro pokračování po vyhodnocení melodie
			self.tlacitko_ulozit.place(x=225,y=600) # tlačítko pro uložení melodie
			self.generace.place(x=200,y=100) # nápis číslo generace
			self.melodie.place(x=230,y=150) #nápis číslo melodie
			self.platno.create_text(300,55,text="Líbí se vám tato melodie?",font="Arial 35 bold",fill="black")
			self.platno.create_text(300,60,text="Líbí se vám tato melodie?",font="Arial 35 bold",fill="#5e84de")		
			self.platno.create_text(300,270,text="0 = Odpad\n3 = Jde to",font="Arial 10 bold",fill="white") #vysvětlivky k self.scale
			self.manual()

	
	def manual(self):
		genom,generace,melodie = self.app.gen.manual()
		self.tlacitko_ulozit.config(command=lambda:self.ulozit(genom))
		self.tlacitko_prehrat.config(command=lambda:self.app.audio.zvuk(genom,len(genom)))
		self.generace.config(text="Generace "+str(generace))
		self.melodie.config(text="Melodie "+str(melodie))
		if generace==int(self.iterations)+1: #pokud bylo dosaženo maximálního počtu generací, upozornit uživatele
			self.generace.destroy()
			self.melodie.destroy()
			self.tlacitko_ulozit.destroy()
			self.scale.destroy()
			self.platno.create_text(280,410,text="Dosažen maximální\n   počet generací",font="Arial 30",fill="white")
			self.tlacitko_prehrat.config(text="Přehrát nejlepší melodii\nv poslední generaci",font="Arial 14")
		
	def pridej_hodnoceni(self):
		## přidat uživatelovo hodnoceni do seznamu hodnoceni, když klikne na tlačítko Pokračuj
		self.app.gen.pridej_hodnoceni(self.scale.get())	
		self.manual() # další melodie z populace
		
	def automat(self):
		genom = self.app.gen.automat() # vítězný finální genom
		self.platno.create_text(300,60,text="Hotovo!",font='Arial 40',fill='white')	
		self.tlacitko_prehrat.config(command=lambda:self.app.audio.zvuk(genom[0],len(genom[0])))
		self.tlacitko_ulozit.config(command=lambda:self.ulozit(genom[0]))
		self.generace.config(text="Generace "+str(genom[1]-1))	

	def ulozit(self,genom):
		# spuštění po kliknutí na tlačítko uložit
		# název ukládané melodie
		self.tlacitko_ulozit.destroy()
		self.title = Entry (self.platno,font="Arial 20",width="10",bg="white") 
		self.title.place(x=215,y=600)
		self.title.insert(0,"nazev")		
		self.potvrd = Button(self.platno,text="OK",font="Arial 20",bg="#5e84de",command=lambda:self.ok(genom))
		self.potvrd.place(x=260,y=640)
			
	def ok(self,genom):
		# umístění ukládané melodie
		self.file_directory = filedialog.askdirectory() #otevře prohlížeč souborů 
		self.file_title=self.title.get() #název mmelodie
		self.app.audio.ulozit(genom,self.file_title,self.pocet_dob,self.delka_doby,self.file_directory)	#ulozit melodii
		self.musescore() 
		
	def musescore(self):
		# zobrazit tlačítko pro zobrazení not, pokud je nainstalován program Musescore
		self.uloz_directory = open('directory.txt','r+') #otevři textový soubor, ve kterém je nahrané předpokládané umístění programu MuseScore
		self.directory_musescore = self.uloz_directory.read() #přečti adresu z textového souboru
		self.uloz_directory.close() #zavři textový soubor
		print(self.directory_musescore)
		if os.path.isfile(str(self.directory_musescore)) == True: #pokud adresa existuje, zobraz tlačítko, kterým se otevře musescore
			Button(self.platno,text="Noty\n(MuseScore)",font="Arial 24",bg="#5e84de",command=lambda:self.app.audio.noty(self.file_title,self.file_directory,self.directory_musescore)).place(x=180,y=600)
		else: # jinak zobraz upozornění, že nejspíš není nainstalován musescore
			self.nelze_noty = Label(self.platno,text="Nelze zobrazit noty \nMuseScore3 není nejspíš nainstalován",font="Arial 16",bg="#5e84de")
			self.nelze_noty.place(x=120,y=600)
			# pokud je musescore nainsatlován, může uživatel určit jeho umístění
			self.najit_musescore=Button(self.platno,text="Pokusit se najít MuseScore\n(pokud je nainstalován)",font="Arial 14",bg="#5e84de",command=self.directory)
			self.najit_musescore.place(x=180,y=680)
			
		self.title.destroy()
		self.potvrd.destroy()
	
	def directory(self):
		## zjistit umístění programu Musescore
		self.directory_musescore = filedialog.askopenfilename() #otevřít prohlížeč souborů 
		self.uloz_directory = open('directory.txt','w') 
		self.uloz_directory.write(self.directory_musescore) #uložit vybrané umístění do textového souboru
		self.uloz_directory.close()
		self.nelze_noty.destroy()
		self.najit_musescore.destroy()
		self.musescore() # opět zkontrolovat, zda je nové umístění platné. POkud ano, zobrazit tlačítko pro zobrazení not v musescoru

	def definovat_akordy(self):
		## pokud uživatel vybral "Ano" pro parametr Akordy, musí ještě před spuštěním genetického algoritmu, vybrat akord pro každý takt
		self.platno.create_text(300,40,text='Sled akordů:',font="Arial 30 bold",fill="black")
		self.platno.create_text(300,43,text='Sled akordů:',font="Arial 30 bold",fill="#5e84de")	
		self.platno.create_text(300,73,text='(Chord progression)',font="Arial 16",fill="#5e84de")	
			
		for x in range(int(self.pocet_taktu)):
			self.platno.create_text(100,130+x*40,text="Takt "+str(x+1),font="Arial 20",fill="white")
			
		stupnice = [] # list, kam se uloží všech sedm akordů patřících dané tónině
		stupne = [0,2,4,5,7,9,11] # durová stupnice (stupně odpovídají stupňum v chromatické (půltonové) stupnici
		mollove_akordy = [2,4,9,11] # stupně, na kterých jsou postaveny mollové (případně zmenšené) akordy (2.,3.,6.,7, stupen v durové stupnici)
		
		for x in stupne:
			if x in mollove_akordy:
				if x != 11:
					text = "m" #značka pro molový akord
				else:
					text = "m(b5)" #značka pro zmenšený akord
			else:
				text = "" # durový akord se značí pouze písmenem jeho první noty
					
			if self.root_note + x < 12: 
				stupnice.append(list(self.stupnice.keys())[x+self.root_note-3]+text) # vytvořit název akordu: název první noty akordu + značka pro molový, durový, zmenšený akord
			else:
				stupnice.append(list(self.stupnice.keys())[x+self.root_note-15]+text) 
		
		tlacitko=Button(self.platno,text="OK!",font='Arial 40',fg='white',bg='#070e1a',activebackground='black',activeforeground='white',command=lambda:self.kontrola_akordu(stupnice))
		tlacitko.place(x=440,y=680)	
		
		tlacitko2=Button(self.platno,text="Random!",font='Arial 20',fg='white',bg='#1c46a6',activebackground='black',activeforeground='white',command=lambda:self.random_akordy(stupnice))
		tlacitko2.place(x=440,y=580)
		
		self.option_menus(stupnice)
		
	def option_menus (self,stupnice):
		## vytvořit tolik widgetů (optionmenu), kolik je taktů. 
		self.optionmenus = []
		self.vybrane_akordy = [] # akordy, které uživatel zvolil
					
		for x in range(int(self.pocet_taktu)):
			self.promenna8=StringVar(self.platno)
			takt=OptionMenu(self.platno,self.promenna8,*stupnice)
			takt.place(x=200,y=110+x*40)
			takt.config(font='Rockwell 14',bg='#1c46a6',activebackground='#070e1a',activeforeground='white',fg='white')	
			self.optionmenus.append(self.promenna8)
		
	def random_akordy(self,stupnice):
		## náhodně vybrat akordy
		for i in self.optionmenus:
			chord = choice(stupnice)
			i.set(chord)
			
	def kontrola_akordu(self,stupnice):
		## kontrola, zds jsou akordy vybrané ve všech taktech
		kontrola = True 
		for chord in self.optionmenus:
			x = chord.get()
			if x == "":
				kontrola = False
			else:
				self.vybrane_akordy.append(x)
		if kontrola == True:
			self.get_chords(stupnice)		
		else:
			self.vybrane_akordy = []
			self.error("CHYBÍ AKORDY","Doplňte akordy do taktů nebo klikněte na tlačítko Random")
			
	def get_chords(self,stupnice):
		## převest vybrané názvy akordů na akordy rozepsané do not
		self.platno.delete('all')
		self.platno.create_image(0,0,image=self.img2,anchor=NW)	
		for widget in self.platno.winfo_children():
			widget.destroy()
		
		chord_progression = []

		akordy = {stupnice[0]:[1,5,8,13],stupnice[1]:[3,6,10],stupnice[2]:[5,8,12],stupnice[3]:[1,6,10,13],stupnice[4]:[3,6,8,12],stupnice[5]:[1,5,10,13],stupnice[6]:[3,6,12]}
		
		for x in self.vybrane_akordy:
			chord_progression.append(akordy[x])
		
		self.skladam = Label(self.platno,text="Skládám...",font="Arial 40",bg='#070e1a',fg="#5e84de")
		self.skladam.place(x=180,y=120)
		self.okno.after(2,lambda:self.spustit(chord_progression))
		
g=grafika()
mainloop()

