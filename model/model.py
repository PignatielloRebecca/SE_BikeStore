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
        self.G.add_nodes_from(self._lista_nodi)  # gli id de nodi

        # costruisco gli archi
        lista_archi=DAO.read_connessioni_archi(categoria_id,data_inizio, data_fine)
        for (n1, n2, peso) in lista_archi:
            self.G.add_edge(n1, n2,weight=peso)  # utilio add edge perche sto usando una lista

        return self.G


    def ricerca_cammino_minimo(self, nodo_iniziale, nodo_finale, lunghezza):

        self._best_cammino=[]
        self._best_somma=-1

        self.__ricorsione(nodo_iniziale, nodo_finale, lunghezza, [nodo_iniziale], 0)
        return self._best_cammino, self._best_somma

    def __ricorsione(self, nodo_corrente, nodo_finale, lunghezza_max, lunghezza_parziale, peso_corrente ):

        if len(lunghezza_parziale) == lunghezza_max:
            if nodo_corrente==nodo_finale:

                if peso_corrente > self._best_somma:
                    self._best_somma=peso_corrente
                    self._best_cammino= lunghezza_parziale.copy()
            return

        for vicino in self.G.neighbors(nodo_corrente):
            if vicino not in lunghezza_parziale:
                peso_arco=self.G[nodo_corrente][vicino]['weight']
                lunghezza_parziale.append(vicino)
                self.__ricorsione(vicino, nodo_finale, lunghezza_max, lunghezza_parziale, peso_corrente + peso_arco)
                lunghezza_parziale.pop()

# in questo caso li passo come nodo corrente quello iniziale , e mi ricordo che devo inserirlo nella ricorsione!!!









# ---> add_edges_weight_from si aspetta una lista mentre cosi posso prendere una diversi valori





