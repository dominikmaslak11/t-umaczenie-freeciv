import tkinter as tk
from tkinter import messagebox
import math

# --- LOGIKA MATEMATYCZNA (Łańcuchy Markowa dla serii ataków) ---
def oblicz_fale_atakow(s, r, a_hp, d_hp, a_fp, d_fp):
    p = s / (s + r)
    q = 1.0 - p
    
    # Słownik przechowujący rozkład prawdopodobieństwa HP obrońcy.
    # Na początku obrońca ma na 100% (1.0) swoje początkowe HP.
    probs = {h: 0.0 for h in range(d_hp + 1)}
    probs[d_hp] = 1.0
    
    wyniki = []
    
    # Symulujemy kolejne fale (maksymalnie 20 jednostek, żeby uniknąć nieskończonej pętli)
    for fala in range(1, 21):
        # Nowy rozkład HP po tej fali ataków
        nowe_probs = {h: 0.0 for h in range(d_hp + 1)}
        
        # Jeśli obrońca już zginął w poprzednich falach, pozostaje martwy
        nowe_probs[0] = probs[0]
        
        # Analizujemy każdy możliwy stan HP, w jakim mógł przetrwać obrońca
        for h, prob_h in probs.items():
            if h == 0 or prob_h == 0:
                continue # Pomijamy stany niemożliwe lub gdy obrońca nie żyje
            
            k = math.ceil(h / a_fp)
            l = math.ceil(a_hp / d_fp)
            md = k + l - 1
            
            # Scenariusz A: Atakujący wygrywa (obrońca traci całe obecne HP)
            prawd_wygranej_atakujacego = 0.0
            for i in range(k, md + 1):
                prawd_wygranej_atakujacego += math.comb(md, i) * (p**i) * (q**(md - i))
            
            nowe_probs[0] += prob_h * prawd_wygranej_atakujacego
            
            # Scenariusz B: Obrońca wygrywa, ale obrywa 'a' razy
            for a in range(k):
                # Rozkład ujemny dwumianowy: szansa na 'a' sukcesów zanim nastąpi 'l' porażek
                prawd_scenariusza = math.comb(l - 1 + a, a) * (p**a) * (q**l)
                
                # Nowe HP obrońcy po otrzymaniu 'a' trafień
                nowe_hp = h - (a * a_fp)
                if nowe_hp < 1: 
                    nowe_hp = 1 # Teoretyczne zabezpieczenie
                
                nowe_probs[nowe_hp] += prob_h * prawd_scenariusza
                
        probs = nowe_probs
        szansa_zabicia = probs[0]
        wyniki.append((fala, szansa_zabicia))
        
        # Jeśli jesteśmy w 99.5% pewni, że cel padł, przerywamy symulację kolejnych fal
        if szansa_zabicia > 0.995:
            break
            
    return wyniki

# --- INTERFEJS GRAFICZNY (GUI) ---
def uruchom_symulacje_oblężenia():
    try:
        s = float(entry_s.get())
        a_hp = int(entry_a_hp.get())
        a_fp = int(entry_a_fp.get())
        
        r = float(entry_r.get())
        d_hp = int(entry_d_hp.get())
        d_fp = int(entry_d_fp.get())
        
        if any(val <= 0 for val in [s, r, a_hp, d_hp, a_fp, d_fp]):
            messagebox.showerror("Błąd", "Wszystkie wartości muszą być większe od 0.")
            return
            
        wyniki = oblicz_fale_atakow(s, r, a_hp, d_hp, a_fp, d_fp)
        
        # Budowanie raportu
        text_wynik.config(state=tk.NORMAL)
        text_wynik.delete(1.0, tk.END)
        
        text_wynik.insert(tk.END, "SKUMULOWANE SZANSE NA ZDOBYCIE POZYCJI:\n")
        text_wynik.insert(tk.END, "-"*40 + "\n")
        
        rekomendacja = 0
        
        for fala, szansa in wyniki:
            procent = szansa * 100
            pasek_postepu = "█" * int(procent / 5) + "░" * (20 - int(procent / 5))
            text_wynik.insert(tk.END, f"{fala} jednostek: [{pasek_postepu}] {procent:>5.1f}%\n")
            
            # Szukamy momentu, gdzie mamy "pewność" wygranej (>90%)
            if procent >= 90.0 and rekomendacja == 0:
                rekomendacja = fala
                
        text_wynik.insert(tk.END, "-"*40 + "\n\n")
        
        if rekomendacja > 0:
            text_wynik.insert(tk.END, f"WERDYKT: Aby mieć ponad 90% szans na sukces,\nprzygotuj minimum {rekomendacja} jednostek.\n")
        else:
            text_wynik.insert(tk.END, "WERDYKT: Ta pozycja jest niezwykle trudna!\nNawet potężna armia może nie wystarczyć.\n")
            
        text_wynik.config(state=tk.DISABLED)
        
    except ValueError:
        messagebox.showerror("Błąd", "Proszę wprowadzić poprawne wartości liczbowe.")

