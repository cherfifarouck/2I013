echo "Add nouveaux fichiers"

git add *
read -p "Entrer commentaire commit: " msg

read -p "Veux tu sauvegarder en local? o/n " save

git commit -m "$msg" && git push

printf "\n\n"
git status

if [ $save == "o" ]; then
	bash auto_save.sh
	echo "Dossier sauvegarde"
else
	echo "pas de sauvegarde"
fi
