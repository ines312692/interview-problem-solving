# Solution — Le Vin Empoisonné

## Stratégie

Utilisez le **codage binaire**. Avec 10 prisonniers, vous pouvez distinguer 2¹⁰ = 1024 bouteilles différentes.

---

## Méthode

### Étape 1 : Numérotez les bouteilles en binaire

| Bouteille | Binaire (10 bits) |
|-----------|-------------------|
| 1 | 0000000001 |
| 2 | 0000000010 |
| 3 | 0000000011 |
| ... | ... |
| 500 | 0111110100 |
| ... | ... |
| 1000 | 1111101000 |

### Étape 2 : Assignez chaque prisonnier à un bit

- Prisonnier 1 → Bit 1 (unités)
- Prisonnier 2 → Bit 2
- ...
- Prisonnier 10 → Bit 10

### Étape 3 : Distribution du vin

Chaque prisonnier **N** goûte toutes les bouteilles dont le **bit N** vaut **1**.

Exemple :
- Bouteille 7 = `0000000111` → Prisonniers 1, 2, 3 goûtent
- Bouteille 100 = `0001100100` → Prisonniers 3, 6, 7 goûtent

### Étape 4 : Lecture du résultat (24h plus tard)

Les prisonniers morts forment un nombre binaire qui indique directement la bouteille empoisonnée.

**Exemple :** Si les prisonniers 2, 5 et 7 meurent :
- Binaire = `0001010010` = **82** en décimal
- La bouteille **82** est empoisonnée

---

## Tableau récapitulatif

| Prisonnier | Bit | Goûte les bouteilles où... |
|------------|-----|---------------------------|
| 1 | 2⁰ | numéro est impair |
| 2 | 2¹ | (n÷2) mod 2 = 1 |
| 3 | 2² | (n÷4) mod 2 = 1 |
| ... | ... | ... |
| 10 | 2⁹ | n ≥ 512 |

---

## Principe clé

Ce problème est un exemple parfait de **théorie de l'information**. Chaque prisonnier représente **1 bit** d'information (mort = 1, vivant = 0). Avec 10 bits, on peut encoder 2¹⁰ = 1024 valeurs différentes, ce qui est suffisant pour 1000 bouteilles.

C'est aussi une illustration du fait qu'un problème apparemment impossible devient trivial avec le bon **cadre de représentation**.