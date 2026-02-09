# Exercices Git — Du Simple au Très Avancé

---

## Niveau 1 : Débutant

### Exercice 1.1 — Initialisation et premiers commits

```
Contexte : Tu démarres un nouveau projet from scratch.

Tâches :
1. Crée un répertoire "mon-projet" et initialise un dépôt Git.
2. Crée un fichier README.md avec le titre du projet.
3. Ajoute-le au staging area et fais un premier commit.
4. Modifie le README.md, vérifie le diff, puis commite.
5. Affiche l'historique des commits.
```

<details>
<summary>Solution</summary>

```bash
mkdir mon-projet && cd mon-projet
git init
echo "# Mon Projet" > README.md
git add README.md
git commit -m "Initial commit: add README"

echo "Description du projet" >> README.md
git diff
git add README.md
git commit -m "Update README with description"

git log --oneline
```
</details>

---

### Exercice 1.2 — Staging sélectif

```
Contexte : Tu as modifié 3 fichiers mais tu veux commiter seulement 2 d'entre eux.

Tâches :
1. Crée 3 fichiers : a.txt, b.txt, c.txt
2. Ajoute du contenu dans chacun.
3. Ajoute seulement a.txt et b.txt au staging.
4. Vérifie le status (c.txt doit rester unstaged).
5. Commite, puis ajoute c.txt dans un second commit.
```

<details>
<summary>Solution</summary>

```bash
echo "contenu A" > a.txt
echo "contenu B" > b.txt
echo "contenu C" > c.txt

git add a.txt b.txt
git status
# a.txt et b.txt en vert (staged), c.txt en rouge (untracked)

git commit -m "Add a.txt and b.txt"
git add c.txt
git commit -m "Add c.txt"
```
</details>

---

### Exercice 1.3 — Annuler des modifications

```
Tâches :
1. Modifie un fichier existant.
2. Annule la modification AVANT le staging (git restore).
3. Modifie-le à nouveau, ajoute-le au staging.
4. Retire-le du staging SANS perdre les modifications (git restore --staged).
5. Vérifie avec git status à chaque étape.
```

<details>
<summary>Solution</summary>

```bash
echo "modification" >> a.txt
git restore a.txt          # annule la modif dans le working directory

echo "autre modif" >> a.txt
git add a.txt
git restore --staged a.txt  # retire du staging, garde la modif
git status                   # a.txt est modifié mais unstaged
```
</details>

---

### Exercice 1.4 — .gitignore

```
Tâches :
1. Crée un fichier .env contenant SECRET_KEY=abc123
2. Crée un dossier __pycache__/ avec un fichier dedans.
3. Crée un .gitignore qui ignore .env et __pycache__/
4. Vérifie que git status ne montre PAS ces fichiers.
5. Que se passe-t-il si .env était déjà tracké ? Comment le retirer du tracking ?
```

<details>
<summary>Solution</summary>

```bash
echo "SECRET_KEY=abc123" > .env
mkdir __pycache__ && echo "cache" > __pycache__/module.cpython-39.pyc

cat > .gitignore << 'EOF'
.env
__pycache__/
EOF

git add .gitignore && git commit -m "Add .gitignore"
git status  # .env et __pycache__ n'apparaissent pas

# Si .env était déjà tracké :
git rm --cached .env
git commit -m "Stop tracking .env"
```
</details>

---

## Niveau 2 : Intermédiaire

### Exercice 2.1 — Branches et merge

```
Contexte : Tu travailles sur une feature en parallèle du main.

Tâches :
1. Crée une branche "feature/login".
2. Fais 2 commits sur cette branche.
3. Retourne sur main, fais 1 commit.
4. Merge feature/login dans main.
5. Supprime la branche feature/login.
```

<details>
<summary>Solution</summary>

```bash
git checkout -b feature/login
echo "login form" > login.html
git add login.html && git commit -m "Add login form"
echo "login logic" > login.js
git add login.js && git commit -m "Add login logic"

git checkout main
echo "update" >> README.md
git add README.md && git commit -m "Update README on main"

git merge feature/login
# Si pas de conflit → merge commit automatique

git branch -d feature/login
```
</details>

---

### Exercice 2.2 — Résolution de conflits

```
Tâches :
1. Sur main, crée un fichier config.txt avec "port=3000".
2. Crée une branche "feature/port" et change le port en 4000.
3. Retourne sur main et change le port en 5000.
4. Tente de merger feature/port → conflit !
5. Résous le conflit manuellement, puis termine le merge.
```

<details>
<summary>Solution</summary>

