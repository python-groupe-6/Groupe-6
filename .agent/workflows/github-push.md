---
description: Comment pousser vos changements vers GitHub
---

Voici les étapes à suivre pour sauvegarder vote travail sur GitHub :

1.  **Vérifier les modifications**
    Exécutez cette commande pour voir quels fichiers ont été modifiés :
    ```powershell
    git status
    ```

2.  **Ajouter les fichiers**
    Pour ajouter tous les changements effectués :
    ```powershell
    git add .
    ```

3.  **Créer un commit**
    Enregistrez vos modifications avec un message descriptif :
    ```powershell
    git commit -m "Description de vos changements"
    ```

4.  **Pousser vers GitHub**
    Envoyez le tout vers le serveur :
    ```powershell
    git push origin main
    ```
    *(Note : Si votre branche s'appelle `master`, utilisez `git push origin master`)*.
