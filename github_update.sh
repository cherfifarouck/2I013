git add *

read -p "Entrer message: " msg
echo "ca a marched"

git commit -m "$msg" && git push
