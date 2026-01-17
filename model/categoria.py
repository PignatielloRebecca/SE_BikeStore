from dataclasses import dataclass
@dataclass
class Category:
    id: int
    category_name:str


    def __str__(self):
        return f"{self.id} {self.category_name}"

    def __hash__(self):
        return hash(self.id)
