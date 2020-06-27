rm -rf node1
rm -rf node2
mkdir node1
mkdir node2
cp -r /home/manthan/python/flask/simplified-blockchain/* node1/
cd node1
rm */*.db
rm */*.ini
cd ..
cp -r /home/manthan/python/flask/simplified-blockchain/* node2/
cd node2
rm */*.db
rm */*.ini
