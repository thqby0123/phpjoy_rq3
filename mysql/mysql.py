import pymysql

from unserialize import *

HOST = '10.176.36.21'
PORT = 21306
USER = 'root'
PWD = 'password'
DATABASE = 'code_coverage'

db = pymysql.connect(host = HOST,
                     port = PORT,
                     user = USER,
                     password = PWD,
                     database = DATABASE)


def query_cve(cve_id, db):
    curses = db.cursor()
    sql = f'''select covered_files.file_name,covered_lines.line_number from covered_files,covered_lines,tests
where covered_files.fk_test_id = tests.id and tests.test_group = {cve_id} and covered_files.id = covered_lines.fk_file_id'''
    curses.execute(sql)
    result = curses.fetchall()
    curses.close()
    return result

result = query_cve('\'CVE-2014-9701\'',db)
path = 'E:\FDULab\Joern\EnhancedPHPJoern\CMS\mantisbt-1.2.15\\files\www'
res = {}
for line in result:
    if res.get(line[0],None) == None:
        res[line[0]] = []
    res[line[0]].append(line[1])
print(res)
sink_list = {}
source_list = {}

for key in res.keys():
    if key.startswith("/var"):
        continue
    p = path

    for i in key.split('/')[2:]:
        p += '\\'
        p += i;
    with open(p,"r",encoding='utf-8',errors='ignore') as f:
        lines = f.readlines();
        for i in range(len(lines)):
            if i+1 in res[key]:
                if key == '/app/permalink_page.php' and i == 38:
                    print(1)
                if judge_sink(lines[i],["echo", "print", "print_r"]):
                    if sink_list.get(key,None) == None:
                        sink_list[key] = []
                    sink_list[key].append(i+1)
                if judge_source(lines[i]):
                    if source_list.get(key, None) == None:
                        source_list[key] = []
                    source_list[key].append(i + 1)

print(sink_list)
print(source_list)
