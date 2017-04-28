# Auteur:   Jeremy Junac (Groupe 2)
# Conding:  UTF-8

1. Installation
    L'intégralité du code du serveur web se trouve dans le fichier server.py.
    Cependant, il est important que le fichier de configuration server.properties se trouve au 
    même niveau que le serveur dans l'arborescence de fichier, avec tous les paramêtres définis.

2. Configuration
    Si l'arborescence de fichier est laissé par défaut, le serveur est utilisable immédiatement.
    Cependant, le serveur possède quelques paramêtres configurables, regroupés dans le fichiers
    "server.properties". Les différents paramêtres sont décrits ci-dessous:
        * HTTP_ROOT: Défini le HTTP_ROOT du serveur (la racine des fichiers accessibles grâce
            au serveur web)
        * BUFFER_SIZE: La taille du buffer en lecture du socket utilisé par le serveur
        * ADRESS: L'adresse utilisée par le serveur web (laisser localhost)
        * PORT: Le port utilisé par le serveur web. Si le port est inférieur à 1024, le serveur
            doit être lancé en administrateur
        * CGI-BIN_DIRECTORY: Le nom du dossier où seront placé les cgi-bin. En dehors de ce dossier,
            aucun cgi-bin ne sera exécuté par le serveur
            /!\ Ce dossier doit être à l'intérieur du dossier HTTP_ROOT /!\
        * GET_ONLY_DIRECTORY: Le nom du dossier qui contient les cgi-bin qui peuvent être exécutés
            uniquement via la méthode GET. 
            /!\ Ce dossier doit être à l'intérieur du dossier CGI-BIN_DIRECTORY /!\
        * POST_ONLY_DIRECTORY: Le nom du dossier qui contient les cgi-bin qui peuvent être exécutés
            uniquement via la méthode POST. 
            /!\ Ce dossier doit être à l'intérieur du dossier CGI-BIN_DIRECTORY /!\
    /!\ Le changement de certains paramêtres, en particulier HTTP_ROOT, CGI-BIN_DIRECTORY,
        GET_ONLY_DIRECTORY et POST_ONLY_DIRECTORY pourrait rendre les formulaires de tests fournis
        inutilisables.

3. Lancement
    Le lancement du serveur web peut être fait depuis un shell de 2 façons:
        $ ./server.py ou $ python server.py
    Après avoir lancé le serveur web, vous pouvez le tester en allant sur l'index par exemple,
    à l'une des adresses suivante sur votre navigateur (avec les paramêtres par défaut du 
    serveur):
        http://localhost:8080/ ou http://localhost:8080/index.html
    Cet index affiche des liens qui mènent vers les différents formulaires de tests.
    Voici une liste des différents formulaires:
        * Formulaire pour le cgi-bin de type GET: 
            http://localhost:8080/test-get.html
        * Formulaire pour le cgi-bin de type POST: 
            http://localhost:8080/test-post.html
        * Formulaire pour le cgi-bin de type POST/GET en utilisant un GET: 
            http://localhost:8080/test-post-get-get.html
        * Formulaire pour le cgi-bin de type POST/GET en utilisant un POST: 
            http://localhost:8080/test-post-get-post.html
    Les réponses attendues sont à chaque fois décrites sur les pages web contenants les
    formulaires.

4. Explications
    Les explications suivantes décrivent les étapes qui se déroulent par ordre chronologique
    après la réception du début de la requête, voire de la requête entière.

    * Tant que la première ligne n'est pas complète, on lit l'entrée du socket
    * On lit ensuite la requête ligne par ligne jusqu'à trouver deux "\n" d'affiler. Cela marque
        la sépratation entre l'en-tête et le corps de la requête. 
        Toutes les lignes lues à ce moment là sont les en-têtes de la requête. Ils sont stockés 
        pour un usage futur.
    * Une fois la chaine "\n\n" lue, on regarde la méthode utilisée pour la requête.
        Trois cas sont possibles:
            * GET: On extrait le chemin vers le fichier demandé. Là encore, trois cas sont
                possibles:
                    a) Le chemin est "/": Le chemin est changé en "index.html", puis on va au
                        cas c.
                    b) Le chemin pointe vers un fichier du dossier contenant les cgi-bin.
                        On vérifie tout d'abord que le cgi-bin supporte la méthode GET. Si le
                        cgi-bin ne supporte pas la méthode GET, on envoie une erreur 405,
                        spécifiant que la méthode GET n'est pas autorisé sur ce cgi-bin. Puis
                        on met les paramêtres du GET dans la variable d'environnement 
                        QUERY_STRING. Enfin, on exécute le cgi-bin spécifié et envoie sa sortie
                        au client.
                    c) Le fichier n'est pas un cgi-bin. On envoie alors son contenu au client.
                Dans tous les cas, si le fichier n'existe pas, on envoie une erreur 404,
                spécifiant que le fichier n'a pas été trouvé.
            * POST: On lit l'entrée du socket tant que la "Content-length" spécifiée dans 
                l'en-tête ne correspond pas à la taille du corps de la requête.
                Puis, on extrait le chemin vers le fichier demandé. Si le chemin pointe vers un 
                fichier du dossier contenant les cgi-bin, on vérifie que celui-ci supporte la
                méthode POST. Dans le cas contraire, comme pour la méthode GET, on envoie une
                erreur 405. Ensuite, on lance le cgi-bin et on écrit sur son entrée standard
                à l'aide d'un tube. Enfin, on récupère sa sortie, puis on l'envoie au client.
                Là encore, si le fichier n'existe pas, on envoie une erreur 404, spécifiant que
                le fichier n'a pas été trouvé.
            * Ni GET ni POST: On envoie une erreur 400, spécifiant que le serveur n'a pas compris
                la requête.
    
    Pendant la lecture, si une erreur quelconque arrive, on envoie une erreur 400. Une manière
    plus propre de faire serait de différencier les erreurs de lecture (400 Bad Request) et les
    erreurs du serveur (500 Internal Error)