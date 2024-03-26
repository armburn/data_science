

# POUR LA MAP FIGURE :
# nombre de graduations des coordonnées : (sur x et y)
Ngrad_x, Ngrad_y = 11, 11
# couleurs de la colormap :
colormap = {
    'statistique': 'RdYlGn_r',
    'corrélation': 'RdYlGn'
    }
# échelle des couleurs de la colormap :
cmap_norm = {
        'statistique': 'log',
        'corrélation': 'linear'
        }
# pour la position centrale : (couleur, épaisseur du trait)
center_color, center_linewidth = '+b', 5
# pour les départements : (couleur du trait, épaisseur du trait, style du trait)
dep_color, dep_linewidth, dep_linestyle = 'black', 0.5, ':'

# POUR LES SMART SLIDERS : (min, max, start, Nstep)
# pour l'échelle :
scale_min, scale_max, scale_start, scale_N = 0.03, 2, 1, 20
# pour le seuil :
thresh_min, thresh_max, thresh_start, thresh_N = 0, 40000, 0, 30
# pour la taille des points :
dot_min, dot_max, dot_start, dot_N = 1, 100, 10, 30


# POUR L'INTERFACE :
# taille de la fenetre : (largeur, hauteur)
width, height = 1200, 1000



# POUR LA CORRELATION :
# creer tous les fichiers des correlations au lancement :
cheat = True

