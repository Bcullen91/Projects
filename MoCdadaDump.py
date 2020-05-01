from bs4 import BeautifulSoup
import xlsxwriter
import glob
import re
from operator import itemgetter

workbook = xlsxwriter.Workbook('MoC_ActiveUsers.xlsx')
worksheet = workbook.add_worksheet('AllTimePosts')
row = 0
column = 0
numOfPosts = []
activeUsers = {}
count = 1
worksheet.write(row, column, 'Users')
column += 1
worksheet.write(row, column, '# of Posts')
row += 1
column = 0
post = workbook.add_format({'num_format': '#,##0'})
filePath = '' # Enter your file path here


def clean_Username(user):
    userRaw = user.text
    userClean = userRaw.strip()
    if 'via' in userClean:
        userClean = userClean.split('via @')[0]
        userClean = userClean.strip()
    pattern = re.compile(r'\b\d{2}\.\d{2}\.\d{4}\b')
    userClean = (pattern.split(userClean)[0].strip() if pattern.search(userClean) else userClean)
    return userClean



for file in glob.glob(filePath):
    with open(file, 'r') as chatLog:
        soup = BeautifulSoup(chatLog, 'lxml')
        userName = soup.find_all('div', class_='from_name')
        for user in userName:
            numOfPosts.append(clean_Username(user))
        print('Finished with the ' + str(count) + ' list.')
        count += 1

print(numOfPosts)
for users in numOfPosts:
    num = numOfPosts.count(users)
    if users not in activeUsers:
        activeUsers[users] = str(num)

print(activeUsers)


for key, value in sorted(activeUsers.items(), key=lambda l: int(l[1]), reverse=True):
    worksheet.write(row, column, key)
    column += 1
    worksheet.write(row, column, value, post)
    row += 1
    column = 0

row += 2

worksheet.write(row, column, len(activeUsers))
column += 1
worksheet.write(row, column, len(numOfPosts))
print(len(activeUsers))
print(len(numOfPosts))


workbook.close()