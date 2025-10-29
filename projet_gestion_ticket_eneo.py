from tkinter import *
from tkinter import ttk
import mysql.connector as mysc
from tkinter import messagebox

# Connexion à la base de données
def connect_to_db():
    return mysc.connect(host="localhost", user="root", password="ROOT", database="Helpdesk")

# Compter les clients pour générer le matricule
def count_client():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT MAX(CAST(REPLACE(matricule, 'Helpdesk_', '') AS UNSIGNED)) FROM Client")
        dernier_num = cur.fetchone()[0]
        if dernier_num is None:
            return "Helpdesk_1"
        return f"Helpdesk_{dernier_num + 1}"
    except mysc.Error as e:
        print(f"Erreur: {e}")
        return "Helpdesk_1"
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

# Fonction pour obtenir la date au format MySQL
def get_date_mysql():
    jour = jour_var.get().zfill(2)
    mois = mois_var.get().zfill(2)
    annee = annee_var.get()
    return f"{annee}-{mois}-{jour}"

# Fonction pour définir la date dans les listes déroulantes
def set_date(date_str):
    try:
        if date_str and date_str != '':
            parts = date_str.split('-')
            annee_var.set(parts[0])
            mois_var.set(str(int(parts[1])))
            jour_var.set(str(int(parts[2])))
    except:
        pass

