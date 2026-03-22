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

# --- LOGIKA MATEMATYCZNA (Łańcuchy Markowa) ---
def oblicz_fale_atakow(s, r, a_hp, d_hp, a_fp, d_fp):
    p = s / (s + r)
    q = 1.0 - p
    
    probs = {h: 0.0 for h in range(d_hp + 1)}
    probs[d_hp] = 1.0
    wyniki = []
    
    for fala in range(1, 21):
        nowe_probs = {h: 0.0 for h in range(d_hp + 1)}
        nowe_probs[0] = probs[0]
        
        for h, prob_h in probs.items():
            if h == 0 or prob_h == 0:
                continue
            
            k = math.ceil(h / a_fp)
            l = math.ceil(a_hp / d_fp)
            md = k + l - 1
            
            prawd_wygranej_atakujacego = sum(
                math.comb(md, i) * (p**i) * (q**(md - i)) for i in range(k, md + 1)
            )
            nowe_probs[0] += prob_h * prawd_wygranej_atakujacego
            
            for a in range(k):
                prawd_scenariusza = math.comb(l - 1 + a, a) * (p**a) * (q**l)
                nowe_hp = max(1, h - (a * a_fp))
                nowe_probs[nowe_hp] += prob_h * prawd_scenariusza
                
        probs = nowe_probs
        szansa_zabicia = probs[0]
        wyniki.append((fala, szansa_zabicia))
        
        if szansa_zabicia > 0.995:
            break
            
    return wyniki

# --- INTERFEJS GRAFICZNY (GUI) ---
def uruchom_symulacje():
    try:
        # Pobranie wartości bazowych
        bazowy_s = float(entry_s.get())
        a_hp = int(entry_a_hp.get())
        a_fp = int(entry_a_fp.get())
        
        bazowy_r = float(entry_r.get())
        d_hp = int(entry_d_hp.get())
        d_fp = int(entry_d_fp.get())
        
        # Walidacja
        if any(val <= 0 for val in [bazowy_s, bazowy_r, a_hp, d_hp, a_fp, d_fp]):
            messagebox.showerror("Błąd", "Wartości bazowe muszą być > 0.")
            return
            
        # Obliczanie ostatecznej Siły Ataku
        mnożnik_atak = WETERAN_MOD[combo_a_wet.get()]
        finalny_s = bazowy_s * mnożnik_atak
        
        # Obliczanie ostatecznej Siły Obrony
        mnożnik_obrona = WETERAN_MOD[combo_d_wet.get()]
        mnożnik_teren = TEREN_MOD[combo_d_teren.get()]
        mnożnik_struktura = STRUKTURA_MOD[combo_d_struktura.get()]
        
        finalny_r = bazowy_r * mnożnik_obrona * mnożnik_teren * mnożnik_struktura
        if var_rzeka.get():
            finalny_r *= 1.5
        if var_okopanie.get():
            finalny_r *= 1.5
            
        # Uruchomienie symulacji na obliczonych statystykach
        wyniki = oblicz_fale_atakow(finalny_s, finalny_r, a_hp, d_hp, a_fp, d_fp)
        
        # Generowanie raportu
        text_wynik.config(state=tk.NORMAL)
        text_wynik.delete(1.0, tk.END)
        
        text_wynik.insert(tk.END, f"OSTATECZNE STATYSTYKI PO MODYFIKATORACH:\n")
        text_wynik.insert(tk.END, f"Atak: {finalny_s:.2f}  vs  Obrona: {finalny_r:.2f}\n")
        text_wynik.insert(tk.END, "-"*45 + "\n")
        
        rekomendacja = 0
        for fala, szansa in wyniki:
            procent = szansa * 100
            pasek_postepu = "█" * int(procent / 5) + "░" * (20 - int(procent / 5))
            text_wynik.insert(tk.END, f"{fala:2d} ataków: [{pasek_postepu}] {procent:>5.1f}%\n")
            
            if procent >= 90.0 and rekomendacja == 0:
                rekomendacja = fala
                
        text_wynik.insert(tk.END, "-"*45 + "\n")
        if rekomendacja > 0:
            text_wynik.insert(tk.END, f"WERDYKT: Potrzebujesz ok. {rekomendacja} jednostek na sukces.\n")
        else:
            text_wynik.insert(tk.END, "WERDYKT: Pozycja nie do zdobycia!\n")
            
        text_wynik.config(state=tk.DISABLED)
        
    except ValueError:
        messagebox.showerror("Błąd", "Sprawdź, czy wpisano poprawne liczby.")

