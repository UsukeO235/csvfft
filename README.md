# csvfft
Calculate FFT result of csv formatted data, and export the result as csv.

# Description
FFT is a key point of frequency anlysis, but it is bothersome to execute correctly. csvfft ables you to easily get FFT result of csv formatted data.

# Sample Usage
```bash
git clone https://github.com/UsukeO235/csvfft.git
cd csvfft/sample
python generate.py
python ../csvfft.py --input input.csv --period 0.001 --delimiter tab --name --figure --column 2
```