class Issue:

    def __init__(self, title: str, writers: [], artists: [],
                 cover_artists: [], series: str, issue_no: int, characters: []):
        self.title = title
        self.writers = writers
        self.artists = artists
        self.cover_artists = cover_artists
        self.series = series
        self.issue_no = issue_no
        self.characters = characters