```bash
echo "port=3000" > config.txt
git add config.txt && git commit -m "Add config"

git checkout -b feature/port
echo "port=4000" > config.txt
git add config.txt && git commit -m "Change port to 4000"

git checkout main
echo "port=5000" > config.txt
git add config.txt && git commit -m "Change port to 5000"

git merge feature/port
# CONFLICT in config.txt

# Le fichier contient :
# <<<<<<< HEAD
# port=5000
# =======
# port=4000
# >>>>>>> feature/port

# Éditer manuellement pour garder la valeur souhaitée :
echo "port=5000" > config.txt
git add config.txt
git commit -m "Merge feature/port, keep port 5000"
```
</details>

---

### Exercice 2.3 — Git stash

```
Contexte : Tu es en plein travail sur une feature quand on te demande un hotfix urgent.

Tâches :
1. Modifie des fichiers sur ta branche feature (ne commite PAS).
2. Stash tes modifications.
3. Bascule sur main, fais le hotfix, commite.
4. Reviens sur ta branche feature.
5. Récupère tes modifications stashées et continue.
```

<details>
<summary>Solution</summary>

```bash
git checkout -b feature/dashboard
echo "work in progress" >> dashboard.html
# Ne pas commiter !

git stash save "WIP dashboard"
git checkout main
echo "hotfix" >> app.py
git add app.py && git commit -m "Hotfix: fix critical bug"

git checkout feature/dashboard
git stash pop
# dashboard.html a retrouvé ses modifications
```

Commandes utiles :
```bash
git stash list          # voir tous les stashs
git stash show -p       # voir le contenu du dernier stash
git stash drop stash@{0}  # supprimer un stash
```
</details>

---

### Exercice 2.4 — Rebase simple

```
Tâches :
1. Crée une branche feature avec 2 commits.
2. Pendant ce temps, main avance de 2 commits.
3. Au lieu de merger, rebase ta feature sur main.
4. Explique la différence entre merge et rebase dans ce cas.
```

<details>
<summary>Solution</summary>

```bash
git checkout main
echo "base" > base.txt && git add base.txt && git commit -m "Base"

git checkout -b feature/clean-history
echo "feat1" > f1.txt && git add f1.txt && git commit -m "Feature commit 1"
echo "feat2" > f2.txt && git add f2.txt && git commit -m "Feature commit 2"

git checkout main
echo "main1" > m1.txt && git add m1.txt && git commit -m "Main commit 1"
echo "main2" > m2.txt && git add m2.txt && git commit -m "Main commit 2"

git checkout feature/clean-history
git rebase main
# Les commits de feature sont "rejoués" après les commits de main
# → historique linéaire, pas de merge commit
```

**Différence :**
- `merge` : crée un commit de merge, conserve l'historique non-linéaire
- `rebase` : réécrit l'historique pour le rendre linéaire, pas de merge commit
</details>

---

### Exercice 2.5 — Git log avancé

```
Tâches :
1. Crée un historique avec au moins 10 commits sur plusieurs branches.
2. Affiche le log en graphe avec une ligne par commit.
3. Filtre les commits par auteur.
4. Filtre les commits des 7 derniers jours.
5. Cherche un commit qui contient un mot spécifique dans son message.
6. Cherche un commit qui a modifié une ligne contenant un mot spécifique (pickaxe).
```

<details>
<summary>Solution</summary>

```bash
# Graph compact
git log --oneline --graph --all --decorate

# Par auteur
git log --author="Ines"

# Par date
git log --since="7 days ago"
git log --after="2024-01-01" --before="2024-02-01"

# Recherche dans les messages
git log --grep="fix"

# Pickaxe : trouve le commit qui a ajouté/supprimé "SECRET_KEY"
git log -S "SECRET_KEY" --oneline

# Encore plus puissant : regex dans le diff
git log -G "port=[0-9]+" --oneline
```
</details>

---

## Niveau 3 : Avancé

### Exercice 3.1 — Rebase interactif

```
Contexte : Tu as 5 commits sur ta branche feature. Certains sont brouillons.

Tâches :
1. Crée 5 commits :
   - "WIP: start login"
   - "fix typo"
   - "WIP: continue login"
   - "oops forgot file"
   - "Login feature complete"
2. Utilise rebase interactif pour :
   - Squash "fix typo" dans le premier commit
   - Squash "oops forgot file" dans le 3ème commit
   - Reformule les messages restants proprement
3. Résultat : 2-3 commits propres.
```

<details>
<summary>Solution</summary>

```bash
# Après avoir créé les 5 commits :
git rebase -i HEAD~5

# L'éditeur s'ouvre avec :
# pick aaa1111 WIP: start login
# pick bbb2222 fix typo
# pick ccc3333 WIP: continue login
# pick ddd4444 oops forgot file
# pick eee5555 Login feature complete

# Modifier en :
# reword aaa1111 WIP: start login
# fixup  bbb2222 fix typo
# reword ccc3333 WIP: continue login
# fixup  ddd4444 oops forgot file
# pick   eee5555 Login feature complete

# Commandes rebase interactif :
# pick   = garder tel quel
# reword = garder mais changer le message
# squash = fusionner avec le précédent (combine les messages)
# fixup  = fusionner avec le précédent (jette le message)
# drop   = supprimer le commit
# edit   = arrêter pour modifier le commit
```
</details>

