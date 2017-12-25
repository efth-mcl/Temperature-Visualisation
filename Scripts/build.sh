echo install numpy, pandas, matplotlib libraries
sudo pip3 install numpy
sudo pip3 install pandas
sudo pip3 install matplotlib
echo Dawnload Land-Surface Air and Sea-Surface Water Gloabl .CSV
wget --no-check-certificate -O "GLB.Ts+dSST.csv" "https://data.giss.nasa.gov/gistemp/tabledata_v3/GLB.Ts+dSST.csv"

echo remove first line from GLB.Ts+dSST.csv
sed -i '1d' GLB.Ts+dSST.csv

echo run Spider Chart
python3 SpiderChart.py
