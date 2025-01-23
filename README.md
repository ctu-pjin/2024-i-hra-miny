# Hra: Miny

### Seznam členů:
* Adam Králič
* Barbora Matějková
* Adéla Pohanková

Požadavky: python 3.10+, modules: pygame 2.6+, numpy 2.1+, json, random, sys, os
Pouštět přes pygame_part.py, případně celá hra byla vyexportována do miny.exe

Surfaces a veškeré grafické výstupy hry byly vytvořeny touto skupinou v pixel art programu Aseprite (https://www.aseprite.org/). Použitý font je Karma Suture a Karma Future, oba z open licence stažené ze stránky https://www.1001fonts.com/pixel-fonts.html. 

V našem projektu půjde o vytvoření hry, která originálně vznikla pod názvem Minesweeper.
Hra momentálně obsahuje veškeré prvky a možnosti originální hry s přidanými funkcemi (save system, reshuffle).

### Po první prezentaci:

Máme v plánu: Vytvořit sandbox mode, kde si bude moc hráč zvolit velikost pole a počet min v poli
              Přidat možnost uložit si skóre do lokálního (popřípadě globálního) žebříčku 
              Přidat možnost nápovědy ve hře

Hra nabízí tři předpřipravené úrovně:
* Easy - pole 12x10, 18 min
* Medium - pole 16x13, 37 min
* Hard - pole 29, 20, 100 min
  
a možnost vytvoření svého "custom" pole. U volitelného pole je možnost změnit velikost buněk. Aby bylo pole vygenerovatelné, je ošetřeno podmínkou, že počet min musí být o 15 menší než počet polí.

Vložit řešený čas do lokální databáze i zobrazit si nejlepších 12 řešitelů pole daného rozměru, po vložení času do databáze se opět zobrazí nejlepší řešitelé.
V rámci hry je dostupný ukládací systém se třemi save sloty, které lze přeuložit i smazat, hru lze opětovně načíst z hlavního menu. Uloženy budou veškeré parametry (tj. i počet použití funkcí reshuffle a hint).

Při řešení je možné použít dvě nové funkce - reshuffle, který mění polohu nenajitých min, a nápověda, která označí jednu nenalezenou minu modrou vlaječkou, již není možné odebrat. Obě mají omezený počet užití a jiné strategické výhody.

V hlavním menu je proklik na "help", kde je popsán průběh hry a jednotlivé funkce.


### Soubory:
* složky fonts, mines, surfaces obsahují grafické komponenty hry
* složka saves obsahuje uložené hry
* pole_funkce.py, score_funkce.py jsou soubory s dalšími funkcemi volanými z pygame_part.py, což je hlavní soubor hry
* scores.json obsahuje databázi uložených výsledků
* miny.exe obsahuje vyexportovanou hru do executable souboru, musí být ve stejné složce s grafickými soubory, saves a scores.json, aby fungovala!
* projekt_miny_prezentace.pdf je předpřipravená prezentace ke hře