---

### Exercice 3.2 — Cherry-pick

```
Contexte : Un bugfix a été fait sur une branche feature mais tu en as besoin
immédiatement sur main sans merger toute la feature.

Tâches :
1. Sur feature/big-refactor, fais 5 commits dont 1 qui est un bugfix critique.
2. Identifie le hash du commit bugfix.
3. Cherry-pick ce commit sur main.
4. Vérifie que main a le fix mais pas les autres commits de la feature.
```

<details>
<summary>Solution</summary>

```bash
git checkout feature/big-refactor
# ... 5 commits dont : abc1234 "Fix: null pointer in auth module"

git checkout main
git cherry-pick abc1234

# Si conflit :
git cherry-pick --continue   # après résolution
git cherry-pick --abort       # pour annuler

# Cherry-pick sans commiter (juste appliquer les changements) :
git cherry-pick --no-commit abc1234
```
</details>

---

### Exercice 3.3 — Git bisect

```
Contexte : Un bug a été introduit quelque part dans les 20 derniers commits.
Tu ne sais pas lequel.

Tâches :
1. Crée un script qui simule un bug introduit au commit N.
2. Utilise git bisect pour trouver le commit coupable.
3. Automatise bisect avec un script de test.
```

<details>
<summary>Solution</summary>

```bash
# Méthode manuelle :
git bisect start
git bisect bad                  # le commit actuel est buggé
git bisect good v1.0            # ce tag/commit était OK

# Git checkout un commit au milieu. Teste, puis :
git bisect good   # si ce commit n'a pas le bug
git bisect bad    # si ce commit a le bug
# Répéter jusqu'à trouver le coupable.

git bisect reset  # revenir à l'état normal

# Méthode automatisée :
git bisect start HEAD v1.0
git bisect run ./test-script.sh
# Le script doit retourner 0 (good) ou 1 (bad)
# Git trouve automatiquement le commit coupable en O(log n)
```

Exemple de script de test :
```bash
#!/bin/bash
# test-script.sh
python -c "from app import calculate; assert calculate(2,3) == 5"
```
</details>

---

### Exercice 3.4 — Reflog et récupération

```
Contexte : Tu as fait une erreur catastrophique (reset --hard, branche supprimée, etc.)
et tu veux récupérer ton travail.

Tâches :
1. Crée 3 commits importants sur une branche.
2. Supprime la branche (sans merger).
3. Récupère la branche et ses commits en utilisant le reflog.
4. Scénario 2 : fais un git reset --hard qui supprime 2 commits.
5. Récupère ces commits perdus via reflog.
```

<details>
<summary>Solution</summary>

```bash
# Scénario 1 : branche supprimée
git checkout -b feature/important
echo "critical code" > critical.py
git add critical.py && git commit -m "Add critical code"
git checkout main
git branch -D feature/important  # Supprimée !

git reflog
# Trouver le hash du dernier commit de la branche, ex: abc1234
git checkout -b feature/important abc1234
# Branche récupérée !

# Scénario 2 : reset --hard
git reset --hard HEAD~2  # 2 commits perdus !

git reflog
# abc1234 HEAD@{1}: commit: le commit perdu
git reset --hard abc1234
# Commits restaurés !
```

**Règle d'or** : le reflog garde l'historique pendant 90 jours par défaut.
Tant que tu n'as pas fait `git gc`, tes données sont récupérables.
</details>

---

### Exercice 3.5 — Submodules

```
Tâches :
1. Crée un dépôt "shared-lib" avec du code réutilisable.
2. Ajoute-le comme submodule dans ton projet principal.
3. Fais des modifications dans le submodule, commite et push.
4. Dans le projet parent, mets à jour la référence du submodule.
5. Clone le projet parent depuis zéro et initialise les submodules.
```

<details>
<summary>Solution</summary>

```bash
# Ajouter un submodule
git submodule add https://github.com/user/shared-lib.git libs/shared

# Le projet parent a maintenant :
# - .gitmodules (config)
# - libs/shared/ (le contenu du submodule)

# Modifier le submodule
cd libs/shared
echo "new feature" >> lib.py
git add lib.py && git commit -m "Add feature to shared lib"
git push

# Dans le parent, mettre à jour la référence
cd ../..
git add libs/shared
git commit -m "Update shared-lib submodule"

# Cloner avec submodules
git clone --recurse-submodules https://github.com/user/project.git

# Ou après un clone normal :
git submodule init
git submodule update

# Mettre à jour tous les submodules vers leur dernier commit
git submodule update --remote --merge
```
</details>

