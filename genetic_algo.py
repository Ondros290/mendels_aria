from random import randint, choices, random, choice
from pyo import *
from tkinter import *
from mido import Message, MidiFile, MidiTrack,MetaMessage,bpm2tempo
import subprocess

class app:
	def __init__(self):	
		self.rating=[]
		self.konec = 0
	
class gen:
	def __init__(self,a,iterations,genlength,poplength,auto,pravdepodobnost,pocet_taktu):
		self.a=a
		self.iterations=iterations # počet generací (cyklů) genetického algoritmu
		self.genlength=genlength # délka genomu
		self.poplength=poplength # velikost populace
		self.auto=auto # způsob hodnocení (0=manuálně nebo 1=automaticky)
		self.pravdepodobnost=pravdepodobnost #pravděpodobnost, podle které se budou generovat geny v genomu v prvotni populaci
		self.pocet_taktu=pocet_taktu
		self.population=[] 
		self.generation=[]
		self.genom = []
		self.cislo_generace = 1
		self.p = 0
		self.seznam=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,100] #stupně ve stupnici, z kterých se vytvoří melodie (kromě: 0 = pauza; 100 = prodloužení předchozí noty)
		self.create_population() #vytvořit populaci
		
	def manual(self):
		if self.p < self.poplength:
			if self.a.konec == 0:
				self.p=self.p+1
			return self.population[self.p-1],self.cislo_generace,self.p
		else:
			self.p = 1
			n = self.nova_generace()
			if self.a.konec == 0:
				return self.population[self.p-1],self.cislo_generace,self.p
			else:
				return n,self.cislo_generace,self.p
	
			
	def automat(self):
		while self.a.konec == 0:
			for index,genom in enumerate(self.population):
				if self.a.konec == 0: #kontrola, zda už nebylo dosaženo požadovaného výsledku
					self.a.fitness.hodnoť(genom,self.genlength)
				else:
					return self.population[index - 1],self.cislo_generace
			if self.a.konec == 0:
				n = self.nova_generace()
				if self.a.konec == 1:
					return n,self.cislo_generace
					
	def pridej_hodnoceni (self,hodnoceni):
		## funkce, kterou zavolá uživatel, když vyhodnotí genom
		self.a.rating.append(hodnoceni)
	
	def nova_generace (self):
		## vytvoří novou generaci pomocí genetických operátorů 0.elitism; 1.selekce; 2.kížení; 3.mutace	
		self.cislo_generace = self.cislo_generace + 1	
		if self.cislo_generace <= self.iterations:
			
			print("prumer_hodnoceni "+str(sum(self.a.rating)/len(self.a.rating)))
			offset = min(self.a.rating)	
			positive_weights = [z - offset + 1 for z in self.a.rating]
				
			self.serazeny = [x for y,x in sorted(zip(self.a.rating,self.population))] #seřadit populaci podle hodnocení
			self.elitism = 0
			if self.poplength >= 20:
				self.elitism = 2
				for i in range(2): #elitism: 2 jedince s nejlepším hodnocením přesune rovnou do nové generace
					self.generation.append(self.serazeny[self.poplength-i-1]) 
					self.serazeny.pop(self.poplength-i-1)
			
			for genoms in range((self.poplength-self.elitism)//2): #proveď genetické operátory; vytvoř potomky
				parents = self.selection()
				offsprings = self.crossover(parents[0],parents[1])
				for offspring in offsprings:
					self.mutace(offspring)
				
			self.population.clear()
			for g in self.generation:
				self.population.append(g)
			self.generation.clear()
			
			self.a.rating.clear()

		else:
			best_rating = max(self.a.rating)
			index = (self.a.rating).index(best_rating)
			self.a.konec = 1	
			return self.population[index]
			
	def create_population(self):
		## vytvořit počáteční populaci
		## pravděpodobnost generování pauz a dlouhých not se může proti pravděpodobnosti generování obyčejných not lišit
		# podle toho, jak pravděpodobnosti nadefinoval uživatel
		sance_noty = (self.pravdepodobnost[0]*0.01*16)/14
		sance_pauzy = (self.pravdepodobnost[1]*0.01*16)
		sance_dlouhe_noty = (self.pravdepodobnost[2]*0.01*16)

		weights = [sance_pauzy]
		for i in range (16):
			if i in list(range(1,15)):
				weights.append(sance_noty)
		weights.append(sance_dlouhe_noty)
		print(weights)
		
		for i in range(self.poplength):
			self.population.append(choices(self.seznam,weights=weights,k=self.genlength))
    
	def selection(self):		
		### SELECTION (podle pořadí):	
		## seřadí genomy podle hodnocení a následně vybere 2 (různé) genomy na základě pravděpodobnosti	
		seznam = []
		seznam2 = []
		for x in range(self.poplength-self.elitism):
			seznam.append(x)		
		for x in range(2):
			s = choices(range(0,self.poplength-self.elitism), weights=range(0,self.poplength-self.elitism))
			seznam2.append(s[0])
			if x == 0:
				seznam.pop(s[0])
		return self.serazeny[seznam2[0]],self.serazeny[seznam2[1]]
		
	def crossover(self,a,b):
		## provede křížení mezi dvěma genomy 
		## pokud je genom kratší než 31, tak provede jednobodové křížení, jinak dvoubodové
		if self.genlength < 31:
			r=randint(0,self.genlength)
			return a[0:r]+b[r:],b[0:r]+a[r:]
		else:
			r1=randint(0,self.genlength)
			r2=randint(r1,self.genlength)
			return a[0:r1]+b[r1:r2]+a[r2:],b[0:r1]+a[r1:r2]+b[r2:]
	
	def mutace(self,genom):
		### MUTACE 1: nahradí náhodnou notu/pauzu jinou náhodnou notou/pauzou
		if randint(0,5)==1:
			r=randint(0,self.genlength-1)
			genom[r]=choice(self.seznam)
		
		### MUTACE 2: prohodí dvě sousední noty/pauzy
		if randint(0,5)==1:
			p=randint(1,self.genlength-1)
			genom = genom[0:p-1] + [genom[p]] + [genom[p-1]] + genom[p+1:]
		
		### MUTACE 3a: vytvoří pattern o náhodné délce na náhodné pozici		
		if randint(0,4)==1:
			if self.genlength > 31:
				if randint(0,1) == 0:		
					delka = randint((self.genlength//10),self.genlength//5) #náhodná délka
					pozice = randint(0,self.genlength-delka) #náhodná pozice
					self.mutace_pattern(genom,pozice,delka,1)			
		### MUTACE 3b: vytvoří pattern od dané délce na daných pozicích
				else:
					if self.pocet_taktu > 3:
						delka = 1 #délka se rovná délce jednoho taktu
						pozice = (randint(0,(self.genlength//self.a.fitness.noty_v_taktu)-delka)) #nová pozice bude jiný náhodný takt	
						self.mutace_pattern(genom,pozice,delka,self.a.fitness.noty_v_taktu)
		
		self.generation.append(genom)

	def mutace_pattern (self,genom,pozice,delka,y):
		### zkopíruje část genomu o určité délce a pozici, posune noty ve zkopírované-
		# -části o určitý interval (posun) a vloží na novou pozici v genomu ##

		if pozice + delka < self.genlength-delka:
			x = list(range(0,pozice-delka))+list(range(pozice+delka,(self.genlength//y)-delka))
		else:
			x = list(range(0,pozice-delka))
		
		nova_pozice = choice(x)
		
		pozice = pozice * y
		delka = delka * y
		nova_pozice = nova_pozice * y
		
		melody = []
		for x in genom[pozice:pozice+delka]:
			if x != 100 and x != 0:
				melody.append(x)
				
		if len(melody) != 0:		
			max_posun = max(melody)
			min_posun = min(melody)
			horni_hranice = 14 - max_posun 
			dolni_hranice = 1-min_posun
			posun = randint(dolni_hranice,horni_hranice)
		
		new_melody = list(genom)
					
		for x in range(delka):
			if genom[pozice+x] != 0 and genom[pozice+x] != 100:
				y = posun
			else:
				y = 0
			new_melody[nova_pozice+x] = genom[pozice+x]+y
		
		genom = new_melody

class fitness:
	def __init__ (self,a,delka_doby,pocet_dob,akordy):	
		self.a=a
		self.delka_doby = delka_doby
		self.pocet_dob = pocet_dob
		self.akordy = akordy
		self.noty_v_taktu = int(self.a.audio.jednotka/self.delka_doby*self.pocet_dob)
		self.all_ratings=[] #hodnocení jedné melodie různými automatickými hodnotícími funkcemi
					
	def hodnoť (self,genom,genlength):
		## Zavolá jednotlivé hodnotící funkce. Hodnocení z těchto funkcí se ukládá do seznamu. Finálním hodnocením genomu je aritmetický průměr prvků v tomto seznamu.
		self.intervals(genom)
		if self.akordy != 0:
			self.chords(genom)
			
		average=sum(self.all_ratings)/len(self.all_ratings)
				
		if average >= 0:
		## kontroluje, zda už bylo dosaženo požadovaného fitnessu
			print("genom "+str(genom))
			self.a.konec = 1			
		else:	
			self.a.rating.append(average)
		
		self.all_ratings.clear()
		
	def rytmus (self,genom):
		## vytvoří seznam s délkami not ##
		rhythm = list(genom)	
		
		self.x=0
		
		for i,r in enumerate(list(rhythm)):		
			if r!=100:
				rhythm[i]=1
				self.x=0
			if r==100 and i==0:
				rhythm[i]=1
			if r==100 and i!=0:	
				while rhythm[i-self.x]==100:
					rhythm[i-self.x-1]=rhythm[i-self.x-1]+1
					self.x=self.x+1
		
		rhythm = [x for x in rhythm if x != 100]
		
		return rhythm
	
	def chords(self,genom):
		## zjišťuje, zda jsou noty na těžké době (první doba v taktu) a noty delší než jedna jednotka (nejkratší nota) tóny akordickými 
		chord_notes = []
		long_notes = []
		beat = genom[0::self.noty_v_taktu]
		
		for i,x in enumerate(beat):
			o = 1
			if x == 100:
				if i != 0:
					while genom[i * self.noty_v_taktu - o] == 100:
						if o != self.noty_v_taktu:
							o = o + 1
						else:
							break
					else:
						if genom[i*self.noty_v_taktu-o] not in self.akordy[i]:
							chord_notes.append(-1)
							
			if x != 100:
				if x != 0:
					if x not in self.akordy[i]:
						chord_notes.append(-1)
		
		rytmus = self.rytmus(genom)
		melodie=[]
		for i,x in enumerate(genom):
			if x == 100 and i == 0:
				melodie.append(0)
			if x != 100:
				melodie.append(x)
				
		takt = 0
		pocet = 0
		for i,r in enumerate(rytmus):
			takt = takt + r 
			if r > 1:
				pocet = pocet + 1
				if takt % self.noty_v_taktu < r/2:
					a = -1
				else:
					a = 0
				akord = int(takt // self.noty_v_taktu) 
				if melodie[i] not in self.akordy[akord+a]:
					long_notes.append(-1*r)
		if pocet == 0:
			long_notes.append(-1)
			pocet = pocet + 1
				
		self.all_ratings.append(sum(chord_notes))
		self.all_ratings.append(sum(long_notes))
		
	def intervals (self,genom):
		list_of_intervals=[[0,1],[1,0],[2,0],[3,0],[4,0],[5,0],[6,4],[7,1],[8,2],[9,3],[10,4],[11,4],[12,3],[13,4],[14,4],[15,4]]
		tonality = [1,3,5,6,8,10,12,13]	# durová stupnice	
		bad_notes=0
		intervals_quality = []
		intervals = []		
		melody = [x for x in genom if (x != 100 and x != 0)] 
		
		for i,g in enumerate(melody):
			if (g not in tonality):
				bad_notes=bad_notes+1
			if i != 0:
				interval = melody[i]-melody[i-1]
				intervals_quality.append(list_of_intervals[abs(interval)][1])
				intervals.append(interval)
		if len(intervals)>0:
			prumer = sum(intervals_quality)/len(intervals_quality)
		else:
			prumer = 5 # pokud melodie neobsahuje aspoň dvě noty, tak není žádaná
		
		if len(melody)>0:
			prumer2 = 10*bad_notes/len(melody)
		else:
			prumer2 = 1

		self.all_ratings.append(0-prumer)
		self.all_ratings.append(0-prumer2)

		if len(genom) > 32:
			self.vzorec(intervals,genom)
			
	def vzorec(self,seq,genom):
		### začátek převzaté části ###
		## Zdroj: https://stackoverflow.com/questions/38770606/finding-patterns-in-list ##
			storage = {}	
			for length in range(5 ,int(len(seq)/2)+1):
					valid_strings = {}			
					for start in range(len(seq)-length+1):
							valid_strings[start] = tuple(seq[start:start+length])		
					candidates = set(valid_strings.values())				
					if len(candidates) != len(valid_strings):
							storage = valid_strings					
					else:		
							break
			celkem = 0
			print( set(v for v in storage.values() if list(storage.values()).count(v) > 1))
		### konec převzaté části ###
			for i in storage.values():
				pocet = list(storage.values()).count(i)
				if pocet > 1:
					celkem += length - 1
				
			rating = (celkem/len(genom)) 
			self.all_ratings.append(rating)
			#print(celkem) 
			#print(rating)	
 	
class audio:
	def __init__(self,a,root_note,bpm,oktáva,jednotka):
		self.a=a
		self.root_note=root_note # první nota v dané stupnici 
		self.bpm=bpm # tempo
		self.oktáva=oktáva # výška melodie
		self.jednotka = jednotka # nejkratší možná nota
		
		self.midi_numbers = range(21,109) ## chromatická (po půltónech) stupnice 	
		
		self.s = Server().boot() ## nastavit server, který vytváří zvuk
	
	def prevest_midi (self,melody):
		## převede stupně (0-14) na midi hodnoty	
		midi=[]	
		for index,ton in enumerate(melody):
			if ton!=0 and ton!=100:
				midi.append(self.midi_numbers[self.root_note-1+ton+12*self.oktáva])
			if ton==0:
				midi.append(0)
			if ton==100 and index == 0:
				midi.append(0)
						
		return midi	
	
	def zvuk(self,genom,genlength):
		
		rytmus = self.a.fitness.rytmus (genom)	
		midi = self.prevest_midi(genom)
		## přehraje genom 
		e=Events(midinote=EventSeq(midi),attack=0.001,decay=0.05,sustain=0.2,release=0.005,beat=EventSeq(rytmus),bpm=int(self.bpm*self.jednotka/4)).play()
		
		#### metronom: zdroj: kie codes, pyo doc.
		met = Metro(time=1 / ((self.bpm) / 60.0)).play() 
		t = CosTable([(0, 0), (50, 1), (200, .3), (500, 0)])
		amp = TrigEnv(met, table=t, dur=.25, mul=10)
		freq = Iter(met, choice=[660, 440, 440, 440])
		sine= Sine(freq=freq, mul=amp).mix().out()
		####
		self.s.start()
		time.sleep(float(genlength)/(float(self.bpm)*float(self.jednotka/4/60)))
		e.stop()
		self.s.stop()	
	
	def ulozit (self,genom,title,pocet_dob,delka_doby,directory):
		## uloží genom (melodii) jako soubor midi
		
		rytmus = self.a.fitness.rytmus (genom)	
		midi = self.prevest_midi(genom)
		
		stupnice=["A","Bb","B","C","C#","D","Eb","E","F","F#","G","Ab"]
		
		z=0
		mid = MidiFile(ticks_per_beat=4)
		track = MidiTrack()
		mid.tracks.append(track)
		track.append(MetaMessage('set_tempo',tempo=bpm2tempo(self.bpm)))
		track.append(MetaMessage('time_signature',numerator=pocet_dob,denominator=delka_doby))
		track.append(MetaMessage('key_signature', key=stupnice[self.root_note]))
		for x,y in zip(midi,rytmus):
			if x!=0:
				track.append(Message('note_on', note=x, velocity=64, time=z))
				track.append(Message('note_off', note=x, velocity=127, time=int(y*4/(self.jednotka/4))))
				z=0
			else:
				z=z+int(y*4/(self.jednotka/4))
		print(directory)
		mid.save(str(directory)+str("/")+str(title)+str(".mid"))
		
		print("saved!")
				
	def noty (self,title,directory_file,directory_musescore):	
		subprocess.Popen([directory_musescore, str(directory_file)+str("/")+str(title)+str(".mid")])


   

