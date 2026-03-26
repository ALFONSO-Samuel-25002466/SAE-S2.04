import os
import random
import unicodedata
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("fr_FR")
random.seed(42)
Faker.seed(42)

NB_ORGANISATIONS = 20
NB_MODELES = 100
NB_MACHINES = 2500
NB_TENRACS = 5000
NB_REPAS = 1200
NB_SAUCES = 12

FICHIER_SQL = "Extension.sql"

_insert_counter = 0

def sql_escape(txt: str) -> str:
    return txt.replace("'", "''")

def strip_accents(txt: str) -> str:
    txt = unicodedata.normalize("NFKD", txt)
    txt = txt.encode("ascii", "ignore").decode("ascii")
    return txt

def clean_email_part(txt: str) -> str:
    txt = strip_accents(txt).lower()
    txt = txt.replace(" ", "").replace("-", "").replace("'", "")
    return txt

def make_email(full_name: str, i: int) -> str:
    parts = full_name.split()
    prenom = clean_email_part(parts[0])
    nom = clean_email_part(parts[-1])
    return f"{prenom}.{nom}{i}@tenrac.fr"

def random_date(days_back_min=30, days_back_max=1000) -> str:
    days_ago = random.randint(days_back_min, days_back_max)
    d = datetime.now() - timedelta(days=days_ago)
    return d.strftime("%Y-%m-%d")

def random_timestamp(days_back_min=1, days_back_max=700) -> str:
    days_ago = random.randint(days_back_min, days_back_max)
    base = datetime.now() - timedelta(days=days_ago)
    dt = base.replace(
        hour=random.randint(8, 22),
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
        microsecond=0,
    )
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def write_insert(f, stmt: str) -> None:
    global _insert_counter
    line = stmt if stmt.rstrip().endswith(";") else stmt.rstrip() + ";"
    f.write(line + "\n")
    _insert_counter += 1

def weighted_nullable_choice(values, weights, null_probability):
    if random.random() < null_probability:
        return None
    return random.choices(values, weights=weights, k=1)[0]

GRADES = ["Affilié", "Sympathisant", "Adhérent", "Chevalier / Dame", "Grand Chevalier / Haute Dame", "Commandeur", "Grand'Croix"]
GRADE_WEIGHTS = [35, 25, 18, 12, 6, 3, 1]

RANGS = ["Novice", "Compagnon"]
RANG_WEIGHTS = [60, 40]
RANG_NULL_PROBABILITY = 0.50

TITRES = ["Philanthrope", "Protecteur", "Honorable"]
TITRE_WEIGHTS = [50, 30, 20]
TITRE_NULL_PROBABILITY = 0.75

DIGNITES = ["Maître", "Grand Chancelier", "Grand Maître"]
DIGNITE_WEIGHTS = [60, 30, 10]
DIGNITE_NULL_PROBABILITY = 0.95

ENTRETIENS = ["Nettoyage complet", "Révision standard", "Contrôle sécurité", "Détartrage", "Remplacement résistance", "Contrôle thermostat"]
PERIODICITES = ["Mensuelle", "Trimestrielle", "Semestrielle", "Annuelle"]
SAUCES = ["Mayonnaise", "Ketchup", "Samouraï", "Blanche", "Barbecue", "Poivre", "Curry", "Aïl", "Moutarde", "Fromagère", "Piquante", "Burger"]

INGREDIENTS_DATA = [
    ("Tomate", "légume", 1, "aucun"), ("Brocoli", "légume", 1, "aucun"), ("Courgette", "légume", 1, "aucun"),
    ("Poivron", "légume", 1, "aucun"), ("Oignon", "légume", 1, "aucun"), ("Champignon", "légume", 1, "aucun"),
    ("Pomme de terre", "légume", 1, "aucun"), ("Carotte", "légume", 1, "aucun"), ("Aubergine", "légume", 1, "aucun"),
    ("Poulet", "viande", 0, "aucun"), ("Bœuf", "viande", 0, "aucun"), ("Jambon", "charcuterie", 0, "aucun"),
    ("Bacon", "charcuterie", 0, "aucun"), ("Saumon", "poisson", 0, "poisson"), ("Thon", "poisson", 0, "poisson"),
    ("Fromage à raclette", "fromage", 0, "lait"), ("Mozzarella", "fromage", 0, "lait"), ("Chèvre", "fromage", 0, "lait"),
    ("Crème fraîche", "laitage", 0, "lait"), ("Beurre", "matière grasse", 0, "lait"),
    ("Mayonnaise base", "sauce", 0, "œuf"), ("Ketchup base", "sauce", 0, "aucun"), ("Moutarde base", "sauce", 0, "aucun")
]

