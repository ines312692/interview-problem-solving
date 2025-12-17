# Solution — Les 12 Balles

## Stratégie

Divisez les balles en groupes et suivez les **possibilités** (potentiellement lourde ou légère) à chaque pesée.

## Notation

- Balles numérotées de 1 à 12
- `L` = pourrait être plus légère
- `H` = pourrait être plus lourde
- `X` = normale (éliminée)

---

## Pesée 1 : Comparez {1,2,3,4} vs {5,6,7,8}

### Cas A : Équilibre
La balle défectueuse est parmi **{9,10,11,12}**

**Pesée 2 :** {1,2,3} vs {9,10,11}
- Si équilibre → c'est la balle **12** ; Pesée 3 : comparez 12 vs 1 pour savoir si lourde/légère
- Si {9,10,11} plus lourd → une de ces 3 est lourde ; Pesée 3 : 9 vs 10
- Si {9,10,11} plus léger → une de ces 3 est légère ; Pesée 3 : 9 vs 10

---

### Cas B : {1,2,3,4} plus lourd que {5,6,7,8}
Donc : 1,2,3,4 sont suspects-lourds (H) ; 5,6,7,8 sont suspects-légers (L) ; 9,10,11,12 sont normaux (X)

**Pesée 2 :** {1,2,5} vs {3,6,9}

| Résultat | Analyse | Pesée 3 |
|----------|---------|---------|
| Équilibre | C'est 4(H) ou 7(L) ou 8(L) | 7 vs 8 |
| {1,2,5} plus lourd | C'est 1(H) ou 2(H) ou 6(L) | 1 vs 2 |
| {3,6,9} plus lourd | C'est 3(H) ou 5(L) | 3 vs 9 |

---

### Cas C : {1,2,3,4} plus léger que {5,6,7,8}
Symétrique au cas B. Inversez lourd/léger.

---

## Principe clé

Ce problème classique utilise la **logique ternaire** : chaque pesée a 3 résultats possibles (gauche plus lourd, équilibre, droite plus lourd). Avec 3 pesées, on peut distinguer 3³ = 27 situations. Comme il y a 12 × 2 = 24 possibilités (12 balles × 2 états), c'est théoriquement faisable — mais juste !

Ce problème teste votre capacité à gérer une **arborescence de décisions** et à maximiser l'information obtenue à chaque étape.