echo "Add nouveaux fichiers"

git add *
read -p "Entrer commentaire commit: " msg

git commit -m "$msg" && git push