---

### Exercice 3.6 — Git hooks

```
Tâches :
1. Crée un pre-commit hook qui :
   - Vérifie qu'aucun fichier .env n'est staged
   - Lance un linter (ex: flake8 ou eslint)
   - Bloque le commit si le linter échoue
2. Crée un commit-msg hook qui :
   - Vérifie que le message suit le format "type: description"
   - Types autorisés : feat, fix, docs, refactor, test, chore
3. Crée un pre-push hook qui lance les tests.
```

<details>
<summary>Solution</summary>

```bash
# .git/hooks/pre-commit
#!/bin/bash
# Vérifier qu'aucun .env n'est staged
if git diff --cached --name-only | grep -q '\.env'; then
    echo "ERREUR: fichier .env détecté dans le staging !"
    echo "Utilisez: git reset HEAD .env"
    exit 1
fi

# Linter sur les fichiers staged
STAGED_PY=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')
if [ -n "$STAGED_PY" ]; then
    flake8 $STAGED_PY
    if [ $? -ne 0 ]; then
        echo "ERREUR: le linter a échoué. Corrigez avant de commiter."
        exit 1
    fi
fi
```

```bash
# .git/hooks/commit-msg
#!/bin/bash
MSG=$(cat "$1")
PATTERN="^(feat|fix|docs|refactor|test|chore): .{3,}"

if ! echo "$MSG" | grep -qE "$PATTERN"; then
    echo "ERREUR: format de message invalide."
    echo "Format attendu: type: description"
    echo "Types: feat, fix, docs, refactor, test, chore"
    exit 1
fi
```

```bash
# .git/hooks/pre-push
#!/bin/bash
echo "Running tests before push..."
python -m pytest tests/
if [ $? -ne 0 ]; then
    echo "ERREUR: les tests échouent. Push annulé."
    exit 1
fi
```

```bash
# Rendre les hooks exécutables
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/commit-msg
chmod +x .git/hooks/pre-push
```
</details>

---

## Niveau 4 : Très Avancé

### Exercice 4.1 — Réécriture d'historique avec filter-branch / filter-repo

```
Contexte : Un développeur a accidentellement commité un mot de passe
dans un fichier il y a 50 commits. Le fichier a été modifié depuis
mais le secret est dans l'historique.

Tâches :
1. Simule la situation : commite un fichier avec un secret, fais 10 commits après.
2. Vérifie que le secret est visible dans l'historique (git log -S).
3. Utilise git-filter-repo pour supprimer le secret de TOUT l'historique.
4. Vérifie que le secret n'est plus nulle part.
5. Explique pourquoi filter-branch est déprécié et pourquoi
   filter-repo est préférable.
```

<details>
<summary>Solution</summary>

```bash
# Installer git-filter-repo
pip install git-filter-repo

# Vérifier que le secret est dans l'historique
git log -S "MOT_DE_PASSE_SECRET" --all

# Option 1 : Supprimer un fichier entier de tout l'historique
git filter-repo --invert-paths --path secrets.txt

# Option 2 : Remplacer un texte dans tout l'historique
git filter-repo --replace-text <(echo 'MOT_DE_PASSE_SECRET==>REDACTED')

# Option 3 : Supprimer un blob spécifique
BLOB_HASH=$(git rev-parse HEAD~10:secrets.txt)
git filter-repo --strip-blobs-with-ids <(echo $BLOB_HASH)

# Après filter-repo, forcer le push
git push origin --force --all
git push origin --force --tags

# Vérifier
git log -S "MOT_DE_PASSE_SECRET" --all
# Aucun résultat = succès
```

**Pourquoi filter-repo > filter-branch :**
- filter-branch est **extrêmement lent** (shell sur chaque commit)
- filter-branch ne nettoie pas les refs de backup correctement
- filter-repo est écrit en Python, 10-100x plus rapide
- filter-repo gère correctement les cas edge (tags, replace refs, grafts)
</details>

---

### Exercice 4.2 — Stratégies de merge avancées

```
Tâches :
1. Crée un conflit complexe entre 2 branches (même fichier, mêmes lignes).
2. Résous avec la stratégie "ours" (garder notre version).
3. Résous avec la stratégie "theirs" (garder leur version).
4. Utilise un merge avec --no-ff et explique pourquoi.
5. Utilise un octopus merge (merger 3+ branches simultanément).
6. Explique la différence entre stratégie "ours" et option "-X ours".
```

<details>
<summary>Solution</summary>

