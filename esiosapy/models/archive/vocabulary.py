from dataclasses import dataclass


@dataclass
class Vocabulary:
    """
    Represents a vocabulary that groups related taxonomy terms.

    This dataclass contains information about a specific vocabulary, including its
    unique identifier and name.
    """

    id_vocabulary: int
    """The unique identifier for the vocabulary.

    :type: int
    """

    name: str
    """The name of the vocabulary.

    :type: str
    """
