import json

with open('java_stat.json', 'r') as f:
    result = json.load(f)
json.dumps(result, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
table = '''<!DOCTYPE html><html ><head><link href='css/styles.css 'rel='stylesheet' /></head><meta charset='utf-8' /><body><table class='table table-dark'><tr><th>N</th><th>Query count</th><th>Skill</th></tr>'''
count = 0
for obj in result[:10]:
    count += 1
    table += f'<tr><td>{count}</td><td>{obj[1]}</td><td>{obj[0]}</td></tr>'
table += '</table></body>'
# table = table.replace('"','')
# <table>
# <tr><th>текст заголовка</th><th>текст заголовка</th></tr> <!--ряд с ячейками заголовков-->
# <tr><td>данные</td><td>данные</td></tr> <!--ряд с ячейками тела таблицы-->
# </table>
print(table)

with open('Templates/java.html', 'w', encoding='utf-8') as f:
    f.write(table,)
    f.close()