```bash
# Stratégie ours (ignore complètement l'autre branche)
git merge -s ours feature/old-approach
# Le résultat est EXACTEMENT le contenu de main
# Utile pour marquer une branche comme "mergée" sans prendre son code

# Option -X ours (résout les conflits en faveur de HEAD)
git merge -X ours feature/branch
# Les fichiers sans conflit sont mergés normalement
# Seuls les conflits sont résolus en faveur de HEAD

# Option -X theirs
git merge -X theirs feature/branch
# Conflits résolus en faveur de la branche mergée

# --no-ff : force un merge commit même si fast-forward est possible
git merge --no-ff feature/clean
# Préserve l'information qu'une branche a existé
# Utile pour garder un historique clair des features

# Octopus merge (3+ branches)
git merge feature/a feature/b feature/c
# Crée un seul merge commit avec 4 parents
# Ne fonctionne que s'il n'y a PAS de conflits
```
</details>

---

### Exercice 4.3 — Worktrees

```
Contexte : Tu veux travailler sur 2 branches simultanément
sans faire de stash ou de commit temporaire.

Tâches :
1. Crée un worktree lié pour la branche "hotfix".
2. Travaille dans le worktree hotfix pendant que le main worktree
   reste sur ta feature.
3. Commite dans les deux worktrees.
4. Supprime le worktree quand tu as fini.
```

<details>
<summary>Solution</summary>

```bash
# Créer un worktree pour la branche hotfix
git worktree add ../project-hotfix hotfix/critical

# Maintenant tu as 2 répertoires :
# ./mon-projet/          → branche feature (inchangée)
# ../project-hotfix/     → branche hotfix/critical

# Travailler dans le hotfix
cd ../project-hotfix
echo "fix" >> app.py
git add app.py && git commit -m "Fix critical bug"

# Revenir au projet principal
cd ../mon-projet
# Toujours sur la branche feature !

# Lister les worktrees
git worktree list

# Supprimer un worktree
git worktree remove ../project-hotfix

# Nettoyer les worktrees invalides
git worktree prune
```
</details>

---

### Exercice 4.4 — Git internals : les objets

```
Tâches :
1. Crée un fichier et commite-le.
2. Explore le dossier .git/objects/ et identifie les types d'objets.
3. Utilise git cat-file pour inspecter :
   - Un blob (contenu d'un fichier)
   - Un tree (structure d'un répertoire)
   - Un commit (métadonnées d'un commit)
4. Explique le modèle de stockage de Git (DAG).
5. Crée manuellement un blob avec git hash-object.
6. Recrée un commit "à la main" avec les plumbing commands.
```

<details>
<summary>Solution</summary>

```bash
# Voir le type d'un objet
git cat-file -t HEAD
# commit

# Voir le contenu d'un commit
git cat-file -p HEAD
# tree 4b825dc642cb6eb9a060e54bf899d15f7e7d7b0e
# parent abc1234...
# author Ines <email> 1700000000 +0100
# committer Ines <email> 1700000000 +0100
#
# Message du commit

# Voir le tree
TREE=$(git cat-file -p HEAD | grep tree | cut -d' ' -f2)
git cat-file -p $TREE
# 100644 blob abc123... README.md
# 040000 tree def456... src/

# Voir un blob
git cat-file -p abc123
# (contenu du fichier)

# Créer un blob manuellement
echo "Hello Git" | git hash-object -w --stdin
# Retourne un hash SHA-1

# Créer un tree manuellement
git update-index --add --cacheinfo 100644,<blob-hash>,hello.txt
TREE_HASH=$(git write-tree)

# Créer un commit manuellement
COMMIT_HASH=$(echo "Manual commit" | git commit-tree $TREE_HASH)
git update-ref refs/heads/manual-branch $COMMIT_HASH
```

**Modèle de stockage Git :**
```
commit → tree → blob
  │        │
  │        ├── blob (fichier)
  │        ├── tree (sous-répertoire) → blob
  │        └── blob (fichier)
  │
  └── parent commit → tree → ...

Chaque objet est identifié par son SHA-1.
C'est un DAG (Directed Acyclic Graph) : chaque commit pointe
vers son/ses parent(s), jamais de cycle.
```
</details>

---

### Exercice 4.5 — Rebase avancé avec --onto

```
Contexte : Tu as une branche feature-B basée sur feature-A.
feature-A a été refusée. Tu veux rebaser feature-B directement sur main.

Tâches :
1. Crée main → feature-A (3 commits) → feature-B (2 commits).
2. Utilise git rebase --onto pour déplacer feature-B sur main,
   en excluant les commits de feature-A.
3. Vérifie que feature-B ne contient que ses propres commits.
```

<details>
<summary>Solution</summary>

```bash
# Situation initiale :
# main: A─B─C
#              \
#  feature-A:   D─E─F
#                      \
#    feature-B:         G─H

# On veut :
# main: A─B─C
#            \
# feature-B:  G'─H'

git rebase --onto main feature-A feature-B
# Syntaxe : git rebase --onto <nouvelle-base> <ancienne-base> <branche>
# "Prends les commits de feature-B qui ne sont PAS dans feature-A,
#  et rejoue-les sur main"

git log --oneline
# Seulement G' et H' après C
```
</details>