# --- INICJALIZACJA OKNA ---
root = tk.Tk()
root.title("Kalkulator Zaawansowany Freeciv")
root.geometry("500x750")

# --- RAMKA ATAKUJĄCEGO ---
frame_atak = tk.LabelFrame(root, text="Atakujący (Podaj bazowe wartości przed mnożnikami)", padx=10, pady=5)
frame_atak.pack(fill="x", padx=10, pady=5)

tk.Label(frame_atak, text="Bazowa Siła Ataku:").grid(row=0, column=0, sticky="w")
entry_s = tk.Entry(frame_atak, width=10); entry_s.grid(row=0, column=1); entry_s.insert(0, "3")

tk.Label(frame_atak, text="HP / Siła Ognia (FP):").grid(row=1, column=0, sticky="w")
entry_a_hp = tk.Entry(frame_atak, width=5); entry_a_hp.grid(row=1, column=1, sticky="w"); entry_a_hp.insert(0, "10")
entry_a_fp = tk.Entry(frame_atak, width=5); entry_a_fp.grid(row=1, column=1, sticky="e"); entry_a_fp.insert(0, "1")

tk.Label(frame_atak, text="Doświadczenie:").grid(row=2, column=0, sticky="w")
combo_a_wet = ttk.Combobox(frame_atak, values=list(WETERAN_MOD.keys()), state="readonly", width=20)
combo_a_wet.grid(row=2, column=1, pady=2); combo_a_wet.current(0)

# --- RAMKA OBROŃCY ---
frame_obrona = tk.LabelFrame(root, text="Obrońca (Podaj bazowe wartości przed mnożnikami)", padx=10, pady=5)
frame_obrona.pack(fill="x", padx=10, pady=5)

tk.Label(frame_obrona, text="Bazowa Siła Obrony:").grid(row=0, column=0, sticky="w")
entry_r = tk.Entry(frame_obrona, width=10); entry_r.grid(row=0, column=1); entry_r.insert(0, "2")

tk.Label(frame_obrona, text="HP / Siła Ognia (FP):").grid(row=1, column=0, sticky="w")
entry_d_hp = tk.Entry(frame_obrona, width=5); entry_d_hp.grid(row=1, column=1, sticky="w"); entry_d_hp.insert(0, "10")
entry_d_fp = tk.Entry(frame_obrona, width=5); entry_d_fp.grid(row=1, column=1, sticky="e"); entry_d_fp.insert(0, "1")

tk.Label(frame_obrona, text="Doświadczenie:").grid(row=2, column=0, sticky="w")
combo_d_wet = ttk.Combobox(frame_obrona, values=list(WETERAN_MOD.keys()), state="readonly", width=20)
combo_d_wet.grid(row=2, column=1, pady=2); combo_d_wet.current(0)

tk.Label(frame_obrona, text="Teren bazowy:").grid(row=3, column=0, sticky="w")
combo_d_teren = ttk.Combobox(frame_obrona, values=list(TEREN_MOD.keys()), state="readonly", width=20)
combo_d_teren.grid(row=3, column=1, pady=2); combo_d_teren.current(0)

tk.Label(frame_obrona, text="Struktura obronna:").grid(row=4, column=0, sticky="w")
combo_d_struktura = ttk.Combobox(frame_obrona, values=list(STRUKTURA_MOD.keys()), state="readonly", width=20)
combo_d_struktura.grid(row=4, column=1, pady=2); combo_d_struktura.current(0)

var_rzeka = tk.BooleanVar()
tk.Checkbutton(frame_obrona, text="Za rzeką (x1.5)", variable=var_rzeka).grid(row=5, column=0, sticky="w")

var_okopanie = tk.BooleanVar()
tk.Checkbutton(frame_obrona, text="Okopany lub w Mieście (x1.5)", variable=var_okopanie).grid(row=5, column=1, sticky="w")

# --- PRZYCISK ---
btn_oblicz = tk.Button(root, text="Kalkuluj Fale Ataków", command=uruchom_symulacje, bg="#ffcccb", font=("Arial", 10, "bold"))
btn_oblicz.pack(pady=10)

# --- PANEL WYNIKÓW ---
frame_wynik = tk.LabelFrame(root, text="Symulacja Przebiegu Oblężenia", padx=10, pady=5)
frame_wynik.pack(fill="both", expand=True, padx=10, pady=5)

text_wynik = tk.Text(frame_wynik, height=14, width=52, state=tk.DISABLED, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 9))
text_wynik.pack()

root.mainloop()
