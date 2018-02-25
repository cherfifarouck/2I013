echo "Add nouveaux fichiers"

git add *
read -p "Entrer commentaire commit: " msg

read -p "Veux tu sauvegarder en local? o/n" save

git commit -m "$msg" && git push

printf "\n\n"
git status

if [$save == "o"]; then
	echo "tu veux sauvegarder"
else
	echo "tu veux pas"
fi