# --- INICJALIZACJA OKNA ---
root = tk.Tk()
root.title("Kalkulator Oblężeń Freeciv (N vs 1)")
root.geometry("450x620")
root.resizable(False, False)

tk.Label(root, text="Kalkulator Fal Ataków (Ilu potrzeba by zabić?)", font=("Arial", 11, "bold")).pack(pady=5)

# Ramka Atakujących
frame_atak = tk.LabelFrame(root, text="Parametry POJEDYNCZEGO Atakującego", padx=10, pady=10)
frame_atak.pack(fill="x", padx=10, pady=5)

tk.Label(frame_atak, text="Siła Ataku:").grid(row=0, column=0, sticky="w")
entry_s = tk.Entry(frame_atak, width=10)
entry_s.grid(row=0, column=1); entry_s.insert(0, "3") # Np. Łucznik

tk.Label(frame_atak, text="HP jednostki:").grid(row=1, column=0, sticky="w")
entry_a_hp = tk.Entry(frame_atak, width=10)
entry_a_hp.grid(row=1, column=1); entry_a_hp.insert(0, "10")

tk.Label(frame_atak, text="Siła Ognia (FP):").grid(row=2, column=0, sticky="w")
entry_a_fp = tk.Entry(frame_atak, width=10)
entry_a_fp.grid(row=2, column=1); entry_a_fp.insert(0, "1")

# Ramka Obrońcy
frame_obrona = tk.LabelFrame(root, text="Parametry Obrońcy (Ufortyfikowany Cel)", padx=10, pady=10)
frame_obrona.pack(fill="x", padx=10, pady=5)

tk.Label(frame_obrona, text="Siła Obrony:").grid(row=0, column=0, sticky="w")
entry_r = tk.Entry(frame_obrona, width=10)
entry_r.grid(row=0, column=1); entry_r.insert(0, "6") # Np. Falanga (2) * Miasto (1.5) * Fort (2)

tk.Label(frame_obrona, text="Początkowe HP:").grid(row=1, column=0, sticky="w")
entry_d_hp = tk.Entry(frame_obrona, width=10)
entry_d_hp.grid(row=1, column=1); entry_d_hp.insert(0, "10")

tk.Label(frame_obrona, text="Siła Ognia (FP):").grid(row=2, column=0, sticky="w")
entry_d_fp = tk.Entry(frame_obrona, width=10)
entry_d_fp.grid(row=2, column=1); entry_d_fp.insert(0, "1")

# Przycisk
btn_oblicz = tk.Button(root, text="Symuluj Fale Ataków", command=uruchom_symulacje_oblężenia, bg="#ffcccb", font=("Arial", 10, "bold"))
btn_oblicz.pack(pady=10)

# Okno Wyników
frame_wynik = tk.LabelFrame(root, text="Przebieg Oblężenia", padx=10, pady=10)
frame_wynik.pack(fill="both", expand=True, padx=10, pady=5)

text_wynik = tk.Text(frame_wynik, height=15, width=50, state=tk.DISABLED, bg="#2b2b2b", fg="#00ff00", font=("Consolas", 9))
text_wynik.pack()

root.mainloop()
