import tkinter as tk
from tkinter import ttk, messagebox
import math

# --- SŁOWNIKI MODYFIKATORÓW ---
WETERAN_MOD = {
    "Początkujący (x1.0)": 1.0,
    "Weteran (x1.5)": 1.5,
    "Doświadczony (x1.75)": 1.75,
    "Elitarny (x2.0)": 2.0
}

TEREN_MOD = {
    "Płaski / Ocean (x1.0)": 1.0,
    "Las / Dżungla / Bagno (x1.5)": 1.5,
    "Wzgórza (x2.0)": 2.0,
    "Góry (x3.0)": 3.0
}

STRUKTURA_MOD = {
    "Brak (x1.0)": 1.0,
    "Forteca (x2.0)": 2.0,
    "Mury Miejskie (x3.0)": 3.0
}

# --- LOGIKA MATEMATYCZNA (Łańcuchy Markowa + Bombardowanie) ---
def oblicz_fale_atakow(s, r, a_hp, d_hp, a_fp, d_fp, is_bombard, bombard_rate):
    p = s / (s + r)
    q = 1.0 - p
    
    probs = {h: 0.0 for h in range(d_hp + 1)}
    probs[d_hp] = 1.0
    wyniki = []
    
    for fala in range(1, 21):
        nowe_probs = {h: 0.0 for h in range(d_hp + 1)}
        nowe_probs[0] = probs[0] # Martwi pozostają martwi
        
        for h, prob_h in probs.items():
            if h == 0 or prob_h == 0:
                continue
                
            if is_bombard:
                # TRYB BOMBARDOWANIA: Atakujący nie obrywa, obrońca dostaje obrażenia, ale max do 1 HP
                for a in range(bombard_rate + 1):
                    # Rozkład dwumianowy trafień artylerii
                    prawd_trafienia = math.comb(bombard_rate, a) * (p**a) * (q**(bombard_rate - a))
                    nowe_hp = max(1, h - (a * a_fp)) # Nie może spaść poniżej 1 HP
                    nowe_probs[nowe_hp] += prob_h * prawd_trafienia
            else:
                # TRYB STANDARDOWY (Walka w zwarciu)
                k = math.ceil(h / a_fp)
                l = math.ceil(a_hp / d_fp)
                md = k + l - 1
                
                # Atakujący wygrywa
                prawd_wygranej_atakujacego = sum(
                    math.comb(md, i) * (p**i) * (q**(md - i)) for i in range(k, md + 1)
                )
                nowe_probs[0] += prob_h * prawd_wygranej_atakujacego
                
                # Obrońca wygrywa (atakujący ginie, obrońca traci HP)
                for a in range(k):
                    prawd_scenariusza = math.comb(l - 1 + a, a) * (p**a) * (q**l)
                    nowe_hp = max(1, h - (a * a_fp))
                    nowe_probs[nowe_hp] += prob_h * prawd_scenariusza
                
        probs = nowe_probs
        
        if is_bombard:
            # Dla bombardowania zbieramy oczekiwane (średnie) HP obrońcy
            oczekiwane_hp = sum(stan_hp * prawd for stan_hp, prawd in probs.items())
            wyniki.append((fala, oczekiwane_hp))
            if oczekiwane_hp <= 1.05: # Prawie 1 HP - koniec sensu bombardowania
                break
        else:
            szansa_zabicia = probs[0]
            wyniki.append((fala, szansa_zabicia))
            if szansa_zabicia > 0.995:
                break
            
    return wyniki