---

### Exercice 4.6 — Git blame avancé et investigation

```
Tâches :
1. Utilise git blame avec -w (ignorer les changements de whitespace).
2. Utilise git blame -M (détecter les déplacements de code dans un fichier).
3. Utilise git blame -C (détecter le code copié depuis d'autres fichiers).
4. Utilise git blame -L 10,20 pour limiter à des lignes spécifiques.
5. Utilise git log -L :functionName:file.py pour voir l'évolution
   d'une fonction à travers l'historique.
```

<details>
<summary>Solution</summary>

```bash
# Blame basique
git blame app.py

# Ignorer les changements de whitespace
git blame -w app.py

# Détecter le code déplacé dans le même fichier
git blame -M app.py

# Détecter le code copié depuis d'autres fichiers
git blame -C app.py
git blame -C -C app.py    # recherche plus agressive (dans tous les commits)
git blame -C -C -C app.py # encore plus agressif (dans tous les fichiers)

# Limiter aux lignes 10-20
git blame -L 10,20 app.py

# Évolution d'une fonction
git log -L :calculate:math_utils.py
# Montre chaque commit qui a modifié la fonction calculate()
# avec le diff de chaque modification

# Ignorer certains commits (ex: reformatage massif)
echo "abc1234" >> .git-blame-ignore-revs
git config blame.ignoreRevsFile .git-blame-ignore-revs
git blame app.py  # le commit abc1234 sera ignoré
```
</details>

---

## Niveau 5 : Expert / Deep

### Exercice 5.1 — Implémentation d'un merge driver custom

```
Contexte : Ton projet contient un fichier version.json qui crée
systématiquement des conflits lors des merges.

Tâches :
1. Crée un merge driver custom qui résout automatiquement les conflits
   sur version.json en prenant toujours la version la plus haute.
2. Configure .gitattributes pour utiliser ce driver.
3. Teste avec un conflit réel.
```

<details>
<summary>Solution</summary>

```bash
# Créer le script de merge custom
cat > /usr/local/bin/merge-version.sh << 'SCRIPT'
#!/bin/bash
# $1 = ancêtre commun, $2 = version courante (ours), $3 = version mergée (theirs)
ANCESTOR=$1
OURS=$2
THEIRS=$3

VERSION_OURS=$(python3 -c "import json; print(json.load(open('$OURS'))['version'])")
VERSION_THEIRS=$(python3 -c "import json; print(json.load(open('$THEIRS'))['version'])")

# Comparer les versions (semver simplifié)
HIGHEST=$(echo -e "$VERSION_OURS\n$VERSION_THEIRS" | sort -V | tail -1)

python3 -c "
import json
data = json.load(open('$OURS'))
data['version'] = '$HIGHEST'
json.dump(data, open('$OURS', 'w'), indent=2)
"
exit 0  # 0 = conflit résolu
SCRIPT
chmod +x /usr/local/bin/merge-version.sh
```

```bash
# .gitattributes
version.json merge=version-merge
```

```bash
# .git/config (ou git config)
git config merge.version-merge.name "Auto-merge version.json"
git config merge.version-merge.driver "merge-version.sh %O %A %B"
# %O = ancestor, %A = ours, %B = theirs
```
</details>

---

### Exercice 5.2 — Git replace et grafts

```
Contexte : Ton dépôt a un historique de 10 000 commits. Tu veux
"couper" l'historique pour les clones tout en gardant l'historique
complet accessible.

Tâches :
1. Crée un shallow boundary avec un graft point.
2. Utilise git replace pour substituer un commit par un autre.
3. Fais un "split history" : historique récent dans un dépôt,
   historique ancien dans un autre, avec possibilité de reconnecter.
```

<details>
<summary>Solution</summary>

```bash
# Étape 1 : Identifier le commit de coupure
CUT_POINT=$(git log --oneline | tail -n +1000 | head -1 | cut -d' ' -f1)

# Étape 2 : Créer un commit "racine" qui remplace l'historique ancien
TREE=$(git cat-file -p $CUT_POINT | grep tree | cut -d' ' -f2)
NEW_ROOT=$(echo "Historical boundary" | git commit-tree $TREE)

# Étape 3 : Remplacer le commit
git replace $CUT_POINT $NEW_ROOT

# Maintenant git log s'arrête au NEW_ROOT
# L'ancien historique est toujours là dans les objets

# Pour partager les replace refs :
git push origin 'refs/replace/*'

# Pour les récupérer :
git fetch origin 'refs/replace/*:refs/replace/*'

# Pour voir les remplacements actifs :
git replace -l

# Pour supprimer un remplacement :
git replace -d $CUT_POINT

# Split history réel avec filter-repo :
# Garder seulement les 1000 derniers commits
git filter-repo --refs HEAD~1000..HEAD

# L'ancien repo peut être gardé comme archive
# et reconnecter avec git replace si besoin
```
</details>

