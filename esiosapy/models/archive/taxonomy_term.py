from dataclasses import dataclass


@dataclass
class TaxonomyTerm:
    """
    Represents a taxonomy term associated with an archive.

    This dataclass contains information about a specific taxonomy term, including
    its unique identifier, name, and the identifier of the vocabulary it belongs to.
    """

    id_taxonomy_term: int
    """The unique identifier for the taxonomy term.

    :type: int
    """

    name: str
    """The name of the taxonomy term.

    :type: str
    """

    vocabulary_id: int
    """The identifier of the vocabulary this taxonomy term belongs to.

    :type: int
    """
