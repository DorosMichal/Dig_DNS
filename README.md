# dig

## opis
    fiber_dig przetwarza argumenty używajac biblioteki argparse, następnie odpala maina gdzie wykonywane jest jedno zapytanie lub (w przypadku opcji trace) rekurenycjnie odpytywane są wszystkie serwery począwszy od podanego (lub roota jeśli nie podano) aż do otrzymania odpowiedzi od serwera autoratywnego dla danej domeny. Gdy nie dostaniemy adresu serwera DNS jest on odnajdywany przy użyciu tej samej funkcji. Wysyłanie wiadomości zaimplementowane jest w klasie Client.

## przyjęte uproszczenia
    - korzystam z pakietu dnspython - wiem, że pozwala on od razu wysyłać i rozwiązywać zapytania dns, ale postanowiłem ograniczyć jego użycie tylko do parsowania i tworzenia wiadmości dns, a samemu napisać ciekawsze części
    - zaimplementowałem tylko wysyłanie pakietów przez UDP, w rozszerzonej wersji dodałbym TCP jako alternatywną opcję oraz "plan B" w przypadku niepowodzenia
    - ograniczyłem się do serwerów z ip w wersji 4
    - w kilku miejscach występuje komentarz #error handling - powinna zostać tam dodana obsługa błędów, której nie dodawałem, aby nie gamtwać kodu i ułatwić wam przeczytanie
    - wypisywane wiadomości są w domyślnej formie, nie dodawałem żadnego formatowania ani dodatkowych informacji takich jak czas otrzymania, rozmiar, serwer z którego to otrzymano

## przykłady użycia
python3 fiber_dig.py --trace -t MX fibertide.com
python3 fiber_dig.py -s 192.5.6.30 fibertide.com

szczegóły można zobaczyć wywołując
python3 fiber_dig.py -h