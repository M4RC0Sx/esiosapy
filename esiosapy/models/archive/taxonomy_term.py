from dataclasses import dataclass


@dataclass
class TaxonomyTerm:
    id_taxonomy_term: int
    name: str
    vocabulary_id: int
