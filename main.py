from fastapi import FastAPI, HTTPException
from schemas import GenreURLChoices, BandBase, BandCreate, BandWithID

app = FastAPI()


BANDS =[
    {'id': 1, 'name': 'hello', 'genre': 'Rock', 'albums':[]},
    {'id': 2, 'name': 'Alpha Twix', 'genre': 'Electronic', 'albums':[
        {'title': 'Master of Bass', 'release_date': '1999-07-21'}
    ]},
    {'id': 3, 'name': 'hello 3', 'genre': 'Metal', 'albums': [
        {'title': 'Master of Reality', 'release_date': '1971-07-21'},
        {'title': 'Master of Code', 'release_date': '1983-07-21'}
    ]},
    {'id': 4, 'name': 'hello 4', 'genre': 'Pop', 'albums':[]},
    {'id': 5, 'name': 'Rock Band', 'genre': 'Rock', 'albums':[]},
    {'id': 6, 'name': 'Rock in the sky', 'genre': 'Rock', 'albums':[]},
]

@app.get('/bands')
async def bands(genre: GenreURLChoices | None = None, has_albums: bool = False) -> list[BandWithID]:
   band_list = [BandWithID(**b) for b in BANDS]

   if genre:
       band_list = [
           b for b in band_list if b.genre.value.lower() == genre.value
       ]
   
   if has_albums:
       band_list = [
           b for b in band_list if len(b.albums) > 0
       ]
    
   return band_list

@app.get('/bands/{band_id}', status_code=206)
async def band(band_id: int) -> BandWithID:
    band = next((BandWithID(**b) for b in BANDS if b['id'] == band_id), None)

    if band is None:
        raise HTTPException(status_code=404, detail='Band not found')
    return band

@app.get('/bands/genre/{genre}')
async def bands_for_genre(genre: GenreURLChoices) -> list[dict]:
    return [
        b for b in BANDS if b['genre'].lower() == genre.value
    ]

@app.post('/bands')
def create_band(band_data: BandCreate) -> BandWithID:
    id = BANDS[-1]['id'] + 1
    band = BandWithID(id=id, **band_data.model_dump()).model_dump()
    BANDS.append(band)
    return band
