#
# -*- Mode: Python; indent-tabs-mode: nil; tab-width: 4 -*-
#
################################################################################
# HEADING
################################################################################
#
# Author
#   The author of the script.
# Feature (Optional)
#   The 'Feature' contains the reference to the related Jira Nr. and
#   description to which this test case belongs. If the test case belongs to
#   more than one feature, the features have to be separated by a comma.
# Description
#   Description of the test case and the test procedure with the test goal.
# Modified by
#   N.A.
# Version
#   Current version of the file. Should follow the project versioning standards
#   for documents.
# History (Optional)
#   History of the changes of each version. Should follow the project versioning
#   standards for documents.
# Requirements
#   List of requirements covered by the test case.
# Database
#   Database used for INSTANCE.
# Comments (Optional)
#   Any comments for the test case.
# Instance Table
#   The INSTANCE table should be choose and/or created in a way that simplifies
#   the script and allows an easy verification of the number of permutations for
#   the tests. For example, instead of using the "Itineraire" table and
#   iterating for each point or condition, an "Itineraire_ADV" or
#   "Itineraire_condition" should be used.
#
################################################################################

Author = "Author"
Feature = ""
Description = """Sample Description with some "extra" features."""
Modifiedby = ""
Version = "1.0"
History = """"""
Requirements = ""
Database = ""
Comments = """"""
Table = ""

################################################################################
# IMPORT
################################################################################

# Import des fonctions de lecture du modèle
from Interface_Tesia import *

# Import des fonctions d'instanciation
from Interface_Simenv import *

# Import des autres fonctions
from Interface_Database import GetInstanceTest
from Dico_Var import __mode__,__Debug__,__NoDebug__
from Librairie import *
import sys
import inspect

################################################################################
# Scénario de test
################################################################################

def Scenario(instance):
    
    ############################################################################
    # INITIALIZATION
    ############################################################################
    
    # Definition du nom du scénario instancié
    FileName = inspect.getsourcefile(Scenario)
    FileName = FileName[(FileName.rfind("\\")+1):]
    FileName = FileName.replace(".py",".scn")
    SetPath(FileName)

    # Récupération des instances associées au test
    MaBaseDeDonneesEst(instance)
    INSTANCE = GetInstanceTest(FileName)

    # Début de génération du scénario instancié
    Debug("==== Début de génération du %s ===========" % FileName.replace(".scn",""))

    # Création du scénario instancié
    CreationFichier()
    EcrireEntete(Author, Modifiedby, Description, Version)

    # Vérification de la présence d'au moins une instance à tester
    if INSTANCE != [] :
        # On teste chaque ligne de la table des instances
        for PARAMETRE in INSTANCE :
            
            ####################################################################
            # PRECONDITIONS
            ####################################################################
            
            # Récupération des noms des éléments constituant l'instance testée (càd le contenu des colonnes de la table des instances)
            # Par rapport au DVSS, chaque élément mentionné en gras dans les "Objets utilisés" doit être récupéré de cette manière
            # Exemple, récupération du nom de l'itinéraire testé dans la colonne nommée "Itineraire" :
            #
            # Itineraire1 = PARAMETRE['Itineraire']
            #
            ITI = PARAMETRE['Itineraire']
            
            # Récupération des éléments constituant l'instance testée à partir de leur nom
            # A faire pour chaque nom d'élément récupéré ci-dessus
            # Exemple, récupération de l'itinéraire testé à partir de son nom :
            #
            # Itineraire1 = ItineraireNomme(Itineraire1)
            #
            # (cf fichier Librairie.py pour la liste des fonctions de type "xxxNomme(e)")
            ITI = ItineraireNomme(ITI)
            
            # Récupération dans le modèle des éléments ne faisant pas partie de l'instance mais nécessaires au déroulement du test
            # Par rapport au DVSS, chaque élément mentionné non en gras dans les "Objets utilisés" doit être récupéré de cette manière
            # Exemple, récupération d'une aiguille commandée à droite par l'itinéraire testé :
            #
            # Aiguille1 = ListeAigCommandeesParIti(Itineraire1)[0]
            #
            # (cf fichiers Interface_Tesia.py et Librairie.py pour les fonctions (resp. directes et macro) de lecture du modèle)
            SIG = ITI_SIG_origine_Concernant(ITI)[0]
            
            #Affichage de l'instance dans le scénario
            Instance(PARAMETRE)
            
            ####################################################################
            # EXECUTION
            ####################################################################
            
            # TODO
            
    # S'il n'y a aucune instance à tester
    else :
        print "Pas d'instances pour ce scénario"
        Commentaire("Pas d'instances pour ce scénario")   
   
    # Fin de génération du scénario instancié
    FermetureFichier() 
    Debug ("====  %s généré ===========" % FileName.replace(".scn",""))

################################################################################
# Auto-instanciation
################################################################################

def main():
    import CModelCore
    import Dico_Var

    instance = Dico_Var.BasePathInstanceTesia
    modele = Dico_Var.BasePathModelTesia

    core = CModelCore.CModelCore()
    core.OpenModel(modele)
    core.OpenInstance(instance)

    MonGestionnaireEst(core)

    Scenario(instance)

    core.Close()

################################################################################
# Run
################################################################################

if __name__ == '__main__':
    main()