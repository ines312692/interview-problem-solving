# Solution — Les 100 Prisonniers et l'Ampoule

## Stratégie

Désignez un **compteur unique** parmi les prisonniers. Les autres servent de **signaleurs**.

---

## Rôles

### Le Compteur (1 prisonnier désigné)
- **Seul autorisé** à éteindre l'ampoule
- Compte chaque fois qu'il éteint
- Déclare la victoire quand son compte atteint **99**

### Les Signaleurs (99 autres prisonniers)
- Allument l'ampoule **une seule fois** dans leur vie (la première fois qu'ils la trouvent éteinte)
- Après avoir allumé une fois, ils ne touchent plus jamais à l'ampoule

---

## Protocole détaillé

### Pour le Compteur :
```
À chaque visite :
  Si l'ampoule est ALLUMÉE :
    → Éteindre l'ampoule
    → Incrémenter son compteur personnel
    → Si compteur = 99 : DÉCLARER "Tous ont visité"
  Si l'ampoule est ÉTEINTE :
    → Ne rien faire
```

### Pour chaque Signaleur :
```
Variable personnelle : a_déjà_signalé = FAUX

À chaque visite :
  Si a_déjà_signalé = FAUX et ampoule ÉTEINTE :
    → Allumer l'ampoule
    → a_déjà_signalé = VRAI
  Sinon :
    → Ne rien faire
```

---

## Pourquoi ça fonctionne ?

1. Chaque signaleur n'allume l'ampoule **qu'une seule fois**
2. Le compteur est le **seul** à éteindre
3. Donc chaque extinction correspond à **un signaleur unique** qui a visité
4. Quand le compteur atteint 99, cela signifie que 99 signaleurs différents ont visité
5. Comme le compteur lui-même a visité (pour compter), **100 prisonniers** ont visité

---

## Temps estimé

Cette stratégie est **lente** mais **garantie**.

En moyenne, il faut environ **10 000 jours** (~27 ans) pour que tous les prisonniers aient eu l'opportunité de signaler. C'est parce que :
- Le compteur doit être présent pour "collecter" chaque signal
- Les visites sont aléatoires
- Vers la fin, attendre que le dernier signaleur visite ET que le compteur visite ensuite peut prendre très longtemps

---

## Variante optimisée

Il existe des stratégies plus rapides utilisant plusieurs compteurs ou un système de comptage par puissances de 2, mais elles sont plus complexes à coordonner.

---

## Principe clé

Ce problème illustre la **communication à canal limité** : comment transmettre de l'information quand le seul canal disponible est un unique bit (ampoule allumée/éteinte). La solution repose sur un **protocole asymétrique** où les rôles sont clairement définis à l'avance.

C'est aussi un exemple de compromis entre **simplicité** et **efficacité** : la stratégie simple est très lente, mais elle est garantie de fonctionner.