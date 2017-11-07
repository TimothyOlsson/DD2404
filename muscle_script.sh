if [ -d results_of_muscle ]; then
	rm -r results_of_muscle
	echo "removed previous dir"
	mkdir results_of_muscle
	echo "created a dir"
else
	mkdir results_of_muscle
	echo "created a dir"
fi

cd yeast_genes

for file in *.fasta; do

muscle -in $file -out results_$file

mv results_$file $HOME/Downloads/results_of_muscle

done

cd ..
