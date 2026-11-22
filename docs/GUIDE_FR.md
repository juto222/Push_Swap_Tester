# Documentation — Push Swap Tester

## 1. Objectif

Ce programme Python sert à tester automatiquement un exécutable `push_swap` du projet 42. Il ne remplace pas `push_swap` : il **génère des entrées**, **exécute le programme C**, **fait vérifier ses instructions par un checker** et **résume les résultats**.

Le testeur est conçu pour être lancé **dans le terminal**. Il utilise uniquement des modules Python standards.

## 2. Préparer l'environnement

Il faut :

- Python 3 ;
- l'exécutable `push_swap` compilé, avec l'option `--adaptive` ;
- un checker compatible appelé `checker_Mac` sur macOS ou `checker_linux` sur Linux ;
- les fichiers Python `generator.py` et `testerr.py` (ce dernier doit exposer `argerr()`).

Exemple d'arborescence :

```text
Push_swap/
├── push_swap
├── checker_Mac
└── pushswaptester/
    ├── generator.py
    └── testerr.py
```

Depuis le dossier `Push_swap`, lancer :

```bash
python3 pushswaptester/generator.py
```

**Important :** `./push_swap` est recherché dans le **répertoire de travail du terminal**. Si tu lances le script depuis un autre dossier, ce chemin peut ne pas fonctionner.

## 3. Lancer une campagne de tests

Le script demande :

```text
How many test per size :
```

Tu entres un entier positif, par exemple `100`.

Avec `NB_ARG = [10, 20, 100, 500]`, le programme prévoit 100 essais sur 10 nombres, puis 100 sur 20, puis 100 sur 100, puis 100 sur 500, soit **400 tests aléatoires** au total. Pour **chaque essai**, une nouvelle combinaison de nombres est générée.

Les tests d'arguments de `testerr.py` sont lancés en premier via `argerr()`.

## 4. Déroulement d'un test

1. Le générateur crée des entiers aléatoires uniques entre `INT_MIN` et `INT_MAX`.
2. Il prépare les arguments : exécutable, option `--adaptive`, puis nombres sous forme de chaînes.
3. `subprocess.run()` lance `push_swap` et capture les instructions affichées sur `stdout`.
4. `splitlines()` sépare le texte en lignes : normalement, une ligne correspond à une instruction.
5. Le checker reçoit **les mêmes nombres de départ**, ainsi que les instructions par son **entrée standard** (`input` de `subprocess.run()`).
6. Le testeur consulte la réponse du checker : `OK` ou `KO`.
7. Il conserve le nombre d'opérations pour les tests réussis et calcule les statistiques de la taille en cours.

### Pourquoi les mêmes nombres pour le checker ?

Les instructions seules ne suffisent pas. Le checker doit connaître la **pile initiale** sur laquelle appliquer les opérations. Il doit donc recevoir les mêmes nombres, dans le même ordre, que `push_swap`.

## 5. Rôle des fonctions

| Fonction | Rôle |
| --- | --- |
| `know_os()` | Renvoie le système signalé par `platform.system()` (`Darwin` pour macOS, `Linux` pour Linux). |
| `checker_ps(user)` | Choisit un chemin d'exécutable checker selon l'OS. |
| `generate_numbers(i, NB_ARG)` | Génère une liste de nombres uniques de la taille indiquée par `NB_ARG[i]`. |
| `test_forsize(...)` | Répète les essais pour une taille, exécute `push_swap` et le checker, enregistre les résultats. |
| `compteur(...)` | Ajoute un résultat à la liste des `OK` ou à celle des `KO` selon la réponse du checker. |
| `env_gennbr_to_ps(...)` | Parcourt les différentes tailles et affiche le bilan de chacune. |
| `argerr()` | Fonction importée de `testerr.py`, destinée aux tests des arguments invalides et particuliers. |

Cette documentation décrit l'architecture du script partagé. Si tu renommes les fonctions ou modifies leurs paramètres, adapte le tableau.

## 6. Modules Python utilisés

### `random`

