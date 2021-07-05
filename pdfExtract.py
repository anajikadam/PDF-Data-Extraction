import requests
import re
import json
import pdfplumber
import pandas as pd


def read_pdf(path):
    text = []
    with pdfplumber.open(path) as pdf:
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            text1 = page.extract_text()
            a = text1.split('\n')
            text.extend(a)
    return text

def find_CPR(textls):
    cprrow = []
    for j in textls:
        if 'CPR' in j:
            #print(j)
            cprrow.append(j)
    for c in cprrow:
        if re.findall(r'(\b\d{9})$', c):
            cprno = re.findall(r'(\b\d{9})$', c)[0]
    return cprno

def info(textls):
    def rgx(w):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search 
    for row in textls[:8]:
        if ':' in row:
            p = 'Patient'
            if rgx(p) (row):
                Patient = (row.split(':')[1].replace("Insurance","").strip())
            insu = 'Insurance'
            if rgx(insu) (row):
                Insurance = (row.split(':')[-1].strip())
            a = 'Age'
            if rgx(a) (row):
                age = (row.split(':')[1].replace("Scheme","").strip())
            sc = 'Scheme'
            if rgx(sc) (row):
                scheme = (row.split(':')[-1].strip())
            dr = 'Doctor'
            if rgx(dr) (row):
                dctr = (row.split(':')[1].replace("Branch","").strip())
            br = 'Branch'
            if rgx(br) (row):
                brch = (row.split(':')[-1].strip())
            vs = 'Visit'
            if rgx(vs) (row):
                vsit = (row.split(':')[1]+row.split(':')[2].replace("PIC Add",""))
            addr = 'PIC Add'
            if rgx(addr) (row):
                idd = textls.index(row)
                address = (row.split(':')[-1].strip())
                if address[-1]==',':
                    address = address+ textls[idd+1]
    return Patient, Insurance, age, scheme, dctr,brch,vsit,address

def create_bill(textls):
    bill = {}
    cptcode = []
    desc = []
    qt = []
    vat = []
    price = []
    total = []
    ins_Amt = []
    vat_i = []
    pat_amt = []
    vatp = []
    for rows in textls:
        if ' % ' in rows:
            if 'CPT Code' in rows:
                continue
            rowslst = (rows.split())
            cptcode.append(rowslst[0])
            desc.append(' '.join(rowslst[1:-9]))
            qt.append(rowslst[-9])
            vat.append(rowslst[-8])
            price.append(rowslst[-6])
            total.append(rowslst[-5])
            ins_Amt.append(rowslst[-4])
            vat_i.append(rowslst[-3])
            pat_amt.append(rowslst[-2])
            vatp.append(rowslst[-1])
    bill['CPT Code'] = cptcode
    bill['Description'] = desc
    bill['Qty'] = qt
    bill['VAT'] = vat
    bill['Price'] = price
    bill['Total'] = total
    bill['Ins_Amt'] = ins_Amt
    bill['VAT_I'] = vat_i
    bill['Pat_Amt'] = pat_amt
    bill['VAT_P'] = vatp
    bills = pd.DataFrame(bill)
    Bills = []
    for i in range(len(bills)):
        Bills.append([{'CPT Code':bills.iloc[i,0],
                                    'Description':bills.iloc[i,1],
                                    'Qty':bills.iloc[i,2],
                                    'VAT':bills.iloc[i,3],
                                    'Price':bills.iloc[i,4],
                                    'Total':bills.iloc[i,5],
                                    'Ins_Amt':bills.iloc[i,6],
                                    'VAT_I':bills.iloc[i,7],
                                    'Pat_Amt':bills.iloc[i,8],
                                    'VAT_P':bills.iloc[i,9]}]
                    )
    return Bills

def create_json(path = "24158_00009.pdf"):
    # path = "24158_00009.pdf"
    textls = read_pdf(path) 
    cprno = find_CPR(textls)
    name = textls[0]
    address0 = textls[1]
    Patient, Insurance, age, scheme, dctr,brch,vsit,address = info(textls)
    Bills = create_bill(textls)
    sample = { 
        "Data": [
        {"Name": name},
        {"Address": address0},
        {"Patient Name": Patient},
        {"CPR No.": cprno},
        {"Insurance": Insurance},
        {"Age": age},
        {"Scheme": scheme},
        {"Doctor": dctr},
        {"Branch": brch},
        {"Visit": vsit},
        {"PIC Add": address},
        {"Billing": Bills}
        ]
    }
    return sample

# a = create_json()
# print(a)
# with open('24158_00009_pdf_json.json', 'w') as fp:
#     json.dump(sample, fp,indent=4)