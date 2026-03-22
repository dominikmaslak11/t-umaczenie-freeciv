import math

# Funkcja pomocnicza: Dystrybuanta standardowego rozkładu normalnego (Phi)
def phi(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def symuluj_walke_freeciv_ze_stratami(s, r, a_hp, d_hp, a_fp, d_fp):
    print("--- ROZPOCZĘCIE ANALIZY STARCIA ---")
    print(f"Atakujący: Siła={s}, HP={a_hp}, Siła ognia={a_fp}")
    print(f"Obrońca:   Siła={r}, HP={d_hp}, Siła ognia={d_fp}\n")

    # KROK 1: Prawdopodobieństwo w pojedynczej rundzie
    p = s / (s + r)
    q = 1.0 - p
    print("KROK 1: Prawdopodobieństwo w pojedynczej rundzie")
    print(f"  Atakujący (p): {p:.4f} ({p*100:.1f}%) | Obrońca (q): {q:.4f} ({q*100:.1f}%)\n")

    # KROK 2: Wymagane udane trafienia (zaokrąglone w górę)
    k = math.ceil(d_hp / a_fp)  # Ile razy musi trafić atakujący
    l = math.ceil(a_hp / d_fp)  # Ile razy musi trafić obrońca
    print("KROK 2: Wymagane udane trafienia do zabicia przeciwnika")
    print(f"  Atakujący musi trafić: {k} razy. Obrońca musi trafić: {l} razy.\n")

    # KROK 3: Maksymalna długość walki
    md = k + l - 1

    # KROK 4: Dokładny wynik starcia (Model Dwumianowy)
    dokladne_prawd_wygranej_atakujacego = 0.0
    for i in range(k, md + 1):
        szansa = math.comb(md, i) * (p**i) * (q**(md - i))
        dokladne_prawd_wygranej_atakujacego += szansa
        
    prawd_wygranej_obroncy = 1.0 - dokladne_prawd_wygranej_atakujacego

    print("KROK 3 & 4: Szanse na ostateczne zwycięstwo")
    print(f"  Zwycięstwo Atakującego: {dokladne_prawd_wygranej_atakujacego*100:.2f}%")
    print(f"  Zwycięstwo Obrońcy:     {prawd_wygranej_obroncy*100:.2f}%\n")

    # KROK 5: Przewidywanie strat (Oczekiwane HP po walce)
    print("KROK 5: Przewidywane straty (ile HP zostanie zwycięzcy)")
    
    # --- Analiza dla wygranej ATAKUJĄCEGO ---
    oczekiwane_hp_atakujacego = 0.0
    print("  Jeśli wygra ATAKUJĄCY:")
    # Atakujący wygrywa, co oznacza, że otrzymał od 0 do l-1 ciosów (oznaczmy jako 'd')
    for d in range(l):
        # Wzór na wygraną w dokładnie (k+d) rundach: combinacje(k-1+d, d) * p^k * q^d
        prawd_scenariusza = math.comb(k - 1 + d, d) * (p**k) * (q**d)
        pozostale_hp = a_hp - (d * d_fp)
        
        if dokladne_prawd_wygranej_atakujacego > 0:
            # Obliczamy szansę warunkową (szansa tego scenariusza względem wszystkich scenariuszy wygranej)
            szansa_warunkowa = prawd_scenariusza / dokladne_prawd_wygranej_atakujacego
            oczekiwane_hp_atakujacego += pozostale_hp * szansa_warunkowa
            
    print(f"    Średnio zostanie mu: {oczekiwane_hp_atakujacego:.1f} / {a_hp} HP")

    # --- Analiza dla wygranej OBROŃCY ---
    oczekiwane_hp_obroncy = 0.0
    print("  Jeśli wygra OBROŃCA:")
    # Obrońca wygrywa, czyli otrzymał od 0 do k-1 ciosów (oznaczmy jako 'a')
    for a in range(k):
        # Obrońca trafia 'l' razy, atakujący 'a' razy. Wzór: combinacje(l-1+a, a) * q^l * p^a
        prawd_scenariusza = math.comb(l - 1 + a, a) * (q**l) * (p**a)
        pozostale_hp = d_hp - (a * a_fp)
        
        if prawd_wygranej_obroncy > 0:
            szansa_warunkowa = prawd_scenariusza / prawd_wygranej_obroncy
            oczekiwane_hp_obroncy += pozostale_hp * szansa_warunkowa
            
    print(f"    Średnio zostanie mu: {oczekiwane_hp_obroncy:.1f} / {d_hp} HP\n")

    # Podsumowanie z uwzględnieniem kondycji zwycięzcy
    if dokladne_prawd_wygranej_atakujacego > 0.6:
        if oczekiwane_hp_atakujacego / a_hp > 0.5:
            werdykt = "Pewny atak z dużą szansą na przetrwanie w dobrym zdrowiu."
        else:
            werdykt = "Atakujący wygra, ale najpewniej będzie ciężko ranny (podatny na kontratak)."
    elif dokladne_prawd_wygranej_atakujacego > 0.4:
        werdykt = "Starcie wyrównane. Zwycięzca (ktokolwiek nim będzie) wyjdzie z tego ledwo żywy."
    else:
        werdykt = "Ryzykowny atak. Jeśli obrońca przeżyje, zachowa sporo sił."
        
    print(f"WERDYKT TAKTYCZNY: {werdykt}")


# --- PRZYKŁAD UŻYCIA ---
# Załóżmy walkę doświadczonego oddziału (Weteran, Siła Ataku = 4, HP = 20, Siła ognia = 2)
# przeciwko standardowej obronie (Siła Obrony = 3, HP = 10, Siła ognia = 1)

symuluj_walke_freeciv_ze_stratami(s=4, r=3, a_hp=20, d_hp=10, a_fp=2, d_fp=1)
