# TDDC17 Lab 6: Planning — svar på fråga 2 och 3

Alla aktioner har kostnad 1, så plankostnad och planlängd sammanfaller.
Samtliga tal nedan är avlästa ur Fast Downwards utskrift.

## Sammanfattning

| | Fråga 2: GBFS + FF | Fråga 3: A\* + iPDB |
|---|---|---|
| Sökkonfiguration | `eager_greedy([ff()])` | `astar(ipdb())` |
| **Plankostnad** | **11** | **10** |
| **Heuristikvärde i starttillståndet** | **10** | **5** |
| Expanderade tillstånd | 12 | 32 |
| Utvärderade tillstånd | 22 | 49 |
| Genererade tillstånd | 68 | 68 |
| Optimal? | Nej | Ja |

---

## Fråga 2 — Greedy best-first search med FF-heuristiken

**Plankostnad: 11. Heuristikvärde i starttillståndet: h^FF(s₀) = 10.**

Planen som hittades:

```
 1. pick_up   keyK, roomLIVING
 2. open_door roomLIVING, doorK, keyK
 3. pick_up   keyL, roomLIVING
 4. open_door roomLIVING, doorL, keyL
 5. move      roomLIVING → roomKITCHEN
 6. pick_up   keyAll, roomKITCHEN
 7. move      roomKITCHEN → roomLIVING
 8. move      roomLIVING → roomCORRIDOR
 9. open_door roomCORRIDOR, doorC, keyAll
10. move      roomCORRIDOR → roomLOBBY
11. open_door roomLOBBY, doorF, keyAll
```

### Varför planen är suboptimal

Planen är en aktion längre än optimum. Skillnaden mot den optimala planen är
exakt raden `pick_up keyL`.

Roboten öppnar dörr L med keyL i steg 4, alltså *innan* den hämtat huvudnyckeln.
Den passerar Living Room igen i steg 7, och bär då redan keyAll — som också öppnar
dörr L. Hade den väntat med att öppna L till dess hade keyL aldrig behövts.
Själva öppningen av dörr L är nödvändig i båda planerna; det är enbart
upplockningen av keyL som är överflödig.

Orsaken ligger i evalueringsfunktionen. GBFS använder

    f(n) = h(n)

utan g-termen. Aktionen `pick_up keyL` sänkte h^FF från 8 till 7 och såg därför
lokalt ut som framsteg. Eftersom kostnaden dittills inte ingår i f fanns det
ingenting som kunde invända mot att omvägen gjorde den totala planen längre.

### Om heuristikvärdet

h^FF bygger på delete-relaxationen Π⁺, där alla negativa effekter strukits. I den
relaxerade världen tappar roboten aldrig en nyckel och lämnar aldrig ett rum.
Heuristiken bygger en relaxed planning graph framåt, extraherar en relaxerad plan
bakåt, och returnerar dess kostnad.

Extraktionen är girig, inte optimal, så h^FF ≥ h⁺ men är inte admissibel. För
detta problem gav den h^FF(s₀) = 10, vilket råkar sammanfalla med h*(s₀) = 10.
Det är ett sammanträffande, inte en garanti. (En handräkning ger h⁺(s₀) = 9: den
relaxerade planen slipper återvändningsförflyttningen från Kitchen, eftersom
`robot_in(roomLIVING)` aldrig raderas i Π⁺.)

### Plattå i sökningen

Loggen går från g=4 direkt till g=6 utan att h sjunker däremellan. Det steget är
`move roomLIVING → roomKITCHEN`. Delete-relaxationen ser inget värde i den
förflyttningen, eftersom den relaxerade roboten redan "är" i alla rum den besökt.
Det är den enda plattån i sökningen.

---

## Fråga 3 — A\* med iPDB-heuristiken

**Plankostnad: 10. Heuristikvärde i starttillståndet: h^iPDB(s₀) = 5.**

Den optimala planen:

```
 1. pick_up   keyK, roomLIVING
 2. open_door roomLIVING, doorK, keyK
 3. move      roomLIVING → roomKITCHEN
 4. pick_up   keyAll, roomKITCHEN
 5. move      roomKITCHEN → roomLIVING
 6. open_door roomLIVING, doorL, keyAll
 7. move      roomLIVING → roomCORRIDOR
 8. open_door roomCORRIDOR, doorC, keyAll
 9. move      roomCORRIDOR → roomLOBBY
10. open_door roomLOBBY, doorF, keyAll
```

### Att 10 är optimalt

För att öppna dörr F måste roboten stå i Lobby. Det kräver att L och C är
upplåsta, alltså minst 2 `open_door` + 2 `move`, plus den avslutande öppningen
av F — sammanlagt 5 aktioner. Utöver det måste nycklar som täcker {L, C, F}
förvärvas.

Den billigaste täckningen är huvudnyckeln, till en kostnad av 5 aktioner:
`pick_up keyK`, `open_door doorK`, `move` till Kitchen, `pick_up keyAll`,
`move` tillbaka. Totalt 10.

Alternativet med individuella nycklar kostar mer: keyC och keyF ligger båda i
Bathroom, bakom dörr B, vars nyckel ligger i Corridor. Den rutten kräver 12
aktioner.

### Varför A\* hittar optimum

A\* använder

    f(n) = g(n) + h(n)