---

### Exercice 5.3 — Protocole Git et transfer internals

```
Tâches :
1. Configure un serveur Git via SSH (bare repository).
2. Configure un serveur Git via le protocole HTTP smart.
3. Active et configure les pack negotiations (multi-pack-index).
4. Explore et explique le protocole wire v2 de Git.
5. Configure commit signing avec GPG et vérifie les signatures.
6. Active et utilise les partial clones et les sparse checkouts.
```

<details>
<summary>Solution</summary>

```bash
# 1. Bare repository via SSH
ssh server "git init --bare /srv/git/project.git"
git remote add origin ssh://user@server/srv/git/project.git
git push -u origin main

# 2. HTTP smart
# Sur le serveur (avec git-http-backend et nginx/apache)
# nginx.conf :
# location ~ ^/git(/.*) {
#     fastcgi_pass unix:/var/run/fcgiwrap.socket;
#     fastcgi_param SCRIPT_FILENAME /usr/lib/git-core/git-http-backend;
#     fastcgi_param GIT_HTTP_EXPORT_ALL "";
#     fastcgi_param GIT_PROJECT_ROOT /srv/git;
#     fastcgi_param PATH_INFO $1;
# }

# 3. Multi-pack-index
git multi-pack-index write
git multi-pack-index verify
# Accélère les lookups dans les repos avec beaucoup de packfiles

# 4. Protocol v2
git config --global protocol.version 2
GIT_TRACE_PACKET=1 git ls-remote origin
# Le protocol v2 est basé sur des capabilities :
# - ls-refs : lister les refs côté serveur
# - fetch : négociation de pack optimisée
# - server-option : options côté serveur

# 5. GPG signing
gpg --gen-key
git config --global user.signingkey ABC12345
git config --global commit.gpgsign true
git commit -S -m "Signed commit"
git log --show-signature
git verify-commit HEAD

# 6. Partial clone + sparse checkout
git clone --filter=blob:none origin  # clone sans les blobs
git clone --filter=tree:0 origin     # clone sans trees ni blobs

git sparse-checkout init --cone
git sparse-checkout set src/core src/utils
# Seuls src/core/ et src/utils/ sont checkout
# Le reste est téléchargé à la demande (lazy fetch)

git sparse-checkout list
git sparse-checkout disable
```
</details>

---

### Exercice 5.4 — Écrire un custom Git command

```
Tâches :
1. Crée un script "git-standup" qui affiche les commits de l'utilisateur
   des dernières 24h sur toutes les branches.
2. Crée un script "git-delete-merged" qui supprime toutes les branches
   locales déjà mergées dans main (avec confirmation).
3. Crée un script "git-guilt" qui montre les lignes ajoutées/supprimées
   par auteur entre 2 commits.
```

<details>
<summary>Solution</summary>

```bash
#!/bin/bash
# git-standup — placer dans PATH
# Usage: git standup [days] [author]

DAYS=${1:-1}
AUTHOR=${2:-$(git config user.name)}

git log \
  --all \
  --since="${DAYS} days ago" \
  --author="$AUTHOR" \
  --format="%C(yellow)%h %C(green)%ad %C(blue)%s %C(red)(%an)%C(reset)" \
  --date=short \
  --no-merges
```

```bash
#!/bin/bash
# git-delete-merged — placer dans PATH
# Usage: git delete-merged [base-branch]

BASE=${1:-main}

MERGED=$(git branch --merged "$BASE" | grep -v "^\*" | grep -v "$BASE" | sed 's/^ *//')

if [ -z "$MERGED" ]; then
    echo "Aucune branche mergée à supprimer."
    exit 0
fi

echo "Branches mergées dans $BASE :"
echo "$MERGED"
echo ""
read -p "Supprimer ces branches ? (y/N) " confirm

if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
    echo "$MERGED" | xargs git branch -d
    echo "Done."
fi
```

```bash
#!/bin/bash
# git-guilt — placer dans PATH
# Usage: git guilt <since> <until>

SINCE=${1:-HEAD~10}
UNTIL=${2:-HEAD}

git log --numstat --format="%an" "$SINCE..$UNTIL" | \
  awk '
    /^[a-zA-Z]/ { author = $0; next }
    /^[0-9]/ { added[author] += $1; removed[author] += $2 }
    END {
      for (a in added) {
        printf "%s: +%d / -%d (net: %d)\n", a, added[a], removed[a], added[a]-removed[a]
      }
    }
  ' | sort -t: -k2 -rn
```

