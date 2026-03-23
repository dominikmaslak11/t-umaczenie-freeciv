Oto kompletny poradnik przekonwertowany na format Markdown. Dzięki temu bez problemu opublikujesz go na blogu, repozytorium GitHub (jako plik README.md) czy na forum dyskusyjnym.

# ---

**Zaawansowany Poradnik Dowódcy: Freeciv**

## **Analiza taktyczna, matematyczna i ekonomiczna**

Niniejszy poradnik stanowi kompleksowe kompendium wiedzy na temat mechaniki walki w grze Freeciv (opartej na klasycznym zestawie zasad). Wykracza on poza podstawowe instrukcje, skupiając się na matematycznym zapleczu starć, optymalizacji ataków (w tym taktyce oblężniczej), mechanice bombardowania oraz opłacalności ekonomicznej wojen.

## ---

**1\. Wstęp do Mechaniki Walki**

Walka w Freeciv rzadko kończy się po jednym uderzeniu. Zamiast tego, w ułamku sekundy gra przeprowadza symulację starcia turowego, w którym jednostki na przemian zadają sobie obrażenia. Starcie trwa do momentu, w którym punkty życia (HP) jednej z jednostek spadną do zera.

### **Kluczowe statystyki jednostki**

Każda jednostka na polu bitwy jest opisana trzema głównymi wartościami bojowymi:

* **Siła Ataku / Obrony ($s$ i $r$):** Decyduje o szansie na trafienie przeciwnika w pojedynczej rundzie starcia. Prawdopodobieństwo trafienia przez atakującego to zawsze $p \= \\frac{s}{s+r}$.  
* **Punkty Życia (HP):** Zdolność jednostki do przyjmowania obrażeń.  
* **Siła Ognia (Firepower \- FP):** Liczba punktów życia (HP), które jednostka odbiera wrogowi przy każdym udanym trafieniu.

Dzięki temu, że starcie składa się z wielu rund, gra drastycznie faworyzuje jednostkę o wyższych statystykach. Niewielka przewaga siły potęguje się z każdą rundą, dając ostatecznie ogromną szansę na przetrwanie.

## ---

**2\. Modyfikatory Terenu i Doświadczenia**

Jednym z największych błędów początkujących graczy jest ignorowanie faktu, że **modyfikatory we Freeciv się mnożą, a nie dodają**. To sprawia, że dobrze ufortyfikowana obrona jest w stanie odeprzeć siły z pozoru wielokrotnie silniejsze.

### **Najważniejsze mnożniki obronne:**

* **Doświadczenie (Weteran):** Początkujący (x1.0), Weteran (x1.5), Doświadczony (x1.75), Elitarny (x2.0).  
* **Teren:** Rzeka (x1.5), Las/Bagno (x1.5), Wzgórza (x2.0), Góry (x3.0).  
* **Ufortyfikowanie:** Jednostka z rozkazem "Okopanie" (Fortify) lub znajdująca się w mieście zawsze otrzymuje mnożnik x1.5.  
* **Struktury:** Forteca (x2.0), Mury Miejskie (x3.0 przeciwko siłom lądowym).

**Przykład Taktyczny:** Podstawowa Falanga (Obrona 2), będąca elitarnym weteranem (x2), stojąca w mieście z murami (x3), na wzgórzu (x2), za rzeką (x1.5), automatycznie okopana (x1.5), osiąga potworną siłę obrony wynoszącą **54**\!

## ---

**3\. Mechanika "Stack Kill" (Śmierć Stosu)**

Mechanika ta jest najważniejszym elementem pozycjonowania wojsk. Jeśli na jednym polu znajduje się wiele jednostek (tzw. "stos"), do obrony staje zawsze ta jednostka, która ma największe szanse na zwycięstwo.

**Kluczowa zasada:** Jeśli obrońca ten zginie na otwartym terenie, **wszystkie pozostałe jednostki na tym samym polu również ulegają natychmiastowemu zniszczeniu**.

Aby uniknąć tej katastrofy, armie muszą stacjonować wewnątrz Miast lub Zbudowanych Fortec — w tych strukturach śmierć obrońcy nie pociąga za sobą ofiar w reszcie oddziałów.

## ---

**4\. Taktyka Oblężnicza i Ludzkie Fale**

Gdy mierzysz się z silnie ufortyfikowaną pozycją, pojedynczy atak to samobójstwo. Należy zastosować strategię falową (N vs 1).

Mimo że Twoja jednostka atakująca najpewniej zginie, ma szansę odebrać obrońcy część punktów życia (HP). Ponieważ uszkodzone jednostki nie odzyskują zdrowia w trakcie trwania jednej tury gracza, wysyłając serię oddziałów "na stracenie", powoli redukujesz HP potężnego obrońcy. Matematycznie modeluje się to za pomocą Łańcuchów Markowa, co pozwala oszacować, że na przykład do osiągnięcia 90% szansy przełamania frontu potrzebujesz poświecić dokładnie 4 jednostki.

## ---

**5\. Artyleria i Bombardowanie**

W nowszych wersjach gry, jednostki dystansowe posiadają parametr **Bombardment Rate** (Szybkość Bombardowania). Różnice między walką w zwarciu a bombardowaniem są znaczące:

1. **Brak strat własnych:** Atakujący uderza na dystans. Jeśli przegra "rzut kośćmi" w danej rundzie, po prostu pudłuje i nie traci własnych HP.  
2. **Ograniczenie rund:** Jednostka oddaje tylko tyle strzałów, ile wynosi jej wskaźnik *Bombardment Rate*. Starcie nie toczy się aż do śmierci jednej ze stron.  
3. **Złota zasada 1 HP:** Bombardowanie **nigdy** nie zabija. Ostrzał zatrzymuje się, gdy celowi zostaje 1 punkt życia. Wymagane jest wysłanie jednostki walczącej w zwarciu, by wejść na pole i dobić wroga.

**Wniosek:** Zmiękczanie celów artylerią to najbezpieczniejsza i najbardziej opłacalna metoda walki z potężnymi fortyfikacjami.

## ---

**6\. Ekonomia Wojny**

Wojny we Freeciv nie wygrywa się tylko militarnie, ale przede wszystkim ekonomicznie. Każda jednostka kosztuje określoną liczbę Tarcz (Shields).

Zanim dokonasz ataku, zwłaszcza metodą ludzkiej fali, zbadaj jego opłacalność. Jeśli wyślesz 5 jednostek kosztujących łącznie 150 tarcz, aby zniszczyć obrońcę wartego 20 tarcz, poniesiesz potężną stratę gospodarczą. Mimo że wygrałeś bitwę taktycznie, przeciwnik zyskał przewagę ekonomiczną. Szukaj wymian wyrównanych lub posiłkuj się tanim w utrzymaniu i bezstratnym bombardowaniem.

## ---

**7\. Narzędzia Zewnętrzne**

Skuteczne dowodzenie armią opiera się na liczbach. Warto korzystać z zewnętrznych symulatorów i kalkulatorów (np. w Pythonie lub na urządzeniach HP Prime), które potrafią błyskawicznie symulować starcia, obliczać oczekiwane straty oraz wyciągać wnioski ekonomiczne przed wydaniem ostatecznego rozkazu do ataku.

---

Czy chciałbyś, abym przygotował dla Ciebie kod HTML tego poradnika, abyś mógł go łatwo wrzucić bezpośrednio na stronę internetową?