import copy

from database.DAO import DAO
import networkx as nx

from model.sighting import Sighting


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._bestSol = []
        self._maxScore = 0

    def getYears(self):
        return DAO.getYears()

    def getStates(self):
        return DAO.getStates()

    def buildGraph(self, year, state):
        self._graph.clear()
        self._idMap = {}

        nodes = DAO.getNodes(year, state)
        for node in nodes:
            self._idMap[node.id] = node
        self._graph.add_nodes_from(nodes)

        for u in self._graph.nodes:
            for v in self._graph.nodes:
                if u.id < v.id:
                    if u.distance_HV(v) < 100 and u.shape == v.shape:
                        self._graph.add_edge(u, v)

        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getInfoConnessa(self):
        componenti_connesse = list(nx.connected_components(self._graph))
        return len(componenti_connesse), max(componenti_connesse, key=len)

    def getPercorso(self):
        self._bestSol = []
        self._maxScore = 0

        for node in self._graph.nodes:
            self._ricorsione([node], node)

        return self._bestSol, self._maxScore

    def _ricorsione(self, parziale, source):
        if (score := self._calcolaScore(parziale)) > self._maxScore:
            self._bestSol = copy.deepcopy(parziale)
            self._maxScore = score
        for n in self._graph.neighbors(source):
            if n not in parziale:
                if self._nodoAmmissibile(n, parziale):
                    parziale.append(n)
                    self._ricorsione(parziale, n)
                    parziale.pop()

    def _nodoAmmissibile(self, nodo: Sighting, parziale):
        if nodo.duration < parziale[-1].duration:
            return False
        if len(parziale) < 3:
            return True
        if parziale[-3].datetime.month == parziale[-2].datetime.month == parziale[-1].datetime.month:
            return nodo.datetime.month != parziale[-1].datetime.month
        return True

    def _calcolaScore(self, soluzione):
        punteggio = 0
        for i in range(len(soluzione)):
            if i == 0:
                punteggio += 100
            else:
                punteggio += 100
                if soluzione[i].datetime.month == soluzione[i-1].datetime.month:
                    punteggio += 200
        return punteggio

