### Importation ###
from fpdf import FPDF
import os

localPath = os.path.dirname(os.path.abspath(__file__))

def genDataPDF(datasList: list[str], filePath: str) -> None:
    """
    Procédure qui génère un fichier au format PDF stylisé au couleur du logiciel et qui contient l'ensemble
    des informations présentes dans la liste 'datasList'.

    Args:
        datasList (list[str]): liste contenant des chaînes de caractères, dans ce cas, cela sera les informations de l'utilisateur
        filePath (str): chemin absolu du fichier où va être enregistré le fichier au format PDF
    """
    pdf = FPDF()
    
    pdf.add_page()

    ## Définition de la couleur de fond (début) ##
    pdf.set_fill_color(8, 26, 62)
    pdf.rect(0, 0, 210, 297, 'F') # Création d'un rectangle ayant les mêmes dimension qu'une feuille A4 (210 x 297)
    ## Définition de la couleur de fond (fin) ##

    ## Ajout du logo du logiciel (début) ##
    image_width = 70
    image_height = 70
    x = (210 - image_width) / 2
    pdf.image(localPath + "/../ressources/mainLogo.jpg", x = x, y = 10, w = image_width, h = image_height)
    ## Ajout du logo du logiciel (fin) ##

    ## Ajout du titre (début) ##
    pdf.set_font('Arial', 'B', 15) # Définition de la police
    pdf.set_text_color(255, 255, 255) # Définition de la couleur du texte
    pdf.set_xy(0, 75) # Définition des coordonnées du titre
    pdf.cell(0, 10, 'Vos données stockées par Olympic Tournament', 0, 1, 'C') # Ajout du titre centré
    ## Ajout du titre (fin) ##

    ## Ajout du sous-titre (début) ##
    pdf.set_font('Arial', '', 13)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(5, 90)
    pdf.cell(0, 5, 'Ce que nous stockons :', 0, 1)
    ## Ajout du sous-titre (fin) ##
    
    ## Ajout des informations stockées dans liste 'datasList' (début) ##
    pdf.set_font('Arial', '', 12)
    for i in range(10, (len(datasList) + 1) * 10, 10):
        pdf.set_xy(5, 90+i)
        pdf.cell(0, 5, "- " + datasList[(i - 10) // 10], 0, 1)
    ## Ajout des informations stockées dans liste 'datasList' (fin) ##
        
    pdf.output(filePath, 'F') # Enregistrement du fichier au format PDF