`random.randint(INT_MIN, INT_MAX)` produit un entier aléatoire dans l'intervalle **bornes comprises**. Le script rejette les doublons avant de remplir la pile.

### `subprocess`

`subprocess.run()` lance un exécutable et attend sa fin. Les paramètres utilisés dans le projet sont :

- `capture_output=True` : récupère les flux de sortie ;
- `text=True` : traite ces sorties comme du texte ;
- `input=...` : transmet les instructions à l'entrée standard du checker.

L'objet renvoyé donne accès à `stdout`, `stderr` et `returncode`.

### `platform`

`platform.system()` indique le système d'exploitation. Attention, Fedora est aussi une distribution Linux : il ne sera pas distingué par le simple résultat `Linux`.

## 7. Comprendre les résultats

Exemple **fictif** :

```text
[Number 100]
OK : 100
KO : 0
Min ops : 620
Max ops : 710
Avg ops : 664.32
```

- `OK` : nombre d'essais validés par le checker ;
- `KO` : nombre d'essais non validés ;
- `Min ops` : plus petit nombre d'instructions parmi les essais retenus ;
- `Max ops` : plus grand nombre d'instructions ;
- `Avg ops` : moyenne du nombre d'instructions.

Le compte d'opérations mesure le **nombre d'instructions**, pas leur durée d'exécution. Si aucun essai n'est valide, les statistiques doivent être remplacées par un message approprié afin d'éviter une division par zéro ou un appel à `min()` sur une liste vide.

### `returncode` et `OK` ne sont pas la même chose

Un `returncode` nul indique généralement que le programme s'est terminé sans signaler d'erreur. **Cela ne prouve pas que la pile est triée.** C'est la réponse du checker qui valide le résultat.

## 8. Les tests d'arguments

Le module `testerr.py` peut tester des entrées telles que :

- nombres en double : `1 2 2 3` ;
- caractères invalides : `1 abc 2` ;
- dépassement de la plage des entiers : `2147483648` ou `-2147483649` ;
- options invalides : `--unknown` ;
- options incompatibles : `--simple --complex` ;
- doublon d'option : `--bench --bench` ;
- appel sans arguments.

Pour un test d'entrée **invalide**, un message `Error` approprié constitue normalement un **PASS du testeur**. Pour un appel **sans arguments**, le comportement attendu dans `push_swap` est normalement l'absence de sortie. Adapter les attentes aux exigences précises du sujet.

## 9. Problèmes fréquents

**`PermissionError`** : l'exécutable ne dispose peut-être pas des droits nécessaires, ou le chemin désigne un dossier / un mauvais fichier.

**`FileNotFoundError`** : le script ne trouve pas `./push_swap` ou le checker dans le répertoire de travail.

**Tous les tests sont `KO`** : vérifier que le checker reçoit bien les mêmes nombres et que `stdout` contient uniquement des instructions valides ; examiner également le code de retour du processus.

**Le script ne termine pas** : le code d'origine n'impose pas de `timeout` à `subprocess.run()`. Une boucle infinie dans un exécutable peut donc bloquer la campagne.

**Saisie non numérique** : `int(input(...))` peut lever `ValueError`. La vérification des saisies reste à renforcer.

## 10. Limites actuelles et idées d'amélioration

L'outil, dans sa forme actuelle, est volontairement simple. Il peut ensuite évoluer avec :

- des timeouts pour les exécutables ;
- une validation des entrées utilisateur ;
- des chemins configurables ;
- l'enregistrement des arguments ayant provoqué un `KO` ;
- la comparaison des stratégies sur une **même liste** ;
- une graine aléatoire (`seed`) pour reproduire les essais.

Ces pistes ne sont **pas** présentées comme des fonctionnalités déjà implémentées.

## 11. Références officielles

- `subprocess` : https://docs.python.org/3/library/subprocess.html
- `random` : https://docs.python.org/3/library/random.html
- `platform` : https://docs.python.org/3/library/platform.html
- Séquences et méthodes de chaînes (`splitlines`, `strip`) : https://docs.python.org/3/library/stdtypes.html
