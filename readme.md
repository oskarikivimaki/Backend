# Projekti

Tämä projekti käyttää Pythonia ja joitakin sen kirjastoja. Seuraavat ohjeet auttavat sinua asentamaan tarvittavat riippuvuudet.

## Virtuaaliympäristön luominen

Ennen kuin aloitat, voit luoda uuden virtuaaliympäristön seuraavalla komennolla ollessasi halutussa kansiossa:

```python3 -m venv venv```

Tarvittavat ohjelmistot

Python: Tämä projekti vaatii Pythonin version 3.10 tai uudemman.

pip: Pythonin paketinhallintaohjelma, joka tulee yleensä Pythonin mukana.

## Riippuvuudet
Tämä projekti käyttää seuraavia Python-kirjastoja:


FastAPI
Asenna se komennolla: ```pip install fastapi```

Uvicorn
Asenna se komennolla: ```pip install uvicorn```

Pydantic
Asenna se komennolla: ```pip install pydantic```

Matplotlib
Asenna se komennolla: ```pip install matplotlib```

# Sovelluksen suoritus
Jos loit virtuaaliympäristön sen voi aktivoida komennolla

``` .\.venv\Scripts\Activate.ps1 ```

Tämän jälkeen suorita uvicorn komennolla

```uvicorn main:app```

Jos teet koodiin muutoksia on hyvä suorittaa komento mielummin näin

```uvicorn main:app --reload```

Uvicorn aukaisee terminaaliin linkin josta pääset katsomaan itse FastAPI sovellusta.

Docs sivulle pääset kun listää URL linkin perään

```/docs```