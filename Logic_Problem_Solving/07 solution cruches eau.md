# Solution — Le Problème des Cruches d'Eau

## Solution principale (5L et 3L → obtenir 4L)

### Méthode 1 : En 6 étapes

| Étape | Action | Cruche 5L | Cruche 3L |
|-------|--------|-----------|-----------|
| 0 | État initial | 0 | 0 |
| 1 | Remplir la cruche de 5L | **5** | 0 |
| 2 | Verser dans la cruche de 3L | 2 | **3** |
| 3 | Vider la cruche de 3L | 2 | **0** |
| 4 | Transférer les 2L dans la cruche de 3L | **0** | 2 |
| 5 | Remplir la cruche de 5L | **5** | 2 |
| 6 | Compléter la cruche de 3L | **4** | 3 |

 **Résultat : 4 litres dans la cruche de 5L**

---

### Méthode 2 : Alternative en 6 étapes

| Étape | Action | Cruche 5L | Cruche 3L |
|-------|--------|-----------|-----------|
| 0 | État initial | 0 | 0 |
| 1 | Remplir la cruche de 3L | 0 | **3** |
| 2 | Verser dans la cruche de 5L | **3** | 0 |
| 3 | Remplir la cruche de 3L | 3 | **3** |
| 4 | Compléter la cruche de 5L | **5** | 1 |
| 5 | Vider la cruche de 5L | **0** | 1 |
| 6 | Transférer 1L puis remplir 3L et verser | **4** | 0 |

*(Étape 6 détaillée : verser le 1L dans la 5L, remplir la 3L, verser dans la 5L)*

---

## Principe mathématique

Ce problème repose sur l'**identité de Bézout**. 

On peut mesurer toute quantité **Q** si et seulement si **Q** est un multiple du **PGCD** des deux cruches.

- PGCD(5, 3) = **1**
- Donc on peut mesurer : 1L, 2L, 3L, 4L, 5L...

L'équation de Bézout nous dit qu'il existe des entiers a et b tels que :
```
5a + 3b = 4
```

Une solution : a = 2, b = -2 → 5(2) + 3(-2) = 10 - 6 = 4

Cela correspond à : remplir 2 fois la cruche de 5L et vider 2 fois la cruche de 3L.

---

## Solutions des variantes

### Variante 1 : 8L et 5L → obtenir 4L

| Étape | Cruche 8L | Cruche 5L |
|-------|-----------|-----------|
| 1 | **8** | 0 |
| 2 | 3 | **5** |
| 3 | 3 | **0** |
| 4 | 0 | **3** |
| 5 | **8** | 3 |
| 6 | 6 | **5** |
| 7 | 6 | **0** |
| 8 | 1 | **5** |
| 9 | 1 | **0** |
| 10 | 0 | **1** |
| 11 | **8** | 1 |
| 12 | **4** | 5 |

---

### Variante 2 : 7L et 4L → obtenir 5L

| Étape | Cruche 7L | Cruche 4L |
|-------|-----------|-----------|
| 1 | **7** | 0 |
| 2 | 3 | **4** |
| 3 | 3 | **0** |
| 4 | 0 | **3** |
| 5 | **7** | 3 |
| 6 | 6 | **4** |
| 7 | 6 | **0** |
| 8 | 2 | **4** |
| 9 | 2 | **0** |
| 10 | 0 | **2** |
| 11 | **7** | 2 |
| 12 | **5** | 4 |

---

### Variante 3 : 8L (pleine), 5L, 3L → partager en 4L + 4L

| Étape | 8L | 5L | 3L |
|-------|----|----|----| 
| 0 | 8 | 0 | 0 |
| 1 | 3 | **5** | 0 |
| 2 | 3 | 2 | **3** |
| 3 | **6** | 2 | 0 |
| 4 | 6 | 0 | **2** |
| 5 | 1 | **5** | 2 |
| 6 | 1 | **4** | 3 |
| 7 | **4** | 4 | 0 |

 **Résultat : 4L dans la cruche de 8L et 4L dans la cruche de 5L**

---

## Principe clé

Ce problème teste votre capacité à :
1. **Penser en étapes** et gérer des états multiples
2. Reconnaître un problème de **théorie des nombres** (Bézout)
3. Explorer systématiquement un **espace d'états** (approche algorithmique)

C'est aussi un classique du film **Die Hard 3** (Une journée en enfer) !