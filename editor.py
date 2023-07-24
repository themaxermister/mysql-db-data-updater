import re

########## QUESTIONS DATA EDITOR ##########
color_code_dict = {
    "#FF0000": "red",
    "#008000": "green",
    "#0000FF": "blue",
    "#000000": "black",
    "#FFFFFF": "white",
}

def exportQnsTableValues(cnx, columns, qns_tag):
    cursor = cnx.cursor()
    query = f"""
    SELECT {", ".join(columns)}
    FROM QUESTIONS qns
    INNER JOIN (SELECT question_id, tag_id FROM QUESTION_TAGS qt INNER JOIN TAGS t ON qt.tag_id = t.id WHERE t.name = '{qns_tag}') tags ON tags.question_id = qns.id
    """
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data

def replaceH1TextColor(match):
    text_color = color_code_dict.get(match.group(2).upper(), match.group(2))
    return f"<h1 class=\"text-{text_color}\">{match.group(3)}</h1>"

def replaceButtonColor(match):
    btn_color = color_code_dict.get(match.group(2).upper(), match.group(2))
    return f"<button class=\"stroop-button text-white background-{btn_color}\">"

def removeInlineCSS(html):
    h1_text_pattern = r"(<h1 style=\"color:(.*?)\">(.*?)</h1>)"
    html = re.sub(h1_text_pattern, replaceH1TextColor, html)
    btn_pattern = r"(<button class=\"stroop-button\" style=\".+?background-color:(.*?)(?=;).*?\">)"
    html = re.sub(btn_pattern, replaceButtonColor, html)
    return html

###########################################################################################
