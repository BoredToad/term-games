# Fire på rad i python!
Dependencies: termcolor
Jeg har prøvd å skrive koden på en oversiktlig og enkel måte,
så jeg for håpe den kan snakke for seg selv. Det jeg tror trenger
litt forklarelse er den diagonale sjekkingen, dette tok meg litt tid
å fikse og jeg trengte å skrive det for hånd for å løse problemet.

Tenk deg et 5x5 brett, dette er en tegning av hva sum listen representerer:

i = 0 | 0 1 2 3 4
i = 1 | 1 2 3 4 5
i = 2 | 2 3 4 5 6
i = 3 | 3 4 5 6 7
i = 4 | 4 5 6 7 8
        ---------
j =     0 1 2 3 4

Som du kan se, trenger jeg bare å plusse i og j for å finne liste indeksen.


# VIKTIG!!!
I print_board() funksjonen min bruker jeg os for å runne clear i terminalen som er et unix command,
online sto det at dette ikke fungerer på windows så det er mulig du må endre det.
