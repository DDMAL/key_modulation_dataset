#!/bin/bash

for entry in "./tchaikovsky/"/*.krn
do
  echo "Traitement de $entry."



  FILENAME=$entry
  echo "$FILENAME"


  python3 restaff.py $FILENAME 1> temp.krn 2>> error

  FILESIZE=$(stat -c%s "error")
  # echo "Size of error = $FILESIZE bytes."

  if [ $FILESIZE -gt 0 ]
  then
    echo "restaff.py didn't work for $FILENAME."
    exit
  fi

  #treatment for two or four spines

  python3 correct_four_spine_association.py temp.krn 1> final.krn 2>> error
  #python3 correct_two_spine_association.py $FILENAME 1> final.krn 2>> error

  FILESIZE=$(stat -c%s "error")

  if [ $FILESIZE -gt 0 ]
  then
    echo "correct_spine didn't work for $FILENAME."
    exit
  fi

  python3 get_keys.py final.krn 2> error

  FILESIZE=$(stat -c%s "error")
  if [ $FILESIZE -gt 0 ]
  then
    echo "Annotations problems for $FILENAME."
    exit
  fi

  mv final.krn $FILENAME
  rm temp.krn

done
