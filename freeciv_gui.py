import tkinter as tk
from tkinter import messagebox
import math

# --- LOGIKA MATEMATYCZNA (Z poprzedniego kroku) ---
def oblicz_wynik_walki(s, r, a_hp, d_hp, a_fp, d_fp):
    raport = ""
    
    p = s / (s + r)
    q = 1.0 - p
    k = math.ceil(d_hp / a_fp)
    l = math.ceil(a_hp / d_fp)
    md = k + l - 1

    # Dokładne prawdopodobieństwo wygranej atakującego (rozkład dwumianowy)
    prawd_wygranej_atakujacego = 0.0
    for i in range(k, md + 1):
        szansa = math.comb(md, i) * (p**i) * (q**(md - i))
        prawd_wygranej_atakujacego += szansa
        
    prawd_wygranej_obroncy = 1.0 - prawd_wygranej_atakujacego

    # Przewidywane HP po walce - Atakujący
    oczekiwane_hp_atakujacego = 0.0
    for d in range(l):
        prawd_scenariusza = math.comb(k - 1 + d, d) * (p**k) * (q**d)
        pozostale_hp = a_hp - (d * d_fp)
        if prawd_wygranej_atakujacego > 0:
            oczekiwane_hp_atakujacego += pozostale_hp * (prawd_scenariusza / prawd_wygranej_atakujacego)

    # Przewidywane HP po walce - Obrońca
    oczekiwane_hp_obroncy = 0.0
    for a in range(k):
        prawd_scenariusza = math.comb(l - 1 + a, a) * (q**l) * (p**a)
        pozostale_hp = d_hp - (a * a_fp)
        if prawd_wygranej_obroncy > 0:
            oczekiwane_hp_obroncy += pozostale_hp * (prawd_scenariusza / prawd_wygranej_obroncy)

    # Generowanie raportu tekstowego
    raport += "--- SZANSE NA ZWYCIĘSTWO ---\n"
    raport += f"Atakujący: {prawd_wygranej_atakujacego*100:.2f}%\n"
    raport += f"Obrońca:   {prawd_wygranej_obroncy*100:.2f}%\n\n"
    
    raport += "--- PRZEWIDYWANE STRATY ---\n"
    raport += f"Jeśli wygra Atakujący, zostanie mu średnio: {oczekiwane_hp_atakujacego:.1f} / {a_hp} HP\n"
    raport += f"Jeśli wygra Obrońca, zostanie mu średnio: {oczekiwane_hp_obroncy:.1f} / {d_hp} HP\n\n"
    
    raport += "--- WERDYKT TAKTYCZNY ---\n"
    if prawd_wygranej_atakujacego > 0.6:
        if oczekiwane_hp_atakujacego / a_hp > 0.5:
            raport += "Pewny atak. Atakujący powinien przetrwać w dobrym stanie."
        else:
            raport += "Atakujący wygra, ale najpewniej będzie ciężko ranny."
    elif prawd_wygranej_atakujacego > 0.4:
        raport += "Starcie wyrównane. Zwycięzca wyjdzie z tego ledwo żywy."
    else:
        raport += "Ryzykowny atak. Obrońca prawdopodobnie odeprze szturm."

    return raport

# --- INTERFEJS GRAFICZNY (GUI) ---
def uruchom_kalkulator():
    # Pobieranie danych z pól tekstowych
    try:
        s = float(entry_s.get())
        a_hp = int(entry_a_hp.get())
        a_fp = int(entry_a_fp.get())
        
        r = float(entry_r.get())
        d_hp = int(entry_d_hp.get())
        d_fp = int(entry_d_fp.get())
        
        # Zabezpieczenie przed wartościami zerowymi lub ujemnymi
        if any(val <= 0 for val in [s, r, a_hp, d_hp, a_fp, d_fp]):
            messagebox.showerror("Błąd", "Wszystkie wartości muszą być większe od 0.")
            return
            
        # Obliczenia
        raport = oblicz_wynik_walki(s, r, a_hp, d_hp, a_fp, d_fp)
        
        # Wyświetlenie wyniku w polu tekstowym
        text_wynik.config(state=tk.NORMAL)
        text_wynik.delete(1.0, tk.END)
        text_wynik.insert(tk.END, raport)
        text_wynik.config(state=tk.DISABLED)
        
    except ValueError:
        messagebox.showerror("Błąd", "Proszę wprowadzić poprawne wartości liczbowe.")

# Tworzenie głównego okna
root = tk.Tk()
root.title("Kalkulator Taktyczny Freeciv")
root.geometry("400x550")
root.resizable(False, False)

# Ramka dla Atakującego
frame_atak = tk.LabelFrame(root, text="Parametry Atakującego", padx=10, pady=10)
frame_atak.pack(fill="x", padx=10, pady=5)

tk.Label(frame_atak, text="Siła Ataku (po modyfikatorach):").grid(row=0, column=0, sticky="w")
entry_s = tk.Entry(frame_atak, width=10)
entry_s.grid(row=0, column=1)
entry_s.insert(0, "3")

tk.Label(frame_atak, text="Punkty Życia (HP):").grid(row=1, column=0, sticky="w")
entry_a_hp = tk.Entry(frame_atak, width=10)
entry_a_hp.grid(row=1, column=1)
entry_a_hp.insert(0, "10")

tk.Label(frame_atak, text="Siła Ognia (Firepower):").grid(row=2, column=0, sticky="w")
entry_a_fp = tk.Entry(frame_atak, width=10)
entry_a_fp.grid(row=2, column=1)
entry_a_fp.insert(0, "1")

# Ramka dla Obrońcy
frame_obrona = tk.LabelFrame(root, text="Parametry Obrońcy", padx=10, pady=10)
frame_obrona.pack(fill="x", padx=10, pady=5)

tk.Label(frame_obrona, text="Siła Obrony (po modyfikatorach):").grid(row=0, column=0, sticky="w")
entry_r = tk.Entry(frame_obrona, width=10)
entry_r.grid(row=0, column=1)
entry_r.insert(0, "2")

tk.Label(frame_obrona, text="Punkty Życia (HP):").grid(row=1, column=0, sticky="w")
entry_d_hp = tk.Entry(frame_obrona, width=10)
entry_d_hp.grid(row=1, column=1)
entry_d_hp.insert(0, "10")

tk.Label(frame_obrona, text="Siła Ognia (Firepower):").grid(row=2, column=0, sticky="w")
entry_d_fp = tk.Entry(frame_obrona, width=10)
entry_d_fp.grid(row=2, column=1)
entry_d_fp.insert(0, "1")

# Przycisk Oblicz
btn_oblicz = tk.Button(root, text="Oblicz Szanse", command=uruchom_kalkulator, bg="lightblue", font=("Arial", 10, "bold"))
btn_oblicz.pack(pady=10)

# Ramka na wyniki
frame_wynik = tk.LabelFrame(root, text="Raport z pola bitwy", padx=10, pady=10)
frame_wynik.pack(fill="both", expand=True, padx=10, pady=5)

text_wynik = tk.Text(frame_wynik, height=12, width=45, state=tk.DISABLED, bg="#f0f0f0", font=("Consolas", 9))
text_wynik.pack()

# Uruchomienie pętli zdarzeń aplikacji
root.mainloop()
