# Les 100 Prisonniers et l'Ampoule

## Énoncé

**100 prisonniers** sont enfermés dans des cellules individuelles sans aucun moyen de communication entre eux.

Il existe une **salle spéciale** contenant uniquement une ampoule (initialement éteinte). Chaque jour, le gardien choisit **un prisonnier au hasard** et l'emmène dans cette salle. Le prisonnier peut alors :
- Allumer l'ampoule (si elle est éteinte)
- Éteindre l'ampoule (si elle est allumée)
- Ne rien faire

Un même prisonnier peut être choisi plusieurs fois, et certains peuvent ne jamais être choisis pendant longtemps.

À **n'importe quel moment**, un prisonnier peut déclarer : « Les 100 prisonniers ont tous visité cette salle au moins une fois. »
- Si c'est **vrai** : tous les prisonniers sont libérés
- Si c'est **faux** : tous les prisonniers sont exécutés

**Contraintes :**
- Les prisonniers peuvent élaborer une stratégie ensemble **avant** d'être séparés
- Une fois séparés, ils n'ont aucun moyen de communiquer (sauf via l'état de l'ampoule)
- Ils ne savent pas quel jour on est ni combien de visites ont eu lieu
- Le choix du prisonnier chaque jour est totalement aléatoire

**Question :**
Quelle stratégie les prisonniers doivent-ils adopter pour garantir leur libération (même si cela prend du temps) ?