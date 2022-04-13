
import re
import time
import math
from selenium import webdriver

def scrape_my_like():
    """Enregistre la page html"""
    url = "https://www.soundcloud.com/Z0ul0u25/likes"
    nav = webdriver.Firefox(executable_path=r"geckodriver.exe")
    nav.get(url)
    time.sleep(2)  # Donne 2 sec pour ouvrir le nav
    scroll_pause_time = 1 # Pause entre les scroll
    screen_height = nav.execute_script("return window.screen.height;")
    i = 1

    while True: #scroll
        nav.execute_script(f"window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = nav.execute_script("return document.body.scrollHeight;")
        if (screen_height) * i > scroll_height:
            break
    data = nav.page_source

    with open('SoundCloudLikesRaw.html', 'w', encoding="utf-8") as file:
        #Écrit le résultat dans un fichier html
        file.write(data)


def html_to_csv():
    """Transforme la page like en format CSV"""
    # Regex à remplacer
    search_text = []
    search_text.append(r"^.+<\/header>") # header
    search_text.append(r"^.*<div class=\"soundList lazyLoadingList\">") # Le reste au top
    search_text.append(r"<div class=\"l-footer.*") # Le reste en bas
    search_text.append(r"<li class=\"soundList__item\"><div>  <div role=\"group\" class=\"sound playlist streamContext\".*?(</div>\s*?){7}(</li>)") # Les playlists
    search_text.append(r"\s*<(?!\/?span).*?>\s*") # Les span useless
    search_text.append(r"<span style.*?(Écouter|Non disponible|$)") # Plus de span useless
    search_text.append(r"<.{15}visuallyhidden(.+?<\/span>){2}") # Encore plus de span useless
    search_text.append(r"\s*</span><span class=\"(sc-truncate)?\">|</span><span class=\"sc-truncate sc-tagContent\">|(<\/span>)?<span class=\"soundTitle__usernameText\">|</span>$") # Span entre les mots qu'on veut garder
    search_text.append(r"</span>.*?;") # RIP au Canada
    search_text.append(r"\n {14}|$") # Espace de trop
    search_text.append(r"^;") # Première virgule
    search_text.append(r"&amp;") # &
    search_text.append(r"&lt;") # <
    search_text.append(r"&gt;") # >

    # String de remplacememnt
    replace_text = []
    replace_text.append("")
    replace_text.append("")
    replace_text.append("")
    replace_text.append("")
    replace_text.append("")
    replace_text.append("")
    replace_text.append("")
    replace_text.append(";")
    replace_text.append(";x")
    replace_text.append("\n")
    replace_text.append("")
    replace_text.append("&")
    replace_text.append("<")
    replace_text.append(">")


    with open('SoundCloudLikesRaw.html', 'r', encoding="utf-8") as file:

        print("Fichier ouvert")
        # Lit le fichier dans une variable
        data = file.read()
        # Cherche et remplace les strings
        for i, shit in enumerate(search_text):
            if len(shit) > 20:
                print("remplacement de " + shit[0:20] + " ...")
            else:
                print("remplacement de " + shit)
            data = re.sub(search_text[i], replace_text[i], data, flags=re.DOTALL)
        # Ajoute un ID au tounes
        nb_tunes = data.count("\n")-2
        for i in range(nb_tunes, 0, -1):
            data = re.sub(r"\n(?!\d*;)", f"\n{i};", data, 1)


    with open('SoundCloudLikesReformed.csv', 'w', encoding="utf-8") as file:
        #En-tête du CSV
        file.write("ID;Artiste;Titre;Genre;Restraint")
        #Juste un compteur pour finir la job
        print(str(data.count("\n")-2)+" titres")
        #Écriture finale au fichier
        file.write(data)

if __name__ == "__main__":
    debut = time.time()
    print("Scrape l'HTML du navigateur Firefox...")
    scrape_my_like()
    fin = time.time()
    total = fin - debut
    print(f"Temps prit pour scrapper: {math.floor(total/60)}:{total%60}")

    print("Convertion en CSV...")
    html_to_csv()
    print("Convertion terminé")
