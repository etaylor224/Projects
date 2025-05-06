import pandas as pd
import tabula


def imas_pdf_to_excel():
    pdf_path = r"C:\Users\bassj\Downloads\nola_rings.pdf"

    dfs = tabula.read_pdf(pdf_path, pages='all', multiple_tables=False)
    ring_df = pd.DataFrame(dfs[0])
    sorted_by_rdt = ring_df.sort_values(by=["Ring", "Day", "Time"])
    sorted_by_rdt.to_excel('sorted_rings.xlsx', index=False)
    return


imas_pdf_to_excel()
