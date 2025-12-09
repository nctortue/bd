erDiagram
    ARTISTS       ||--o{ TRACKS          : creates
    ALBUMS        ||--o{ TRACKS          : contains
    TRACKS        ||--|| TRACK_FEATURES  : has
    PLAYLISTS     ||--o{ TRACK_PLAYLISTS : includes
    TRACKS        ||--o{ TRACK_PLAYLISTS : appears_in
    TRACKS        ||--o{ SIMILAR_TRACKS  : source
    SIMILAR_TRACKS o{--|| TRACKS         : target
    MODELS        ||--o{ SIMILAR_TRACKS  : produces

    ARTISTS {
      int    artist_id PK
      string name
    }

    ALBUMS {
      string album_id PK
      string name
      date   release_date
    }

    TRACKS {
      string track_id PK
      string name
      int    artist_id   "FK -> ARTISTS.artist_id"
      string album_id    "FK -> ALBUMS.album_id"
      int    popularity
      int    duration_ms
    }

    TRACK_FEATURES {
      string track_id PK "FK -> TRACKS.track_id"
      float  danceability
      float  energy
      float  loudness
      float  speechiness
      float  acousticness
      float  instrumentalness
      float  liveness
      float  valence
      float  tempo
    }

    PLAYLISTS {
      string playlist_id PK
      string name
      string genre
      string subgenre
    }

    TRACK_PLAYLISTS {
      string track_id    PK "FK -> TRACKS.track_id"
      string playlist_id PK "FK -> PLAYLISTS.playlist_id"
    }

    MODELS {
      int      model_id PK
      string   name
      string   description
      string   params      "JSON as text"
      datetime created_at
    }

    SIMILAR_TRACKS {
      string   track_id         PK "FK -> TRACKS.track_id"
      string   similar_track_id PK "FK -> TRACKS.track_id"
      int      model_id         "FK -> MODELS.model_id"
      float    score
      datetime updated_at
    }
