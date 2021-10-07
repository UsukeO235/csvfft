# csvfft

# Overview
Calculate FFT result of csv formatted data, and export the result as csv.

# Description
FFT is a key point of frequency anlysis, but it is bothersome to execute correctly. csvfft ables you to easily get FFT result of csv formatted data.

# Sample Usage
## Basic FFT
```bash
git clone https://github.com/UsukeO235/csvfft.git
cd csvfft/sample/sine_wave
python generate.py
python ../../csvfft.py --input input.csv --period 0.001 --delimiter tab --name --figure --column 2
```
![result](https://user-images.githubusercontent.com/63541132/135855217-2945add7-6a81-421d-9cc4-55214e1bffe1.png)

## Short Time Fourier Transform (STFT)
### Basic STFT
```bash
git clone https://github.com/UsukeO235/csvfft.git
cd csvfft/sample/stft
python ../../csvfft.py --input input.csv --period 0.001 --delimiter tab --name --figure --column 2 --overlap 180 --frame 200 --stft
```
![result](https://user-images.githubusercontent.com/63541132/136400304-bb733539-f314-471a-9a29-418ac13a8966.png)

### STFT with frequency range setting
```bash
git clone https://github.com/UsukeO235/csvfft.git
cd csvfft/sample/stft
python ../../csvfft.py --input input.csv --period 0.001 --delimiter tab --name --figure --column 2 --overlap 180 --frame 200 --stft --range 80.0 250.0
```
![result_range](https://user-images.githubusercontent.com/63541132/136400348-9d855f6f-5dc6-4f4d-9bf4-dee4e6a901b0.png)