# --- INTERFEJS GRAFICZNY (GUI) ---
def uruchom_symulacje():
    try:
        bazowy_s = float(entry_s.get())
        a_hp = int(entry_a_hp.get())
        a_fp = int(entry_a_fp.get())
        a_koszt = int(entry_a_koszt.get())
        is_bombard = var_bombard.get()
        bombard_rate = int(entry_bombard_rate.get())
        
        bazowy_r = float(entry_r.get())
        d_hp = int(entry_d_hp.get())
        d_fp = int(entry_d_fp.get())
        d_koszt = int(entry_d_koszt.get())
        
        if any(val <= 0 for val in [bazowy_s, bazowy_r, a_hp, d_hp, a_fp, d_fp, a_koszt, d_koszt, bombard_rate]):
            messagebox.showerror("Błąd", "Wartości muszą być > 0.")
            return
            
        finalny_s = bazowy_s * WETERAN_MOD[combo_a_wet.get()]
        finalny_r = bazowy_r * WETERAN_MOD[combo_d_wet.get()] * TEREN_MOD[combo_d_teren.get()] * STRUKTURA_MOD[combo_d_struktura.get()]
        if var_rzeka.get(): finalny_r *= 1.5
        if var_okopanie.get(): finalny_r *= 1.5
            
        wyniki = oblicz_fale_atakow(finalny_s, finalny_r, a_hp, d_hp, a_fp, d_fp, is_bombard, bombard_rate)
        
        text_wynik.config(state=tk.NORMAL)
        text_wynik.delete(1.0, tk.END)
        text_wynik.insert(tk.END, f"Atak: {finalny_s:.2f}  vs  Obrona: {finalny_r:.2f}\n")
        text_wynik.insert(tk.END, "-"*45 + "\n")
        
        if is_bombard:
            # Wypisywanie wyników dla Bombardowania
            text_wynik.insert(tk.END, "TRYB BOMBARDOWANIA (Brak strat własnych, cel max do 1 HP)\n")
            rekomendacja = 0
            for fala, oczekiwane_hp in wyniki:
                procent_zdrowia = (oczekiwane_hp / d_hp) * 100
                pasek_postepu = "█" * int(procent_zdrowia / 5) + "░" * (20 - int(procent_zdrowia / 5))
                text_wynik.insert(tk.END, f"{fala:2d} salw: [{pasek_postepu}] Śr. {oczekiwane_hp:.1f} HP\n")
                if oczekiwane_hp <= 1.5 and rekomendacja == 0:
                    rekomendacja = fala
                    
            text_wynik.insert(tk.END, "-"*45 + "\n")
            if rekomendacja > 0:
                text_wynik.insert(tk.END, f"WERDYKT: Po {rekomendacja} bombardowaniach obrońca będzie "
                                          f"na skraju śmierci (1 HP).\nWyślij jednostkę lądową, by go dobić.\n")
            else:
                text_wynik.insert(tk.END, "WERDYKT: Będziesz potrzebować gigantycznego ostrzału.\n")
            text_wynik.insert(tk.END, f"KOSZT: 0 straconych tarcz (tracisz tylko czas/tury).\n")
            
        else:
            # Wypisywanie wyników dla Ataku Standardowego
            rekomendacja = 0
            for fala, szansa in wyniki:
                procent = szansa * 100
                pasek_postepu = "█" * int(procent / 5) + "░" * (20 - int(procent / 5))
                text_wynik.insert(tk.END, f"{fala:2d} ataków: [{pasek_postepu}] {procent:>5.1f}% na zabicie\n")
                if procent >= 90.0 and rekomendacja == 0:
                    rekomendacja = fala
                    
            text_wynik.insert(tk.END, "-"*45 + "\n")
            if rekomendacja > 0:
                koszt_calkowity = rekomendacja * a_koszt
                text_wynik.insert(tk.END, f"WERDYKT: Potrzebujesz ok. {rekomendacja} jednostek na sukces.\n")
                text_wynik.insert(tk.END, f"KOSZT: Zaryzykujesz {koszt_calkowity} tarcz za cel wart {d_koszt} tarcz.\n")
            else:
                text_wynik.insert(tk.END, "WERDYKT: Pozycja nie do zdobycia!\n")
                
        text_wynik.config(state=tk.DISABLED)
        
    except ValueError:
        messagebox.showerror("Błąd", "Sprawdź, czy wpisano poprawne liczby.")

def toggle_bombard_rate():
    if var_bombard.get():
        entry_bombard_rate.config(state=tk.NORMAL)
    else:
        entry_bombard_rate.config(state=tk.DISABLED)

# --- INICJALIZACJA OKNA ---
root = tk.Tk()
root.title("Kalkulator Dowódcy Freeciv - Edycja Artyleryjska")
root.geometry("520x860")

# --- RAMKA ATAKUJĄCEGO ---
frame_atak = tk.LabelFrame(root, text="Atakujący / Artyleria", padx=10, pady=5)
frame_atak.pack(fill="x", padx=10, pady=5)

tk.Label(frame_atak, text="Bazowa Siła Ataku:").grid(row=0, column=0, sticky="w")
entry_s = tk.Entry(frame_atak, width=10); entry_s.grid(row=0, column=1); entry_s.insert(0, "3")

tk.Label(frame_atak, text="HP / Siła Ognia (FP):").grid(row=1, column=0, sticky="w")
entry_a_hp = tk.Entry(frame_atak, width=5); entry_a_hp.grid(row=1, column=1, sticky="w"); entry_a_hp.insert(0, "10")
entry_a_fp = tk.Entry(frame_atak, width=5); entry_a_fp.grid(row=1, column=1, sticky="e"); entry_a_fp.insert(0, "1")

