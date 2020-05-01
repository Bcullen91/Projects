import xlsxwriter
import time

row = 0
column = 0
email = 'testEmailStringHere'
listofletters = list(email)
bits = len(listofletters) - 1
a = []

workbook = xlsxwriter.Workbook(email + '.xlsx')
worksheet = workbook.add_worksheet('safeway')

a1 = 'Used?'
b1 = 'Email'
c1 = 'Password'
d1 = 'Account Number'
password = 'test123'
accnum = 12345

worksheet.write(row, column, a1)
column += 1
worksheet.write(row, column, b1)
column += 1
worksheet.write(row, column, c1)
column += 1
worksheet.write(row, column, d1)

column = 1
row = 1


for n in range(1, 2**bits):
    b = (''.join(listofletters[i] + ('.' if n & (1<<i) else '') for i in range(bits)) + listofletters[-1])
    a.append(''.join(listofletters[i] + ('.' if n & (1<<i) else '') for i in range(bits)) + listofletters[-1])
    if len(b) <= 30:
        worksheet.write(row, column, b + "@gmail.com")
        column += 1
        worksheet.write(row, column, password)
        column += 1
        worksheet.write(row, column, accnum)
        accnum += 1
        column = 1
        row += 1
    else:
        continue

workbook.close()
