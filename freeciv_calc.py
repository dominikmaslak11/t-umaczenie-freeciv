import math

# Funkcja pomocnicza: Dystrybuanta standardowego rozkładu normalnego (Phi)
# Używamy jej do aproksymacji bez konieczności importowania zewnętrznych bibliotek (jak scipy).
def phi(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def symuluj_walke_freeciv(s, r, a_hp, d_hp, a_fp, d_fp):
    print("--- ROZPOCZĘCIE ANALIZY STARCIA ---")
    print(f"Atakujący: Siła={s}, HP={a_hp}, Siła ognia={a_fp}")
    print(f"Obrońca:   Siła={r}, HP={d_hp}, Siła ognia={d_fp}\n")

    # KROK 1: Obliczenie prawdopodobieństwa wygrania pojedynczej rundy (p i q)
    p = s / (s + r)
    q = 1.0 - p
    print("KROK 1: Prawdopodobieństwo w pojedynczej rundzie")
    print(f"  Szansa na trafienie przez atakującego (p): {p:.4f} ({p*100:.1f}%)")
    print(f"  Szansa na trafienie przez obrońcę (q): {q:.4f} ({q*100:.1f}%)\n")

    # KROK 2: Obliczenie ile udanych trafień (wygranych rund) potrzeba do zabicia przeciwnika
    # Używamy math.ceil (zaokrąglenie w górę), ponieważ ułamek trafienia nadal wymaga pełnego ciosu.
    k = math.ceil(d_hp / a_fp)
    l = math.ceil(a_hp / d_fp)
    print("KROK 2: Wymagane udane trafienia")
    print(f"  Atakujący musi trafić (k): {k} razy, aby zniszczyć obrońcę.")
    print(f"  Obrońca musi trafić (l): {l} razy, aby zniszczyć atakującego.\n")

    # KROK 3: Maksymalna możliwa liczba rund w starciu
    # Starcie musi się skończyć, zanim obie jednostki zadadzą sobie śmiertelny cios jednocześnie.
    md = k + l - 1
    print("KROK 3: Długość walki")
    print(f"  Maksymalna liczba rund (md): {md}\n")

    # KROK 4: DOKŁADNY MODEL MATEMATYCZNY (Rozkład Dwumianowy)
    # Sumujemy prawdopodobieństwa wszystkich scenariuszy, w których atakujący
    # wygrywa co najmniej 'k' rund z 'md' dostępnych.
    dokladne_prawdopodobienstwo = 0.0
    for i in range(k, md + 1):
        # math.comb(md, i) to symbol Newtona: "md po i"
        scenariusz_szansa = math.comb(md, i) * (p**i) * (q**(md - i))
        dokladne_prawdopodobienstwo += scenariusz_szansa
    
    print("KROK 4: Dokładny wynik starcia (Model Dwumianowy)")
    print(f"  Całkowita szansa na zwycięstwo atakującego: {dokladne_prawdopodobienstwo:.4f} ({dokladne_prawdopodobienstwo*100:.2f}%)\n")

    # KROK 5: APROKSYMACJA (Rozkład Normalny)
    # Przydatne dla bardzo dużych wartości HP (np. bitwy morskie lub późna faza gry), 
    # gdzie pętle mogłyby spowalniać system.
    srednia = md * p
    odchylenie_standardowe = math.sqrt(md * p * q)
    
    # Obliczamy wartość 'z' dla rozkładu normalnego (z poprawką na ciągłość - 0.5)
    # Zabezpieczenie przed dzieleniem przez zero, gdy p=1 lub p=0
    if odchylenie_standardowe > 0:
        z = (k - srednia - 0.5) / odchylenie_standardowe
        przyblizone_prawdopodobienstwo = 1.0 - phi(z)
    else:
        przyblizone_prawdopodobienstwo = 1.0 if p == 1 else 0.0

    print("KROK 5: Przybliżony wynik starcia (Aproksymacja Rozkładem Normalnym)")
    print(f"  Wartość oczekiwana trafień: {srednia:.2f}")
    print(f"  Odchylenie standardowe: {odchylenie_standardowe:.2f}")
    print(f"  Przybliżona szansa na zwycięstwo atakującego: {przyblizone_prawdopodobienstwo:.4f} ({przyblizone_prawdopodobienstwo*100:.2f}%)\n")
    
    # Wyprowadzenie wniosku końcowego
    szansa_procentowa = dokladne_prawdopodobienstwo * 100
    if szansa_procentowa > 80:
        werdykt = "Atakujący ma miażdżącą przewagę."
    elif szansa_procentowa > 50:
        werdykt = "Atakujący ma lekką przewagę, ale ryzyko porażki istnieje."
    elif szansa_procentowa > 20:
        werdykt = "Ryzykowny atak. Obrońca najpewniej zwycięży."
    else:
        werdykt = "Misja samobójcza. Atakujący ma minimalne szanse."
        
    print(f"WERDYKT: {werdykt}")

# --- URUCHOMIENIE SYMULACJI ---
# Przykład: Rydwan (Atak 3) atakuje Falangę (Obrona 2) w mieście (Obrona * 1.5 = 3)
# Załóżmy podstawowe jednostki: 10 HP każda, siła ognia 1 dla obu.

sila_atakujacego = 3
sila_obroncy = 3       # Falanga 2 * 1.5 (za miasto)
hp_atakujacego = 10
hp_obroncy = 10
sila_ognia_atakujacego = 1
sila_ognia_obroncy = 1

symuluj_walke_freeciv(
    sila_atakujacego, 
    sila_obroncy, 
    hp_atakujacego, 
    hp_obroncy, 
    sila_ognia_atakujacego, 
    sila_ognia_obroncy
)
