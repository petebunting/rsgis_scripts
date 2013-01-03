FILES=*.tar.gz
for f in $FILES
do
  echo "Processing $f file..."
  export filename="${f%%.*}"
  echo $filename
  mkdir $filename
  tar -zxf $f -C ./${filename}
  zip ${filename}.zip ./${filename}/*
  rm -Rf ./${filename}
done