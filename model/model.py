from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._map_nodi={}
        self._lista_nodi=[]
        self.G=nx.DiGraph()

    def get_date_range(self):
        return DAO.get_date_range()

    def load_map_nodi(self, categoria_id):

        for o in DAO.get_prodotti(categoria_id):
            self._map_nodi[o.id]=o
        return  self._map_nodi

    def build_graph(self, categoria_id, data_inizio,data_fine):

        # costruisco i nodi
        self._lista_nodi=[c for c in self.load_map_nodi(categoria_id).keys()]
        self.G.add_nodes_from(self._lista_nodi)

        # costruisco gli archi
        lista_archi=DAO.read_connessioni_archi(categoria_id,data_inizio, data_fine)
        for (n1, n2, peso) in lista_archi:
            self.G.add_edge(n1, n2,weight=peso)

        return self.G


# ---> add_edges_weight_from si aspetta una lista mentre cosi posso prendere una diversi valori





