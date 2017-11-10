
#First, check if the folder "results_of_muscle exist"
if [ -d results_of_muscle ]; then

	#If it exists, delete it's contencts and create a new
	rm -r results_of_muscle
	echo "removed previous dir"
	mkdir results_of_muscle
	echo "created a dir"
else
	#If it does not exist, create the folder
	mkdir results_of_muscle
	echo "created a dir"
fi

#Go to the working directory with all the fasta files
cd yeast_genes


#Loop through all files with the "fasta" extension
for file in *.fasta; do

#Do muscle calculation, taking the first file and outputting into  the results
muscle -in $file -out results_$file

#Moves the result file into the result folder
mv results_$file $HOME/Downloads/results_of_muscle

done

#Goes back to the first directory
cd ..
