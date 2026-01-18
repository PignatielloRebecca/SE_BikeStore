from UI.view import View
from database.dao import DAO
from model.model import Model
import flet as ft
import datetime

from model.prodotti import Prodotti
from operator import itemgetter


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def popola_categoria(self):
        dizionario={}
        for c in DAO.read_categorie_biciclette():
            dizionario[c.id] = c
        return dizionario

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        categoria=int(self._view.dd_category.value)
        data_inizio=self._view.dp1.value
        data_fine=self._view.dp2.value


        self._model.build_graph(categoria, data_inizio, data_fine)
        self._view.txt_risultato.controls.append(ft.Text(f"numero di nodi {self._model.G.number_of_nodes()}"))
        self._view.txt_risultato.controls.append(ft.Text(f"numero di archi {self._model.G.number_of_edges()}"))
        self._view.page.update()
        # TODO

    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        lista_prodotti=[]
        for nodo in self._model.G.nodes():
            somma=0
            for arco_out in self._model.G.out_edges(nodo, data=True): # restituisce una tupla (u1, u2, {dizionario})
                somma+=arco_out[2]['weight']
            for arco_in in self._model.G.in_edges(nodo, data=True):
                somma-=arco_in[2]['weight']

            lista_prodotti.append((nodo, somma))
        lista_ordinata=sorted(lista_prodotti, key=itemgetter(1), reverse=True)
        #lista_prodotti.sort(key=lambda x: x[1], reverse=True) # in questo caso non devo creare una nuova lista


        best_prodotti=lista_ordinata[:5]
        for n, s in best_prodotti:
            nome=self._model._map_nodi[n].product_name
            self._view.txt_risultato.controls.append(ft.Text(f"{nome} ----> {s}"))
        self._view.page.update()

        # TODO

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
