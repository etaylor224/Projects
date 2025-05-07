import datetime

import pandas as pd
import tabula
from tkinter import filedialog


def read_pdf_to_df(multi_table : bool = False):

    pdf_path = filedialog.askopenfilename()
    pdf_read = tabula.read_pdf(pdf_path, pages="all", multiple_tables=multi_table)
    return pd.DataFrame(pdf_read[0])

def imas_pdf_to_excel():
    
    ring_df = read_pdf_to_df()
    sorted_by_rdt = ring_df.sort_values(by=["Ring", "Day", "Time"])
    sorted_by_rdt.to_excel('sorted_rings.xlsx', index=False)
    return

def first_pdf_to_excel():
    df = read_pdf_to_df()
    sort_df = df.sort_values(by=["Division", "Ring", "Time"])
    today = datetime.date.today()
    sort_df.to_excel(f"sorted_rings_{today}.xlsx", index=False)

first_pdf_to_excel()
