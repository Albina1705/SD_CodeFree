import os
import matplotlib.pyplot as plt
import pandas as pd


# 1. DEFINIREA FUNCȚIEI
def generate_chart(data, output_path):
    # Crează folderul 'output' dacă nu există
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(12, 6))

    # Identificăm automat coloanele pentru a evita alte erori
    col_data = data.columns[0]  # Prima coloană (de obicei Data)
    col_valoare = data.columns[1]  # A doua coloană (de obicei Glicemia)

    # Desenare grafic
    plt.plot(
        data[col_data],
        data[col_valoare],
        marker="o",
        linestyle="-",
        color="#2c3e50",
    )

    plt.title(f"Evoluție Glicemie (Sursa: {col_valoare})", fontsize=14, bold=True)
    plt.xlabel(col_data, fontsize=12)
    plt.ylabel("Valoare (mg/dL sau mmol/L)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Salvare
    plt.savefig(output_path)
    plt.close()
    print(f" Graficul a fost salvat cu succes în: {output_path}")


# 2. ÎNCĂRCAREA ȘI FILTRAREA DATELOR (Folosim export.csv)
try:
    # Încărcăm fișierul tău
    df = pd.read_csv("export.csv")

    # Opțional: Aici poți filtra datele dacă vrei (ex: ultimele 30 de înregistrări)
    filtered = df.tail(30)

    # 3. APELUL FUNCȚIEI
    generate_chart(filtered, "output/glucose_chart.png")

except FileNotFoundError:
    print(
        " Eroare: Fișierul 'export.csv' nu a fost găsit! Pune-l în același folder cu chart.py."
    )
except Exception as e:
    print(f" A apărut o eroare la citirea fișierului: {e}")
