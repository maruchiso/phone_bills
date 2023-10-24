import pandas as pd
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import os

def do_a_flip(path):
    calls = pd.read_csv(path, encoding='ANSI', sep=';')

    calls['Netto'] = calls['Netto'].str.replace(' zł', '').str.replace(',', '.').astype(float)

    calls = calls[calls['Netto'] > 0]
    calls = calls[calls['Nr telefonu'].notna() & ~calls['Nr telefonu'].empty]
    calls['Nr telefonu'] = calls['Nr telefonu'].astype(int)
    calls['Nr telefonu'] = calls['Nr telefonu'].astype(str)


    calls = calls[['Opis połączenia','Data','Numer docelowy','Kraj','Netto','Nr telefonu']]

    #calls.to_csv('output.csv', index=False, encoding='ANSI')

    #numbers = pd.read_excel('numery tel..xlsx')
    numbers = pd.read_csv('numery_tel.csv', encoding='ANSI', sep=';')

    
    numbers['Nr telefonu'] = numbers['Nr telefonu'].astype(str)
    numbers['Nr telefonu'] = numbers['Nr telefonu'].str.replace('.0', '').str.replace('48', '', 1)
    numbers = numbers.dropna()
    #numbers.to_csv('output1.csv', index=False, encoding='ANSI')

    #merge dataframes by 'Nr telefonu'

    merge_data = calls.merge(numbers, on='Nr telefonu', how='left')
    merge_data = merge_data[merge_data['Netto'] > 0]
    merge_data = merge_data.sort_values(by='Nazwisko')

    rozliczenia_suma = merge_data[['Imię', 'Nazwisko', 'Opis połączenia', 'Netto']]
    result = rozliczenia_suma.groupby(['Imię', 'Nazwisko', 'Opis połączenia'])['Netto'].sum().reset_index()
    
    #merge_data.to_csv('finale.csv', index=False, encoding='ANSI')
    #desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    desktop_path = 'C:/Users/ITPoland/OneDrive - Neuraxpharm/Pulpit/Rozliczenia+'
    output_path1 = os.path.join(desktop_path, 'rozliczenia_plus.csv')
    output_path2 = os.path.join(desktop_path, 'suma_rozliczenia_plus.csv')
    result.to_csv(output_path2, index=False, encoding='ANSI', sep=',')
    merge_data.to_csv(output_path1, index=False, encoding='ANSI', sep=',')
    return output_path1, output_path2


def on_drop(event):
    data = event.data
    if data:
        path = data.strip('{}')
        print(path)
    else:
        print('NIEEEEEEE')
    result_label.config(text="Przetwarzanie danych")
    fin_path1, fin_path2 = do_a_flip(path)
    result_label.config(text=f'"rozliczenia_plus.csv" zapisany na pulpicie: {fin_path1}\n "suma_rozliczenia_plus.csv" zapisany na pulpicie: {fin_path2}\n ')

#GUI

root = TkinterDnD.Tk()
root.title('Rozliczenia+')
root.geometry('400x300')
frame = tk.Frame(root)
frame.pack(padx=20, pady=100)

label = tk.Label(frame, text="Przeciągnij plik CSV")
label.pack()

result_label = tk.Label(frame, text='')
result_label.pack()

frame.drop_target_register(DND_FILES)
frame.dnd_bind('<<Drop>>', on_drop)

root.mainloop()