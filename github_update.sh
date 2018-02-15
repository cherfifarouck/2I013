git add *

while true; do
	read -p "Entrer message: " msg
	case $msg in
		[]* ) echo "Entrer message"; continue;;
		* ) break;;
	esac
done

echo "ca a marched"

git commit -m "$msg" && git push && echo cherfifarouck
