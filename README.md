- udokumentowany, czyli opisany na githubie w pliku README.md, który ma zawierać następujące informacje:
    - do czego służy program i jaką funkcjonalność oferuje (transformacja XYZ -> BLH, transformacja BLH -> XYZ, jakie elipsidy są obsługiwane, ...)
    - jakie wymagania trzeba spełnić, by program działał na danym komputerze (np. trzeba mieć pythona w wesji takiej-a-takiej,
      zainstalowaną bibliotekę taką-a-taką, ...)
    - dla jakiego systemu operacyjnego został napisany program
    - jak go używać wraz z kilkoma przykładami wywołań obrazującymi jak z niego korzystać (w tym opis struktury danych wejściowych i wyjściowych)
      oraz rezultatami tych wywołań (przykładowe wywołania powinny za input brać plik z przykładowymi danymi)
    - znane błędy i nietypowe zachowania programu, które nie zostały jeszcze naprawione
# Informatyka geodezyjna 2 projekt 1

Program napisany w języku python oferuje konwersję współrzędnych.
Program działa na elipsoidach grs80 i wgs84. Możliwe są konwersje wielu danych przy odpowiednim wywołaniu. Obsługuje następujące transformacje:

+ XYZ -> BLH
+ BLH -> XYZ
+ XYZ -> NEUp
+ BL -> XY2000
+ BL -> XY1992
+ XYZ -> XY1992
+ XYZ -> XY2000


## Wymagania:

- dowolny system operacyjny posiadający python 3.7 lub nowszy
- math
- numpy
- argparse

## Przykładowe uruchomienie
Wywołania z poziomu pliku main.py


Aby uzyskać instrukcje należy uruchomienie z flagą -h
```python main.py -h```
Kolejne współrzędne powinny być podane za flagami -x, -y, -z. Program obsługuje pliki txt, gdzie kolejna linia współrzędnych oddzielona jest przecinkiem. Przykład
```
5773723.182,7502160.783
5773723.175,7502160.77
5773723.171,7502160.757
5773723.167,7502160.744
```
Wywołania zwracją pliki w takim samym formacie. Przykładowe wyołania:
```
python main.py --model grs80 -e XYZ -o XY2000 -f wsp_inp_xyz.txt -n XYZtoXY2000.txt
python main.py --model grs80 -e BL -o XY2000 -f BHL.txt -n XY1992.txt
python main.py --model wgs84 -e XYZ -o BLH -f wsp_inp_xyz.txt -n BHL.txt
python main.py --model grs80 -e BL -o XY2000 -x 52.097276260222685 -y 21.0315332542456
python main.py --model grs80 -e BLH -o XYZ -x 52.097276260222685 -y 21.0315332542456 -z 141.9990357980132
```
## Wady programu

 - Konwertuje dane z marginalnym błędem
 - Słaba obsługa błędów przy złych argumentach