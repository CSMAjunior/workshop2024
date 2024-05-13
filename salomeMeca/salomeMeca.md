
# Installation de salome_meca 

salome_meca est un container singularity, qui, modulo  l'installation de singularity, permet de l'exécuter sur toutes les plateformes.

Il y a donc deux étapes principales
- Installer singularity
- Installer le container contenant salome_meca

Le site officiel pour code_aster est salome_meca est https://code-aster.org/V2/spip.php?rubrique1.
La procédure d'installation est basée sur https://gitlab.com/codeaster-opensource-documentation/opensource-installation-development

Il y a deux containers disponibles (au choix):
- une version qui contient une version MPI de salome_meca et de code_aster (16.3)
- une version officielle qui contient uniquement salome_meca en version séquentielle

Une troisième version de salome_meca, utilisable uniquement sur Windows pourra être founie sur place (sur clef USB). Elle ne nécessite
aucune installation préalable.

## Installer Singularity

Le conteneur fourni est un conteneur Singularity. Il est compatible avec Singularity 3.6.4 et plus.

Tout d'abord, essayez d'installer Singularity à partir de votre gestionnaire de paquets (https://packages.debian.org/source/sid/singularity-container sous debian/ubuntu récent).
Sinon, il faut le compiler à partir de zéro.

Voir la procédure indiquée sur le site officiel https://docs.sylabs.io/guides/4.1/admin-guide/installation.html. 

- Linux : il existe un paquetage officiel ou non https://docs.sylabs.io/guides/4.1/admin-guide/installation.html#installation-on-linux. 
- Windows : il est préférable d'utiliser WSL2 https://gitlab.com/codeaster-opensource-documentation/opensource-installation-development/-/blob/main/install/installation_windows.md ou une machine virtuelle https://docs.sylabs.io/guides/4.1/admin-guide/installation.html#installation-on-windows-or-mac.
- Mac-os : il faut utiliser une machine virtuelle https://docs.sylabs.io/guides/4.1/admin-guide/installation.html#installation-on-windows-or-mac.

## Créer le répertoire d'installation

Cette documentation prend pour acquis que le répertoire d'installation du conteneur salome_meca se trouve dans le répertoire 
d'un utilisateur, tel que `$HOME/containers`. Le nom de ce répertoire peut bien sûr être modifié, mais il faut adapter les lignes de commande en conséquence.

Tout d'abord, créons le répertoire spécifié :

```bash
mkdir -p ${HOME}/containers
cd ${HOME}/containers
```

Sauf indication contraire, toutes les opérations ultérieures sont effectuées à l'intérieur de ce répertoire.

## Télécharger le container

Le Singularity Image File (SIF) doit être téléchargé localement. wget peut être
utilisé pour le télécharger directement depuis le site web de code_aster.

La version standard salome_meca 2022 + code_aster MPI (16.3) :

```bash
wget -c https://code-aster.org/FICHIERS/singularity/salome_meca_2022.1.0_lgpl_summer.sif
```

La version standard salome_meca 2022:

```bash
wget -c https://code-aster.org/FICHIERS/singularity/salome_meca-lgpl-2022.1.0-1-20221225-scibian-9.sif
```

La taille des fichiers est importante (6 GB) et il est préférable de prévoir suffisamment de temps pour ce téléchargement.
Si le téléchargement échoue pour une raison quelconque, il peut être poursuivi en utilisant l'option `wget -c`.

## Configuration du container

Un fichier de lancement salome_meca est situé dans le conteneur. Il faut donc
copier le fichier dans le répertoire de la machine locale. Un script a été préparé
à cet effet.

Il va de soit que les commandes suivantes doivent être modifiées suivant le container téléchargé.

```bash
singularity run --app install salome_meca_2022.1.0_lgpl_summer.sif
```

Vous devriez voir cette sortie dans votre terminal

```none
Installation successfully completed.
To start salome_meca, just use:
  .../containers/salome_meca_2022.1.0_lgpl_summer
or (in the installation directory):
  ./salome_meca_2022.1.0_lgpl_summer

If you want to check your configuration, use:
  singularity run --app check salome_meca_2022.1.0_lgpl_summer.sif
```

In order to display the different options of the launcher, one may use
`--help`:

```bash
./salome_meca_2022.1.0_lgpl_summer --help
```

Pour lancer salome_meca, il faut simplement utiliser cette commande:

```bash
./salome_meca_2022.1.0_lgpl_summer
```

## Test de l'installation

Par défaut, le dossier $HOME est monté automatiquement. Vous pouver ouvrir salome_meca en mode graphique avec

```bash
./salome_meca_2022.1.0_lgpl_summer
```

et pour utiliser en mode shell
```bash
./salome_meca_2022.1.0_lgpl_summer --shell
```

alors vous êtes dans un terminal.

Pour tester votre intallation, lancer le conteneur en mode shell (avec la commande précédente), 
puis aller dans le répertoire code_aster avec

```bash
cd /opt/public/code_aster
```
et lancer code_aster en mode python:

```bash
./bin/run_aster
```
Normallement, code_aster s'éxecute dans le terminal python avec l'output suivant;

```none
# ------------------------------------------------------------------------------------
Execution of code_aster
...
```
Importer le module code_aster
```python
import code_aster
```

Sortez avec
```python
exit()
```
Vous devriez avoir la sortie suivante

```none
...
------------------------------------------------------------------------------------
------- DIAGNOSTIC JOB : OK
------------------------------------------------------------------------------------
```

Le container fourni contient tous les outils (compilateurs par exemple) et les pré-requis nécessaires à la compilation et à
la modification de code_aster. Pour les aventuriers curieux ! 
Des conteneurs plus récents existents pour les versions de développement de code_aster.