start=1
end=$1

touch tracker2.txt
echo -n "" > tracker2.txt

# Loop to create directories
for ((i = start; i <= end; i++)); do
  mkdir -p "sender$i/"
  cp sender.py "sender$i/"
  cp hello.txt "sender$i/hello.txt"
  echo "hello.txt $i bwurster-XPS-15-7590 $((5000 + $i))" >> tracker2.txt
  cd sender$i/
  python3 sender.py -p "$((5000 + $i))" -g 5000 -r 1 -q 1000 -l 1 &
  cd ..
done