```bash
# Installation : placer les scripts dans le PATH
chmod +x git-standup git-delete-merged git-guilt
mv git-standup git-delete-merged git-guilt /usr/local/bin/

# Utilisation :
git standup          # commits des dernières 24h
git standup 7        # des 7 derniers jours
git delete-merged    # supprimer branches mergées
git guilt HEAD~20 HEAD  # qui a écrit quoi sur les 20 derniers commits
```
</details>

---

### Exercice 5.5 — Debugging avec Git : scénario complet

```
Contexte : Tu reçois un rapport de bug en production. Le bug n'existait
pas il y a 2 semaines. Le dépôt a 150 commits depuis.

Tâches :
1. Utilise git log --all --oneline --graph pour avoir une vue d'ensemble.
2. Utilise git bisect automatisé pour trouver le commit coupable.
3. Le commit coupable est un merge commit. Utilise git log -m -p
   pour voir les changements introduits par le merge.
4. Utilise git diff <merge>^1 <merge> et git diff <merge>^2 <merge>
   pour comprendre les deux côtés du merge.
5. Crée un revert du merge commit (attention au -m 1).
6. Explique pourquoi reverter un merge est dangereux et comment
   "re-merger" la branche plus tard.
```

<details>
<summary>Solution</summary>

```bash
# 1. Vue d'ensemble
git log --all --oneline --graph --since="2 weeks ago"

# 2. Bisect automatisé
git bisect start
git bisect bad HEAD
git bisect good HEAD~150
git bisect run python -m pytest tests/test_critical.py
# Résultat : abc1234 is the first bad commit (un merge commit)

git bisect reset

# 3. Voir les changements du merge commit
git log -m -p -1 abc1234
# -m : traite le merge comme 2 diffs séparés

# 4. Comprendre les deux côtés
git diff abc1234^1 abc1234   # diff entre 1er parent et merge
git diff abc1234^2 abc1234   # diff entre 2ème parent et merge
# ^1 = la branche qui recevait le merge (main)
# ^2 = la branche qui était mergée (feature)

# 5. Revert du merge
git revert -m 1 abc1234
# -m 1 signifie "garder le 1er parent (main) comme référence"
# Cela annule les changements venus de la feature branch

# 6. Le piège du revert de merge :
# Après le revert, la branche feature est toujours considérée comme
# "déjà mergée". Si on tente de re-merger la feature :
git merge feature/broken
# → "Already up to date" car Git pense que c'est fait !

# Solution : reverter le revert AVANT de re-merger
git revert <hash-du-revert>
git merge feature/broken
# Maintenant le merge reprend les changements originaux
```
</details>

---

### Exercice 5.6 — Monorepo et stratégies avancées

```
Tâches :
1. Configure un monorepo avec sparse-checkout pour que chaque équipe
   ne checkout que son dossier.
2. Implémente des path-based CODEOWNERS.
3. Configure des merge queues avec des CI checks par path.
4. Utilise git subtree (alternative aux submodules) pour extraire
   un dossier en repo séparé tout en gardant l'historique.
5. Configure scalar (ou git maintenance) pour optimiser un gros repo.
```

<details>
<summary>Solution</summary>

```bash
# 1. Sparse checkout par équipe
git clone --no-checkout --filter=blob:none https://github.com/org/monorepo.git
cd monorepo
git sparse-checkout init --cone
git sparse-checkout set packages/team-a shared/

# 2. CODEOWNERS
cat > .github/CODEOWNERS << 'EOF'
# Chaque ligne : pattern owner(s)
/packages/team-a/  @org/team-a
/packages/team-b/  @org/team-b
/shared/           @org/platform
*.sql              @org/dba
/docs/             @org/docs-team
EOF

# 3. Subtree : extraire un dossier en repo séparé
# Ajouter un sous-projet
git subtree add --prefix=libs/utils https://github.com/org/utils.git main --squash

# Mettre à jour le sous-projet
git subtree pull --prefix=libs/utils https://github.com/org/utils.git main --squash

# Pousser des changements vers le repo du sous-projet
git subtree push --prefix=libs/utils https://github.com/org/utils.git main

# Extraire un dossier avec son historique complet
git subtree split --prefix=packages/team-a -b team-a-standalone
git push https://github.com/org/team-a-repo.git team-a-standalone:main

# 4. Git maintenance (intégré dans Git moderne)
git maintenance start
# Configure des tâches automatiques :
# - gc : garbage collection
# - commit-graph : accélérer les traversals
# - prefetch : fetch en arrière-plan
# - loose-objects : consolider les objets
# - incremental-repack : repacker les packfiles
# - pack-refs : consolider les refs

git maintenance run --task=gc
git maintenance run --task=commit-graph

# Scalar (pour les très gros repos, ex: Windows, Chromium)
scalar clone https://github.com/org/huge-monorepo.git
# Active automatiquement : sparse-checkout, partial clone,
# file system monitor, commit-graph, multi-pack-index
```
</details>

---