# Fonctions CRUD
def ajouter():
    if not modifier_mode[0]:
        matricule = matricule_var.get()
        nom = nom_entry.get()
        prenom = prenom_entry.get()
        Unite = Unite_entry.get()
        Materiel = Materiel_entry.get()
        numero_serie = numero_serie_entry.get()
        telephone = telephone_entry.get()
        Modele = Modele_entry.get()
        Nom_technicien = Nom_technicien_entry.get()
        date = get_date_mysql()
        diagnostics = diagnostics_entry.get()
        solutions_propose = solutions_propose_entry.get()
        statut = statut_var.get()

        # Validation des champs obligatoires
        if not all([nom, prenom, telephone, Unite]):
            messagebox.showwarning("Attention", "Veuillez remplir les champs obligatoires!")
            return

        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("SELECT matricule FROM Client WHERE matricule=%s", (matricule,))
            if cur.fetchone():
                messagebox.showwarning("Attention", "Ce matricule existe déjà !")
                return
            cur.execute("INSERT INTO Client (matricule,nom,prenom,telephone,Unite,Materiel,numero_serie,Modele,Nom_technicien,date,diagnostics,solutions_propose,statut) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (matricule,nom,prenom,telephone,Unite,Materiel,numero_serie,Modele,Nom_technicien,date,diagnostics,solutions_propose,statut))
            conn.commit()
            messagebox.showinfo("Succès", "Ticket enregistré avec succès !")
            vider_champs()
            actualiser_liste_client()
        except mysc.Error as e:
            messagebox.showerror("Erreur", str(e))
        finally:
            cur.close()
            conn.close()
    else:
        matricule = matricule_var.get()
        date = get_date_mysql()
        statut = statut_var.get()
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("UPDATE Client SET nom=%s, prenom=%s, telephone=%s,Unite=%s,Materiel=%s,numero_serie=%s,Modele=%s,Nom_technicien=%s,date=%s,diagnostics=%s,solutions_propose=%s,statut=%s WHERE matricule = %s",
                        (nom_entry.get(),prenom_entry.get(),telephone_entry.get(),Unite_entry.get(),Materiel_entry.get(),numero_serie_entry.get(),Modele_entry.get(),Nom_technicien_entry.get(),date,diagnostics_entry.get(),solutions_propose_entry.get(),statut, matricule))
            conn.commit()
            messagebox.showinfo("Succès", "Modifications enregistrées avec succès.")
            vider_champs()
            actualiser_liste_client()
            modifier_mode[0] = False
        except mysc.Error as e:
            messagebox.showerror("Erreur", str(e))
        finally:
            cur.close()
            conn.close()

def modifier():
    if not matricule_var.get():
        messagebox.showwarning("Alerte", "Veuillez d'abord sélectionner un Ticket.")
        return
    modifier_mode[0] = True
    for entry in [nom_entry,prenom_entry,telephone_entry,Unite_entry,Materiel_entry,numero_serie_entry,Modele_entry,Nom_technicien_entry,diagnostics_entry,solutions_propose_entry]:
        entry.config(state=NORMAL)
    # Activer les listes déroulantes de date
    jour_combo.config(state='normal')
    mois_combo.config(state='normal')
    annee_combo.config(state='normal')
    # Activer les boutons radio de statut
    for btn in statut_buttons:
        btn.config(state=NORMAL)
    messagebox.showinfo("Modification", "Une fois la modification terminée, Cliquez sur 'Enregistrer' pour valider.")

def supprimer():
    if messagebox.askquestion("Confirmation", "Voulez-vous supprimer ce Ticket ?") == 'yes':
        matricule = matricule_var.get()
        try:
            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM Client WHERE matricule=%s", (matricule,))
            conn.commit()
            messagebox.showinfo("Succès", "Ticket supprimé.")
            vider_champs()
            actualiser_liste_client()
        except mysc.Error as e:
            messagebox.showerror("Erreur", str(e))
        finally:
            cur.close()
            conn.close()

# Vider les champs et générer un nouveau matricule
def vider_champs():
    matricule_var.set(count_client())
    for entry in [nom_entry,prenom_entry,telephone_entry,Unite_entry,Materiel_entry,numero_serie_entry,Modele_entry,Nom_technicien_entry,diagnostics_entry,solutions_propose_entry]:
        entry.config(state=NORMAL)
        entry.delete(0, END)
    # Réinitialiser la date à aujourd'hui
    from datetime import date
    today = date.today()
    jour_var.set(str(today.day))
    mois_var.set(str(today.month))
    annee_var.set(str(today.year))
    jour_combo.config(state='normal')
    mois_combo.config(state='normal')
    annee_combo.config(state='normal')
    # Réinitialiser le statut à "helpdesk"
    statut_var.set("helpdesk")
    for btn in statut_buttons:
        btn.config(state=NORMAL)

# Suivi du dernier client sélectionné
dernier_client_selectionne = [""]

def reagir_clic(event):
    global dernier_client_selectionne
    selected = tableau.focus()
    if not selected:
        return

    valeurs = tableau.item(selected, 'values')
    matricule_actuel = valeurs[0]

    if matricule_actuel == dernier_client_selectionne[0]:
        vider_champs()
        for entry in [nom_entry,prenom_entry,telephone_entry,Unite_entry,Materiel_entry,numero_serie_entry,Modele_entry,Nom_technicien_entry,diagnostics_entry,solutions_propose_entry]:
            entry.config(state=NORMAL)
        jour_combo.config(state='normal')
        mois_combo.config(state='normal')
        annee_combo.config(state='normal')
        for btn in statut_buttons:
            btn.config(state=NORMAL)
        tableau.selection_remove(tableau.focus())
        modifier_mode[0] = False
        dernier_client_selectionne[0] = ""
    else:
        matricule_var.set(matricule_actuel)
        entries_data = [valeurs[1], valeurs[2], valeurs[3], valeurs[4], valeurs[5], valeurs[6], valeurs[7], valeurs[8], valeurs[10], valeurs[11]]
        for entry, value in zip([nom_entry,prenom_entry,telephone_entry,Unite_entry,Materiel_entry,numero_serie_entry,Modele_entry,Nom_technicien_entry,diagnostics_entry,solutions_propose_entry], entries_data):
            entry.config(state=NORMAL)
            entry.delete(0, END)
            entry.insert(0, value)
            entry.config(state=DISABLED)
        
        # Gérer le champ date séparément
        set_date(valeurs[9])
        jour_combo.config(state='disabled')
        mois_combo.config(state='disabled')
        annee_combo.config(state='disabled')
        
        # Gérer le statut
        statut_var.set(valeurs[12])
        for btn in statut_buttons:
            btn.config(state=DISABLED)
        
        modifier_mode[0] = False
        dernier_client_selectionne[0] = matricule_actuel

# Fonction pour filtrer les tickets selon le statut
# Fonction pour filtrer les tickets selon le statut
def filtrer_tickets(filtre):
    for i in tableau.get_children():
        tableau.delete(i)
    
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        
        if filtre == "tous":
            cur.execute("SELECT * FROM Client ORDER BY date DESC")
            label_titre.config(text="Liste de tous les Tickets")
        elif filtre == "non_termines":
            cur.execute("SELECT * FROM Client WHERE statut != 'terminé' ORDER BY date DESC")
            label_titre.config(text="Liste des Tickets non clôturés")
        elif filtre == "terminé":
            cur.execute("SELECT * FROM Client WHERE statut = 'terminé' ORDER BY date DESC")
            label_titre.config(text="Liste des Tickets terminés")
        elif filtre == "labo":
            cur.execute("SELECT * FROM Client WHERE statut = 'labo' ORDER BY date DESC")
            label_titre.config(text="Liste des Tickets au Labo")
        elif filtre == "prestataire":
            cur.execute("SELECT * FROM Client WHERE statut = 'prestataire' ORDER BY date DESC")
            label_titre.config(text="Liste des Tickets chez le Prestataire")
        elif filtre == "helpdesk":
            cur.execute("SELECT * FROM Client WHERE statut = 'helpdesk' ORDER BY date DESC")
            label_titre.config(text="Liste des Tickets Helpdesk")
        
        rows = cur.fetchall()
        for row in rows:
            tableau.insert("", END, values=row)
        
        # Afficher le nombre de tickets
        nombre_tickets = len(rows)
        label_titre.config(text=f"{label_titre.cget('text')} ({nombre_tickets} ticket{'s' if nombre_tickets > 1 else ''})")
        
    except Exception as e:
        print("Erreur lors du chargement :", e)
    finally:
        cur.close()
        conn.close()


def actualiser_liste_client():
    # Par défaut, afficher les tickets non terminés
    filtrer_tickets("non_termines")

# Interface
root = Tk()
root.title("Gestion des tickets - Eneo Cameroon")
root.configure(bg="#6a7c7b")
root.geometry("1400x700")

matricule_var = StringVar(value=count_client())
modifier_mode = [False]
statut_var = StringVar(value="helpdesk")

# Variables pour la date
from datetime import date
today = date.today()
jour_var = StringVar(value=str(today.day))
mois_var = StringVar(value=str(today.month))
annee_var = StringVar(value=str(today.year))

titre = Label(root, text="APPLICATION DE GESTION DES TICKETS", font=("Helvetica", 18, "bold"), fg='black', bg='#6a7c7b')
titre.grid(row=0, column=0, columnspan=2, pady=20)

form_frame = Frame(root, bg='#6a7c7b')
form_frame.grid(row=1, column=0, padx=20, sticky="n")

Label(form_frame, text="Matricule:", bg='#6a7c7b').grid(row=0, column=0, sticky="w")
matricule_entry = Entry(form_frame, textvariable=matricule_var, state=DISABLED)
matricule_entry.grid(row=0, column=1, pady=5)

labels = ["nom","prenom","telephone","Unite","Materiel","numero de serie","Modele","Nom_technicien","diagnostics","solutions proposées"]
entries = []
for i, lab in enumerate(labels):
    Label(form_frame, text=f"{lab}:", bg='#6a7c7b').grid(row=i+1, column=0, sticky="w")
    e = Entry(form_frame)
    e.grid(row=i+1, column=1, pady=5)
    entries.append(e)
     
nom_entry,prenom_entry,telephone_entry,Unite_entry,Materiel_entry,numero_serie_entry,Modele_entry,Nom_technicien_entry,diagnostics_entry,solutions_propose_entry = entries

# Champ Date avec listes déroulantes
Label(form_frame, text="Date:", bg='#6a7c7b').grid(row=11, column=0, sticky="w")
date_frame = Frame(form_frame, bg='#6a7c7b')
date_frame.grid(row=11, column=1, pady=5, sticky="w")

# Jour (1-31)
Label(date_frame, text="J:", bg='#6a7c7b').pack(side=LEFT)
jour_combo = ttk.Combobox(date_frame, textvariable=jour_var, width=3, state='readonly')
jour_combo['values'] = [str(i) for i in range(1, 32)]
jour_combo.pack(side=LEFT, padx=2)

# Mois (1-12)
Label(date_frame, text="M:", bg='#6a7c7b').pack(side=LEFT, padx=(5,0))
mois_combo = ttk.Combobox(date_frame, textvariable=mois_var, width=3, state='readonly')
mois_combo['values'] = [str(i) for i in range(1, 13)]
mois_combo.pack(side=LEFT, padx=2)

# Année (2020-2030)
Label(date_frame, text="A:", bg='#6a7c7b').pack(side=LEFT, padx=(5,0))
annee_combo = ttk.Combobox(date_frame, textvariable=annee_var, width=6, state='readonly')
annee_combo['values'] = [str(i) for i in range(2020, 2031)]
annee_combo.pack(side=LEFT, padx=2)

# Champ Statut avec boutons radio sur 2 lignes
Label(form_frame, text="Statut:", bg='#6a7c7b').grid(row=12, column=0, sticky="nw", pady=5)
statut_frame = Frame(form_frame, bg='#6a7c7b')
statut_frame.grid(row=12, column=1, pady=5, sticky="w")

statut_buttons = []

# Première ligne : Labo et Prestataire
ligne1 = Frame(statut_frame, bg='#6a7c7b')
ligne1.pack(anchor='w')

rb_labo = Radiobutton(ligne1, text="Labo", variable=statut_var, value="labo", bg='#6a7c7b')
rb_labo.pack(side=LEFT, padx=5)
statut_buttons.append(rb_labo)

rb_prestataire = Radiobutton(ligne1, text="Prestataire", variable=statut_var, value="prestataire", bg='#6a7c7b')
rb_prestataire.pack(side=LEFT, padx=5)
statut_buttons.append(rb_prestataire)

# Deuxième ligne : Helpdesk et Terminé
ligne2 = Frame(statut_frame, bg='#6a7c7b')
ligne2.pack(anchor='w')

rb_helpdesk = Radiobutton(ligne2, text="Helpdesk", variable=statut_var, value="helpdesk", bg='#6a7c7b')
rb_helpdesk.pack(side=LEFT, padx=5)
statut_buttons.append(rb_helpdesk)

rb_termine = Radiobutton(ligne2, text="Terminé", variable=statut_var, value="terminé", bg='#6a7c7b')
rb_termine.pack(side=LEFT, padx=5)
statut_buttons.append(rb_termine)

Button(form_frame, text="Enregistrer", command=ajouter, bg='#6a7c7b', fg='black').grid(row=13, column=0, pady=10)
Button(form_frame, text="Modifier", command=modifier, bg='#6a7c7b', fg='black').grid(row=13, column=1)
Button(form_frame, text="Supprimer", command=supprimer, bg='#6a7c7b', fg='black').grid(row=14, column=0, columnspan=2, pady=5)

# Affichage liste client
liste_frame = Frame(root, bg='#6a7c7b')
liste_frame.grid(row=1, column=1, padx=10, sticky="nsew")

# Configurer le redimensionnement
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

# Frame pour le titre et les boutons de filtrage
header_frame = Frame(liste_frame, bg='#6a7c7b')
header_frame.pack(pady=5, fill=X)

label_titre = Label(header_frame, text="Liste des Tickets non clôturés", font=("Helvetica", 14, "bold"), bg="#6a7c7b", fg="black")
label_titre.pack(side=TOP, pady=5)

# Frame pour les boutons de filtrage
filtres_frame = Frame(header_frame, bg='#6a7c7b')
filtres_frame.pack(side=TOP, pady=5)

Label(filtres_frame, text="Filtrer par:", bg='#6a7c7b', font=("Helvetica", 10, "bold")).pack(side=LEFT, padx=5)

Button(filtres_frame, text="Tous", command=lambda: filtrer_tickets("tous"), bg='#87CEEB', fg='black', width=10).pack(side=LEFT, padx=2)
Button(filtres_frame, text="Non clôturés", command=lambda: filtrer_tickets("non_termines"), bg='#90EE90', fg='black', width=12).pack(side=LEFT, padx=2)
Button(filtres_frame, text="Helpdesk", command=lambda: filtrer_tickets("helpdesk"), bg='#FFD700', fg='black', width=10).pack(side=LEFT, padx=2)
Button(filtres_frame, text="Labo", command=lambda: filtrer_tickets("labo"), bg='#FFA500', fg='black', width=10).pack(side=LEFT, padx=2)
Button(filtres_frame, text="Prestataire", command=lambda: filtrer_tickets("prestataire"), bg='#DDA0DD', fg='black', width=12).pack(side=LEFT, padx=2)
Button(filtres_frame, text="Terminés", command=lambda: filtrer_tickets("terminé"), bg='#FF6B6B', fg='white', width=10).pack(side=LEFT, padx=2)

# Scrollbars vertical et horizontal
scrollbar_y = Scrollbar(liste_frame, orient=VERTICAL)
scrollbar_y.pack(side=RIGHT, fill=Y)

scrollbar_x = Scrollbar(liste_frame, orient=HORIZONTAL)
scrollbar_x.pack(side=BOTTOM, fill=X)

entetes = ["Matricule","nom","prenom","telephone","Unite","Materiel","numero de serie","Modele","Nom_technicien","date","diagnostics","solutions proposées","statut"]
tableau = ttk.Treeview(liste_frame, columns=entetes, show="headings", 
                       yscrollcommand=scrollbar_y.set,
                       xscrollcommand=scrollbar_x.set,
                       height=15)

# Largeurs optimisées
largeurs = {"Matricule": 90, "nom": 70, "prenom": 70, "telephone": 85, "Unite": 60, 
            "Materiel": 70, "numero de serie": 85, "Modele": 70, "Nom_technicien": 90,
            "date": 75, "diagnostics": 100, "solutions proposées": 100, "statut": 70}

for col in entetes:
    tableau.heading(col, text=col)
    tableau.column(col, width=largeurs[col])

tableau.pack(fill=BOTH, expand=True)
tableau.bind("<ButtonRelease-1>", reagir_clic)

scrollbar_y.config(command=tableau.yview)
scrollbar_x.config(command=tableau.xview)

actualiser_liste_client()
root.mainloop()