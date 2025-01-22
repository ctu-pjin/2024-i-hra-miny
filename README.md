# Hra: Miny

Požadavky: python 3.10+, modules: pygame, json, numpy, random, sys, os
Pouštět přes pygame_part.py

Surfaces a veškeré grafické výstupy hry byly vytvořeny touto skupinou v pixel art prograpu Aseprite. Použitý font je Karma Suture a Karma Future, oba z open licence. 

V našem projektu půjde o vytvoření hry, která originálně vznikla pod názvem Minesweeper.
Hra momentálně obsahuje veškeré prvky a možnosti originální hry s přidanými funkcemi (save system, reshuffle).

Máme v plánu: Vytvořit sandbox mode, kde si bude moc hráč zvolit velikost pole a počet min v poli
              Přidat možnost uložit si skóre do lokálního (popřípadě globálního) žebříčku 
              Přidat možnost nápovědy ve hře

Seznam členů:
* Adam Králič
* Barbora Matějková
* Adéla Pohanková

Hra nabízí tři předpřipravené úrovně
    Easy - pole 12x10, 18 min
    Medium - pole 16x13, 37 min
    Hard - pole 29, 20, 100 min
a možnost vytvoření svého "custom" pole. U volitelného pole je možnost změnit velikost buněk. Aby bylo pole vygenerovatelné, je ošetřeno podmínkou, že počet min musí být o 15 menší než počet polí.
Vložit řešený čas do lokální databáze i zobrazit si nejlepších 12 řešitelů pole daného rozměru, po vložení času do databáze se opět zobrazí nejlepší řešitelé.
V rámci hry je dostupný ukládací systém se třemi save sloty, které lze přeuložit i smazat, hru lze opětovně načíst z hlavního menu. Uloženy budou veškeré parametry (tj. i počet použití funkcí reshuffle a hint).
Při řešení je možné použít dvě nové funkce - reshuffle, který mění polohu nenajitých min, a nápověda, která označí jednu nenalezenou minu modrou vlaječkou, již není možné odebrat. Obě mají omezený počet užití a jiné strategické výhody.
V hlavním menu je proklik na "help", kde je popsán průběh hry a jednotlivé funkce.