tk.Label(frame_atak, text="Koszt w tarczach:").grid(row=2, column=0, sticky="w")
entry_a_koszt = tk.Entry(frame_atak, width=10); entry_a_koszt.grid(row=2, column=1); entry_a_koszt.insert(0, "30")

tk.Label(frame_atak, text="Doświadczenie:").grid(row=3, column=0, sticky="w")
combo_a_wet = ttk.Combobox(frame_atak, values=list(WETERAN_MOD.keys()), state="readonly", width=20)
combo_a_wet.grid(row=3, column=1, pady=2); combo_a_wet.current(0)

# OPCJE BOMBARDOWANIA
frame_bombard = tk.Frame(frame_atak)
frame_bombard.grid(row=4, column=0, columnspan=2, sticky="w", pady=5)
var_bombard = tk.BooleanVar()
tk.Checkbutton(frame_bombard, text="Tryb Bombardowania (bez strat własnych)", variable=var_bombard, command=toggle_bombard_rate, fg="red").pack(side=tk.LEFT)

tk.Label(frame_atak, text="Rate (Rundy Bombardowania):").grid(row=5, column=0, sticky="w")
entry_bombard_rate = tk.Entry(frame_atak, width=10, state=tk.DISABLED)
entry_bombard_rate.grid(row=5, column=1, sticky="w")
entry_bombard_rate.insert(0, "2") # Domyślnie 2 rundy bombardowania na jednostkę

# --- RAMKA OBROŃCY ---
frame_obrona = tk.LabelFrame(root, text="Obrońca", padx=10, pady=5)
frame_obrona.pack(fill="x", padx=10, pady=5)

tk.Label(frame_obrona, text="Bazowa Siła Obrony:").grid(row=0, column=0, sticky="w")
entry_r = tk.Entry(frame_obrona, width=10); entry_r.grid(row=0, column=1); entry_r.insert(0, "2")

tk.Label(frame_obrona, text="Początkowe HP / Siła Ognia:").grid(row=1, column=0, sticky="w")
entry_d_hp = tk.Entry(frame_obrona, width=5); entry_d_hp.grid(row=1, column=1, sticky="w"); entry_d_hp.insert(0, "10")
entry_d_fp = tk.Entry(frame_obrona, width=5); entry_d_fp.grid(row=1, column=1, sticky="e"); entry_d_fp.insert(0, "1")

tk.Label(frame_obrona, text="Koszt w tarczach:").grid(row=2, column=0, sticky="w")
entry_d_koszt = tk.Entry(frame_obrona, width=10); entry_d_koszt.grid(row=2, column=1); entry_d_koszt.insert(0, "20")

tk.Label(frame_obrona, text="Doświadczenie:").grid(row=3, column=0, sticky="w")
combo_d_wet = ttk.Combobox(frame_obrona, values=list(WETERAN_MOD.keys()), state="readonly", width=20)
combo_d_wet.grid(row=3, column=1, pady=2); combo_d_wet.current(0)

tk.Label(frame_obrona, text="Teren bazowy:").grid(row=4, column=0, sticky="w")
combo_d_teren = ttk.Combobox(frame_obrona, values=list(TEREN_MOD.keys()), state="readonly", width=20)
combo_d_teren.grid(row=4, column=1, pady=2); combo_d_teren.current(0)

tk.Label(frame_obrona, text="Struktura obronna:").grid(row=5, column=0, sticky="w")
combo_d_struktura = ttk.Combobox(frame_obrona, values=list(STRUKTURA_MOD.keys()), state="readonly", width=20)
combo_d_struktura.grid(row=5, column=1, pady=2); combo_d_struktura.current(0)

var_rzeka = tk.BooleanVar()
tk.Checkbutton(frame_obrona, text="Za rzeką (x1.5)", variable=var_rzeka).grid(row=6, column=0, sticky="w")

var_okopanie = tk.BooleanVar()
tk.Checkbutton(frame_obrona, text="Okopany / Miasto (x1.5)", variable=var_okopanie).grid(row=6, column=1, sticky="w")

# --- PRZYCISK ---
btn_oblicz = tk.Button(root, text="Uruchom Symulację Dowódczą", command=uruchom_symulacje, bg="#ffcccb", font=("Arial", 10, "bold"))
btn_oblicz.pack(pady=10)

# --- PANEL WYNIKÓW ---
frame_wynik = tk.LabelFrame(root, text="Raport Taktyczny", padx=10, pady=5)
frame_wynik.pack(fill="both", expand=True, padx=10, pady=5)

text_wynik = tk.Text(frame_wynik, height=18, width=58, state=tk.DISABLED, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 9))
text_wynik.pack()

root.mainloop()
