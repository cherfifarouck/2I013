date=$(date +'%d-%m-%Y')

num_fold=$(ls -l ../saves/ | grep -c ^d)
if [ $num_fold -ge 10 ]; then
	echo "clean save folder xaxa"
fi

mkdir ../saves/$date; cp -R ./* ../saves/$date/;


