# src/ark/entity.py


class Entity:
    """
    Represents a geometric element in the ark Model.
    Currently supports simple cubes with metadata and semantic tags.
    """

    def __init__(
        self,
        id: str,
        width: float,
        depth: float,
        height: float,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        semantic: str = None,
        source_file: str = None,
        source_line: int = None,
    ):
        self.id = id
        self.width = float(width)
        self.depth = float(depth)
        self.height = float(height)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.semantic = semantic
        self.source_file = source_file
        self.source_line = source_line

    def __repr__(self):
        return (
            f"Entity(id={self.id!r}, width={self.width}, depth={self.depth}, height={self.height}, "
            f"x={self.x}, y={self.y}, z={self.z}, semantic={self.semantic!r}, "
            f"file={self.source_file}, line={self.source_line})"
        )
