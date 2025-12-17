# Solution — Les Deux Cordes (Minuteur 45 Minutes)

## Stratégie

Allumez les cordes par **plusieurs extrémités** pour manipuler le temps de combustion.

## Étapes

1. **Au temps T=0 :**
   - Allumez la **corde A par les DEUX bouts**
   - Allumez la **corde B par UN seul bout**

2. **Au temps T=30 minutes :**
   - La corde A se consume entièrement (brûler des deux côtés divise le temps par 2)
   - À cet instant, allumez l'**autre bout de la corde B**

3. **Au temps T=45 minutes :**
   - La corde B se consume entièrement
   - **45 minutes se sont écoulées**

## Explication détaillée

| Temps | Corde A | Corde B |
|-------|---------|---------|
| T=0 | Allumée des 2 bouts | Allumée d'1 bout |
| T=30 | Consumée (30 min) | Il reste 30 min de corde |
| T=30 | — | On allume l'autre bout |
| T=45 | — | Consumée (15 min de plus) |

## Principe clé

Allumer une corde par les deux bouts **divise son temps de combustion par 2**, peu importe la non-uniformité de la combustion. Ce problème teste votre capacité à sortir des schémas de pensée conventionnels.