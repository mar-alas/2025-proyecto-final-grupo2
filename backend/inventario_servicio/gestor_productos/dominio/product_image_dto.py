from dataclasses import dataclass

@dataclass
class ProductImageDTO:
    """Representa una imagen asociada a un producto."""
    filename: str
