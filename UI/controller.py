import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDs(self):
        years = self._model.getYears()
        for year in years:
            self._view.ddyear.options.append(ft.dropdown.Option(year))
        states = self._model.getStates()
        for state in states:
            self._view.ddstate.options.append(ft.dropdown.Option(state))
        self._view.update_page()


    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        year = self._view.ddyear.value
        if not year:
            self._view.txt_result1.controls.append(ft.Text("Selezionare l'anno", color="red"))
            self._view.update_page()
            return
        state = self._view.ddstate.value
        if not state:
            self._view.txt_result1.controls.append(ft.Text("Selezionare lo stato", color="red"))
            self._view.update_page()
            return
        nodes, edges = self._model.buildGraph(year, state)
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {nodes}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {edges}"))
        NConnesse, componenteMax = self._model.getInfoConnessa()
        self._view.txt_result1.controls.append(ft.Text(f"Il grafo ha: {NConnesse} componenti connesse"))
        self._view.txt_result1.controls.append(ft.Text(f"La componente connessa più grande è costituita da {len(componenteMax)} nodi"))
        for nodo in componenteMax:
            self._view.txt_result1.controls.append(ft.Text(nodo))
        self._view.btn_path.disabled = False
        self._view.update_page()

    def handle_path(self, e):
        self._view.txt_result2.controls.clear()
        percorso, score = self._model.getPercorso()
        self._view.txt_result2.controls.append(ft.Text(f"Trovato percorso di {len(percorso)} nodi"))
        for nodo in percorso:
            self._view.txt_result2.controls.append(ft.Text(nodo))
        self._view.txt_result2.controls.append(ft.Text(f"Punteggio percorso: {score}"))
        self._view.update_page()

