from graphviz import Digraph
import os

class Node:
    """
    Classe qui gère un arbre binaire.
    """
    def __init__(self, label: str, left: 'Node' = None, right: 'Node' = None):
        self.label = label
        self.left = left
        self.right = right
        self.id = id(self) # Identifiant unique de la classe qui permettra de différencier les '?' dans l'arbre final
     
    def getLabel(self) -> str:
        """
        Méthode qui renvoie l'étiquette de la racine actuelle de l'arbre

        Returns:
            str: texte de l'étiquette
        """
        return(self.label)
     
    def getLeft(self) -> 'Node':
        """
        Méthode qui renvoie le sous-arbre gauche de la racine actuelle de l'arbre

        Returns:
            Node: le sous-arbre gauche
        """
        return(self.left)
     
    def getRight(self) -> 'Node':
        """
        Méthode qui renvoie le sous-arbre droit de la racine actuelle de l'arbre

        Returns:
            Node: le sous-arbre droit
        """
        return(self.right)

def isEmpty(tree: Node) -> bool:
    """
    Fonction qui renvoie un booléen indiquant si l'arbre est vide ou non

    Args:
        tree (Node): objet de type Node que 'lon compare à None

    Returns:
        bool: Prends pour valeur 'True' si l'arbre est vide et 'False' si l'arbre n'est pas vide
    """
    
    return(tree is None)

def addNodes(graph: Digraph, node: Node) -> None:
    """
    Procédure qui ajoute des noeuds à l'arbre

    Args:
        graph (Digraph): l'arbre (à tracer) dont on veut ajouter des noeuds
        node (Node): l'arbre dont la racine est le noeud à ajouter après le précédent (qui sera son parent)
    """
    assert(type(graph) == Digraph), "ERREUR : type incorrect pour l'argument 'graph', requis: Digraph"
    
    if node is not None:
        # Si l'arbre binaire n'est pas vide, on ajoute sa racine actuelle puis on essaye d'ajouter le sous-arbre gauche et le sous-arbre droit
        graph.node(str(node.id), str(node.label), shape='none', fontcolor='#ffffff')  # Ajout du nœud avec sa valeur comme étiquette
        addNodes(graph, node.left)
        addNodes(graph, node.right)

def addEdges(graph: Digraph, node: Node) -> None:
    """
    Procédure qui ajoute les flèches entre les noeuds de l'arbre

    Args:
        graph (Digraph): l'arbre (à tracer) dont ont veut ajouter les flèches
        node (Node): l'arbre dont la racine est le noeud d'où part la flèche
    """
    assert(type(graph) == Digraph), "ERREUR : type incorrect pour l'argument 'graph', requis: Digraph"
    
    if node is not None:
        if node.left is not None:
            ## Ajout d'une flèche entre le noeud actuel et le noeud gauche (début) ##
            graph.edge(str(node.left.id), str(node.id), arrowhead='normal', color='#ffffff')
            addEdges(graph, node.left)
            ## Ajout d'une flèche entre le noeud actuel et le noeud gauche (fin) ##
        if node.right is not None:
            ## Ajout d'une flèche entre le noeud actuel et le noeud droit (début) ##
            graph.edge(str(node.right.id), str(node.id), arrowhead='normal', color='#ffffff')
            addEdges(graph, node.right)
            ## Ajout d'une flèche entre le noeud actuel et le noeud droit (fin) ##

def drawBinaryTree(root: Node, viewTree: bool) -> None:
    """
    Procédure qui crée la représentation d'un arbre à l'aide de la bibliothèque 'Graphviz'

    Args:
        root (Node): arbre binaire contenant l'ensemble de l'arbre à tracer
        viewTree (bool): si vaut 'True', l'arbre sera affiché après la génération sinon, il ne sera pas affiché
    """
    assert(type(viewTree) == bool), "ERREUR : type incorrect pour l'argument 'viewTree', requis: bool"
    
    graph = Digraph('G', filename=os.path.dirname(os.path.abspath(__file__)) + "\\..\\application\\treeView", format="png") # Chemin d'enregistrement de l'image
    
    ## Options de création de l'arbre (début) ##
    graph.attr(rankdir='BT') # Orientation de bas en haut
    graph.attr(dpi='300') # Qualité maximale
    graph.attr('graph', bgcolor='#081a3e') # Définition de la couleur
    graph.attr(fontname='Courier New') # Définition de la police (ne semble pas fonctionner)
    ## Options de création de l'arbre (fin) ##
    
    addNodes(graph, root) # Ajout des nœuds à partir de la racine
    addEdges(graph, root) # Ajout des flèches à partir de la racine
    
    graph.render(cleanup=True, view=viewTree) # Génération de la représentation de l'arbre binaire à partir de l'objet 'graph'
        
def createTree(participants: list[str]) -> Node: 
    """
    Fonction récursive qui renvoie un arbre binaire représentant un arbre de tournoi
    à partir d'une liste de chaînes de caractères contenant le nom des participants.
    Seules les feuilles sont complétées, le reste est rempli avec des '?'.

    Args:
        participants (list[str]): la liste des participants

    Returns:
        Node: l'arbre binaire représentant l'état initial de l'arbre de tournoi
    """
    assert(type(participants) == list), "ERREUR : type incorrect pour l'argument 'participants', requis: list[str]"
    
    if(not(participants)):
        return(None)
    
    if(len(participants) == 1):
        return(Node(participants[0]))

    middle = len(participants) // 2
    gauche = createTree(participants[:middle])
    droit = createTree(participants[middle:])
    
    return(Node("?", gauche, droit))

def defineWinners(arbre: Node, vainqueurs: list[str]) -> Node:
    """
    Fonction récursive qui renvoie un arbre binaire représentant un arbre de tournoi
    à partir d'une liste de chaînes de caractères contenant le nom des vainqueurs du tour précédent.
    Seul le niveau de l'arbre se situant "au dessus" du niveau du tour précédent sera complété.

    Args:
        arbre (Node): l'arbre binaire à modifier pour ajouter les vainqueurs
        vainqueurs (list[str]): la liste des vainqueurs

    Returns:
        Node: l'arbre binaire représentant l'état de la compétition après la victoire des vainqueurs
    """
    assert(type(vainqueurs) == list), "ERREUR : type incorrect pour l'argument 'participants', requis: list[str]"
    
    if(arbre.label != "?"):
        return(arbre.label)
    else:
        gauche = defineWinners(arbre.left, vainqueurs)
        droit = defineWinners(arbre.right, vainqueurs)
        if(gauche in vainqueurs): arbre.label = gauche
        elif(droit in vainqueurs): arbre.label = droit
        return(arbre)