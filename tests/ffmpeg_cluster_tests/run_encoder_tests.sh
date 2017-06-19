#!/bin/bash
#PBS -l select=1:ncpus=272 -lpace=excl

for i in {65..120..5}
do
	for j in {1..5..1}
	do 
		NEW=./copies_of_encoders/encoder_test_${i}_${j}.sh
		cp encoder_test.sh $NEW
		sed -i "s/TIME=/TIME=$i # /g" $NEW

		#submit to cluster	
		{ qsub $NEW ; } 1>/dev/null

		#run locally
		#./$NEW

		#rm $NEW
	done
done