NB_COMPOSANTS = len(INGREDIENTS_DATA)
NB_PLATS = 30

def generer():
    global _insert_counter
    _insert_counter = 0

    with open(FICHIER_SQL, "w", encoding="utf-8") as f:
        f.write("BEGIN TRANSACTION;\n\n")

        organisation_ids = list(range(1, NB_ORGANISATIONS + 1))
        for org_id in organisation_ids:
            write_insert(f, f"INSERT INTO organisation (id_Organisation) VALUES ({org_id});")
        f.write("\n")

        organisme_names = []
        for org_id in organisation_ids:
            nom_o = sql_escape(f"Organisme_{org_id}_{fake.company()[:20]}")
            siret = fake.numerify(text="##############")
            organisme_names.append(nom_o)
            write_insert(f, f"INSERT INTO Organisme (nom_O, Numero_SIRET) VALUES ('{nom_o}', '{siret}');")
        f.write("\n")

        grade_parents = {"Affilié": None, "Sympathisant": "Affilié", "Adhérent": "Sympathisant", "Chevalier / Dame": "Adhérent", "Grand Chevalier / Haute Dame": "Chevalier / Dame", "Commandeur": "Grand Chevalier / Haute Dame", "Grand'Croix": "Commandeur"}
        for g in GRADES:
            parent = grade_parents[g]
            parent_sql = "NULL" if parent is None else f"'{sql_escape(parent)}'"
            write_insert(f, f"INSERT INTO Grade (nom_G, nom_G_1) VALUES ('{sql_escape(g)}', {parent_sql});")
        f.write("\n")

        titre_parents = {"Philanthrope": None, "Protecteur": "Philanthrope", "Honorable": "Protecteur"}
        for t in TITRES:
            parent = titre_parents[t]
            parent_sql = "NULL" if parent is None else f"'{sql_escape(parent)}'"
            write_insert(f, f"INSERT INTO Titre (nom_T, nom_T_1) VALUES ('{sql_escape(t)}', {parent_sql});")
        f.write("\n")

        dignite_parents = {"Maître": None, "Grand Chancelier": "Maître", "Grand Maître": "Grand Chancelier"}
        for d in DIGNITES:
            parent = dignite_parents[d]
            parent_sql = "NULL" if parent is None else f"'{sql_escape(parent)}'"
            write_insert(f, f"INSERT INTO Dignite (nom_D, nom_D_1) VALUES ('{sql_escape(d)}', {parent_sql});")
        f.write("\n")

        rang_parents = {"Novice": None, "Compagnon": "Novice"}
        for r in RANGS:
            parent = rang_parents[r]
            parent_sql = "NULL" if parent is None else f"'{sql_escape(parent)}'"
            write_insert(f, f"INSERT INTO Rang (nom_R, nom_R_1) VALUES ('{sql_escape(r)}', {parent_sql});")
        f.write("\n")

        ordre_names = []
        for i, org_id in enumerate(organisation_ids, start=1):
            nom_ordre = f"Ordre_{i}"
            ordre_names.append(nom_ordre)
            write_insert(f, f"INSERT INTO Ordre (nom_Ordre, id_Organisation) VALUES ('{sql_escape(nom_ordre)}', {org_id});")
        f.write("\n")

        adresse_names = []
        used_addresses = set()
        target_nb_addresses = max(NB_REPAS * 2, 40)
        while len(adresse_names) < target_nb_addresses:
            adresse = fake.address().replace("\n", ", ")
            adresse = sql_escape(adresse[:50])
            if adresse in used_addresses: continue
            used_addresses.add(adresse)
            adresse_names.append(adresse)
            ordre = random.choice(ordre_names)
            write_insert(f, f"INSERT INTO Adresses (Nom_A, nom_Ordre) VALUES ('{adresse}', '{sql_escape(ordre)}');")
        f.write("\n")

        club_names = []
        for i, org_id in enumerate(organisation_ids, start=1):
            nom_club = f"Club_{i}"
            club_names.append(nom_club)
            write_insert(f, f"INSERT INTO Club (nom_Club, nom_Ordre, id_Organisation) VALUES ('{sql_escape(nom_club)}', '{sql_escape(ordre_names[i - 1])}', {org_id});")
        f.write("\n")

        machine_ids = list(range(1, NB_MACHINES + 1))
        for machine_id in machine_ids:
            write_insert(f, f"INSERT INTO Machine (id_Machine, nom) VALUES ({machine_id}, 'Machine_{machine_id}');")
        f.write("\n")

        modele_ids = list(range(1, NB_MODELES + 1))
        for modele_id in modele_ids:
            entretien = sql_escape(random.choice(ENTRETIENS))
            periodicite = sql_escape(random.choice(PERIODICITES))
            write_insert(f, f"INSERT INTO Modele (id_Modele, Entretien, Periodicite) VALUES ({modele_id}, '{entretien}', '{periodicite}');")
        f.write("\n")

        for machine_id in machine_ids:
            modele_id = random.choice(modele_ids)
            write_insert(f, f"INSERT INTO Type (id_Machine, id_Modele) VALUES ({machine_id}, {modele_id});")
        f.write("\n")

        composant_ids = []
        ingredient_ids = []
        legume_ids = []
        for i, (nom, type_ing, est_legume, allergene) in enumerate(INGREDIENTS_DATA, start=1):
            composant_ids.append(i)
            ingredient_ids.append(i)
            write_insert(f, f"INSERT INTO Composant (id_Composant, nom_ingredient, type_ingredient, legume, alergene) VALUES ({i}, '{sql_escape(nom)}', '{sql_escape(type_ing)}', {est_legume}, '{sql_escape(allergene)}');")
            if est_legume == 1:
                legume_ids.append(i)
                write_insert(f, f"INSERT INTO Legume (id_Composant, verifier) VALUES ({i}, 1);")
            write_insert(f, f"INSERT INTO Ingredient (id_I, id_Composant) VALUES ({i}, {i});")
        f.write("\n")

        sauce_names = []
        for nom in SAUCES:
            sauce_names.append(nom)
            write_insert(f, f"INSERT INTO Sauce (Nom) VALUES ('{sql_escape(nom)}');")
        f.write("\n")

        plat_ids = list(range(1, NB_PLATS + 1))
        for plat_id in plat_ids:
            comp_legume = random.choice(legume_ids)
            write_insert(f, f"INSERT INTO Plats (id_P, Raclette, id_Composant) VALUES ({plat_id}, 'Plat_{plat_id}', {comp_legume});")
        f.write("\n")

        tenrac_ids = list(range(1, NB_TENRACS + 1))
        for id_t in tenrac_ids:
            full_name = fake.name()
            nom = sql_escape(full_name)
            courriel = sql_escape(make_email(full_name, id_t))
            num_tel = random.randint(600000000, 799999999)
            adr = sql_escape(fake.address().replace("\n", ", "))[:50]
            rfid = sql_escape(fake.hexify(text="^^:^^:^^:^^:^^:^^", upper=True))
            id_org = random.choice(organisation_ids)
            nom_o = organisme_names[id_org - 1]
            nom_g = random.choices(GRADES, weights=GRADE_WEIGHTS, k=1)[0]
            nom_r = weighted_nullable_choice(RANGS, RANG_WEIGHTS, RANG_NULL_PROBABILITY)
            nom_t = weighted_nullable_choice(TITRES, TITRE_WEIGHTS, TITRE_NULL_PROBABILITY)
            nom_d = weighted_nullable_choice(DIGNITES, DIGNITE_WEIGHTS, DIGNITE_NULL_PROBABILITY)
            nom_r_sql = "NULL" if nom_r is None else f"'{sql_escape(nom_r)}'"
            nom_t_sql = "NULL" if nom_t is None else f"'{sql_escape(nom_t)}'"
            nom_d_sql = "NULL" if nom_d is None else f"'{sql_escape(nom_d)}'"
            write_insert(f, f"INSERT INTO Tenrac (id_T, nom, courriel, num_tel, adr, RFID, id_Organisation, nom_O, nom_R, nom_G, nom_T, nom_D) VALUES ({id_t}, '{nom}', '{courriel}', '0{num_tel}', '{adr}', '{rfid}', {id_org}, '{sql_escape(nom_o)}', {nom_r_sql}, '{sql_escape(nom_g)}', {nom_t_sql}, {nom_d_sql});")
        f.write("\n")

        historique_ids = []
        for idx, machine_id in enumerate(machine_ids, start=1):
            historique_ids.append(idx)
            d = random_date(30, 900)
            write_insert(f, f"INSERT INTO Historique (id_H, date_, id_Machine) VALUES ({idx}, '{d}', {machine_id});")
        f.write("\n")

        repas_ids = list(range(1, NB_REPAS + 1))
        for id_r in repas_ids:
            nom = f"Repas_{id_r}"
            dt = random_timestamp(1, 700)
            nom_a = random.choice(adresse_names)
            write_insert(f, f"INSERT INTO Repas (Id_R, Nom, Date_, Nom_A) VALUES ({id_r}, '{sql_escape(nom)}', '{dt}', '{sql_escape(nom_a)}');")
        f.write("\n")

        certif_pairs = set()
        target_certif = min(max(NB_MACHINES * 2, 40), NB_TENRACS * NB_MACHINES)
        while len(certif_pairs) < target_certif:
            certif_pairs.add((random.choice(tenrac_ids), random.choice(machine_ids)))
        for id_t, machine_id in sorted(certif_pairs):
            write_insert(f, f"INSERT INTO Certif (id_T, id_Machine) VALUES ({id_t}, {machine_id});")
        f.write("\n")

        assembler_pairs = set()
        target_assembler = min(80, len(composant_ids) * len(sauce_names))
        while len(assembler_pairs) < target_assembler:
            assembler_pairs.add((random.choice(composant_ids), random.choice(sauce_names)))
        for id_comp, nom_sauce in sorted(assembler_pairs):
            write_insert(f, f"INSERT INTO Assembler (id_Composant, Nom) VALUES ({id_comp}, '{sql_escape(nom_sauce)}');")
        f.write("\n")

        composer_pairs = set()
        target_composer = min(120, len(plat_ids) * len(ingredient_ids))
        while len(composer_pairs) < target_composer:
            composer_pairs.add((random.choice(plat_ids), random.choice(ingredient_ids)))
        for id_p, id_i in sorted(composer_pairs):
            write_insert(f, f"INSERT INTO Composer (id_P, id_I) VALUES ({id_p}, {id_i});")
        f.write("\n")

        extra_pairs = set()
        target_extra = min(60, len(plat_ids) * len(sauce_names))
        while len(extra_pairs) < target_extra:
            extra_pairs.add((random.choice(plat_ids), random.choice(sauce_names)))
        for id_p, nom_sauce in sorted(extra_pairs):
            write_insert(f, f"INSERT INTO Extra (id_P, Nom) VALUES ({id_p}, '{sql_escape(nom_sauce)}');")
        f.write("\n")

        comporter_pairs = set()
        target_comporter = min(180, len(repas_ids) * len(plat_ids))
        while len(comporter_pairs) < target_comporter:
            comporter_pairs.add((random.choice(repas_ids), random.choice(plat_ids)))
        for id_r, id_p in sorted(comporter_pairs):
            write_insert(f, f"INSERT INTO Comporter (Id_R, id_P) VALUES ({id_r}, {id_p});")
        f.write("\n")

        partager_pairs = set()
        target_partager = min(max(NB_REPAS * 5, 150), len(repas_ids) * len(tenrac_ids))
        while len(partager_pairs) < target_partager:
            partager_pairs.add((random.choice(tenrac_ids), random.choice(repas_ids)))
        for id_t, id_r in sorted(partager_pairs):
            write_insert(f, f"INSERT INTO Partager (id_T, Id_R) VALUES ({id_t}, {id_r});")
        f.write("\n")

        stocker_pairs = set()
        for id_h in historique_ids:
            stocker_pairs.add((random.choice(organisation_ids), id_h))
        for id_org, id_h in sorted(stocker_pairs):
            write_insert(f, f"INSERT INTO Stocker (id_Organisation, id_H) VALUES ({id_org}, {id_h});")

        f.write("\nCOMMIT;\n")

    print("✅ Génération terminée pour SQLite")
    print(f"   Fichier   : {os.path.abspath(FICHIER_SQL)}")
    print(f"   Inserts   : {_insert_counter:,}")

if __name__ == "__main__":
    generer()