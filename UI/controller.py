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
            dizionario[c.id] = c  # identifico la categoria con l'oggetto e posso prendere poi l'id
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
        # grafo orientato, quindi devo prendere archi uscenti e archi entranti
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

        # adesso devo implementare la dropdown con i prodotti piu venduti
        for (c,v) in self._model._map_nodi.items():
            self._view.dd_prodotto_iniziale.options.append(ft.dropdown.Option(key=str(c), text=str(v.product_name)))

        self._view.page.update()

        for (c, v) in self._model._map_nodi.items():
            self._view.dd_prodotto_finale.options.append(ft.dropdown.Option(key=str(c), text=str(v.product_name)))

        self._view.page.update()
        # TODO

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        self._view.txt_risultato.controls.clear()  # pulisco i risultati precendeti della dropdown

        try:
            prodotto_iniziale = int(self._view.dd_prodotto_iniziale.value)
            prodotto_finale = int(self._view.dd_prodotto_finale.value)
            lunghezza = int(self._view.txt_lunghezza_cammino.value)
        except (ValueError, TypeError):
            self._view.txt_risultato.controls.append(ft.Text("Inserisci valori validi"))
            self._view.page.update()
            return

        cammino, peso=self._model.ricerca_cammino_minimo(prodotto_iniziale, prodotto_finale, lunghezza)

        if not cammino:
            self._view.txt_risultato.controls.append(ft.Text("Nessun cammino trovato"))
        else:
            for id in cammino:
                nome = self._model._map_nodi[id].product_name
                self._view.txt_risultato.controls.append(ft.Text(f"{nome}"))
            self._view.txt_risultato.controls.append(ft.Text(f"Somma dei pesi: {peso}"))

            # aggiornamento finale della pagina
        self._view.page.update()

        # TODO
