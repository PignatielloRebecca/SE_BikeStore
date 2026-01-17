from dataclasses import dataclass
@dataclass
class Prodotti:
    id: int
    product_name:str


    def __str__(self):
        return f"{self.id} {self.product_name}"

    def __hash__(self):
        return hash(self.id)