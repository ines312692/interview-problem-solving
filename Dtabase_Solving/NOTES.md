## Inner Join (Jointure Interne)
````
INNER JOIN
Idée : Ne garde que les lignes qui existent dans les deux tables.
Si une personne n’a pas d’adresse, elle n’apparaît pas.
````
## Left Join (Jointure Gauche)
````
LEFT JOIN
Idée : Garde toutes les lignes de la table de gauche, même si elles n’ont pas de correspondance à droite.
Si une personne n’a pas d’adresse, on met NULL pour les colonnes de l’adresse.
````
## Right Join (Jointure Droite)
````
RIGHT JOIN
Idée : Garde toutes les lignes de la table de droite, même si elles n’ont
    pas de correspondance à gauche.
Si une adresse n’a pas de personne associée, on met NULL pour les colonnes de la personne.
````
## Full Join (Jointure Complète)
````
FULL JOIN
Idée : Garde toutes les lignes des deux tables, même si elles n’ont pas de
    correspondance.
Si une personne n’a pas d’adresse, on met NULL pour les colonnes de l’adresse.
Si une adresse n’a pas de personne associée, on met NULL pour les colonnes de
    la personne.
````