Optimalitetsgarantin kräver två saker: att h är **admissibel** (h ≤ h\*, aldrig en
överskattning) och att g ingår i f. Mönsterdatabasheuristiker är admissibla per
konstruktion — de löser exakt en projektion av problemet på en delmängd av
variablerna, och en optimal lösning på en avslappning kan aldrig överstiga den
verkliga optimalkostnaden.

Med C\* = 10 måste varje nod med f(n) < 10 expanderas innan målet kan plockas ur
kön. Det är precis vad loggen visar:

```
f = 5  →  0 expanderade
f = 6  →  1
f = 7  →  5
f = 8  → 10
f = 9  → 15
f = 10 → 19        ("Expanded until last jump: 19")
totalt   32
```

De 19 noderna med f < 10 är garantin i konkret form. Resterande 13 ligger i det
sista f = 10-skiktet, där sökningen stötte på målet innan skiktet uttömts.

### iPDB och mönstergenerering

iPDB (`ipdb()`) är en kanonisk PDB-heuristik där mönsterkollektionen genereras med
hill climbing. Loggen visar att den körde 4 iterationer, genererade 21
kandidatmönster, och efter dominansbeskärning behöll **ett** mönster med total
PDB-storlek 40.

Att bara ett mönster överlevde förklarar det låga heuristikvärdet: h^iPDB(s₀) = 5
är hälften av det verkliga avståndet. En enda projektion fångar bara en del av
problemets struktur.

Sökningen kördes med `with reopening closed nodes`, men `Reopened 0`. Orsaken är
att PDB-heuristiker är **konsistenta**, alltså uppfyller h(s) ≤ c(a) + h(s'), och
en konsistent heuristik i A\* når varje nod med optimalt g redan första gången.

---

## Jämförelse

Det mest anmärkningsvärda resultatet är att den **sämre informerade heuristiken
gav den bättre planen**:

| | h(s₀) | h\*(s₀) | Plankostnad |
|---|---|---|---|
| FF | 10 | 10 | 11 |
| iPDB | 5 | 10 | 10 |

h^FF träffade det verkliga avståndet exakt; h^iPDB var hälften. Ändå var det
iPDB-körningen som returnerade optimum.

Slutsatsen är att heuristikens noggrannhet styr **hur snabbt** sökningen går, inte
**hur bra planen blir**. Plankvaliteten avgörs av sökalgoritmen: A\* har både
admissibilitet och g-termen, GBFS har ingendera. h^FF är dessutom inte admissibel,
så även om den hade använts i A\* hade optimalitetsgarantin fallit.

Priset för garantin var en faktor 2,7 i expansioner (32 mot 12) för att spara en
enda aktion. På ett större problem hade den avvägningen sett annorlunda ut — det
är därför satisficing-planering existerar som eget forskningsområde.

---

## Bilaga: h^add som kontrollexperiment

Samma sökning kördes även med `eager_greedy([add()])`:

| | h(s₀) | Plankostnad | Expanderade | Utvärderade |
|---|---|---|---|---|
| h^FF | 10 | 11 | 12 | 22 |
| h^add | 17 | 11 | 12 | 22 |

h^add överskattar h\* = 10 med sju och är alltså bevisligen icke-admissibel.
Orsaken är att den summerar kostnaden för varje delmål oberoende och därmed
dubbelräknar delat förarbete — att hämta huvudnyckeln krävs både för att nå Lobby
och för att öppna ytterdörren, och räknas två gånger.

Trots det blev sökningen **identisk**: samma plan, samma antal expansioner,
utvärderingar och genererade tillstånd. Förklaringen är att h^add och h^FF längs
denna väg är relaterade via

    h^add(s) = 2 · h^FF(s) − 3     (för g ≤ 8)

vilket är en strikt monotont växande transformation. GBFS jämför endast
heuristikvärden och adderar dem aldrig till något, så en monoton omskalning ändrar
inte rangordningen mellan tillstånd och därmed inte sökningens beteende.

Relationen upphör vid g = 9, där roboten nått Lobby och de återstående delmålen
inte längre delar förarbete — då försvinner dubbelräkningen och de två
heuristikerna sammanfaller.

För A\* hade h^add varit förödande, eftersom f = g + h kräver att h är
kommensurabel med verkliga kostnader. Det är därför fråga 3 specificerar en
admissibel heuristik.

---

## Modellens storlek

Fast Downwards översättare rapporterar 12 variabler, 27 fakta och 32 operatorer.
Operatorantalet stämmer mot uppgiftsspecifikationen:

| Aktion | Antal | Motsvarar |
|---|---|---|
| `open_door` | 18 | "one for each fitting pair of door and key" |
| `pick_up` | 6 | "one for each key" |
| `move` | 8 | "one for each connected pair of rooms" |

För `open_door`: fyra dörrar (K, L, B, C) har vardera två angränsande rum och två
passande nycklar (färgnyckeln plus keyAll) = 4 instanser var; dörr F nås endast
från Lobby = 2 instanser. Summa 18.

Beskärningen sker automatiskt eftersom `room_has_door` och `key_fits` aldrig
förekommer i någon effekt. Fast Downwards Datalog-baserade grundning känner igen
dem som statiska och grundar bara de kombinationer som faktiskt är möjliga — en
enda parametriserad aktion räcker alltså i modellen.