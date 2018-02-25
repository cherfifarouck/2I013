echo "Add nouveaux fichiers"

git add *
read -p "Entrer commentaire commit: " msg

read -p "Veux tu sauvegarder? o/n" save
if [$save == "o"]; then
	echo "tu veux sauvegarder"
fi

git commit -m "$msg" && git push

printf "\n\n"
git status
