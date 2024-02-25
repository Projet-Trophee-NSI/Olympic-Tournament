from graphviz import Digraph
import os

class Noeud:
    def __init__(self, e, g = None, d = None):
        self.label = e
        self.left = g
        self.right = d
        self.id = id(self)
     
    def getLabel(self):
        return self.label
     
    def getLeft(self):
        return self.left
     
    def getRight(self):
        return self.right


def isEmpty(tree): return tree is None

def addEdges(graph, node: Noeud):
    if node is not None:
        if node.left is not None:
            graph.edge(str(node.left.id), str(node.id), arrowhead='normal', color='#ffffff')
            addEdges(graph, node.left)
        if node.right is not None:
            graph.edge(str(node.right.id), str(node.id), arrowhead='normal', color='#ffffff')
            addEdges(graph, node.right)

def drawBinaryTree(root: Noeud, viewTree: bool):
    graph = Digraph('G', filename=os.path.dirname(os.path.abspath(__file__)) + "\\treePreview", format="png")
    #graph.attr(rankdir='LR')
    graph.attr(rankdir='BT')
    graph.attr(dpi='300')
    graph.attr('graph', bgcolor='#021438')
    graph.attr(fontname='Courier New')
    addNodes(graph, root)  # Ajoute tous les nœuds à partir de la racine
    addEdges(graph, root)
    graph.render(cleanup=True, view=viewTree)
    
def addNodes(graph, node: Noeud):
    if node is not None:
        graph.node(str(node.id), str(node.label), shape='none', fontcolor='#ffffff')  # Ajoute le nœud avec la valeur comme étiquette
        addNodes(graph, node.left)
        addNodes(graph, node.right)
        
def createTree(participants: list):
    if not participants:
        return None
    
    if len(participants) == 1:
        return Noeud(participants[0])

    middle = len(participants) // 2
    gauche = createTree(participants[:middle])
    droit = createTree(participants[middle:])
    return Noeud("?", gauche, droit)

def definedWinners(arbre: Noeud, vainqueurs: list):
    if(arbre.etiquette != "?"):
        return(arbre.etiquette)
    else:
        gauche = definedWinners(arbre.gauche, vainqueurs)
        droit = definedWinners(arbre.droit, vainqueurs)
        if(gauche in vainqueurs): arbre.etiquette = gauche
        elif(droit in vainqueurs): arbre.etiquette = droit