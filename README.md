# Informatyka geodezyjna 2 projekt 1

Program napisany w języku python oferuje konwersję współrzędnych.
Program działa na elipsoidach grs80 i wgs84. Możliwe są konwersje wielu danych przy odpowiednim wywołaniu. Obsługuje następujące transformacje:

+ XYZ -> BLH (metry -> stopnie, h metry)
+ BLH -> XYZ (stopnie -> metry; z flagą -r: radiany -> metry)
+ XYZ -> NEUp (metry -> metry)
+ BL -> XY2000 (stopnie -> metry; z flagą -r: radiany -> metry)
+ BL -> XY1992 (stopnie -> metry; z flagą -r: radiany -> metry)
+ XYZ -> XY1992 (metry -> metry)
+ XYZ -> XY2000 (metry -> metry)

## Wymagania:

- dowolny system operacyjny posiadający python 3.7 lub nowszy
- math
- numpy
- argparse

## Przykładowe uruchomienie


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
python main.py --model wgs84 -e XYZ -o BLH -f wsp_inp_xyz.txt -n BHL.txt
python main.py --model grs80 -e XYZ -o BLH -x 3664940.5153321843 -y 1409153.5900046194 -z 5009571.91982934
python main.py --model grs80 -e BLH -o XYZ -x 52.097276260222685 -y 21.0315332542456 -z 141.9990357980132
python main.py --model grs80 -e BLH -o XYZ -x 0.909269002 -y 0.367069502 -z 141.9990357980132 -r
python main.py --model wgs84 -e XYZ -o NEUp -x 3664940.5153321843 -y 1409153.5900046194 -z 5009571.91982934 -a 0.909269002 -b 0.367069502 -c 141.9990357980132
python main.py --model grs80 -e BL -o XY1992 -x 52.097276260222685 -y 21.0315332542456
python main.py --model grs80 -e BL -o XY2000 -x 52.097276260222685 -y 21.0315332542456
python main.py --model grs80 -e BL -o X1992 -f BHL.txt -n XY1992.txt
python main.py --model grs80 -e XYZ -o XY2000 -f wsp_inp_xyz.txt -n XYZtoXY2000.txt
python main.py --model grs80 -e XYZ -o XY1992 -x 3664940.5153321843 -y 1409153.5900046194 -z 5009571.91982934
```

## Wady programu

 - Konwertuje dane z marginalnym błędem
 - Słaba obsługa błędów przy złych argumentach
