import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ClimaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Previsão de Produtividade Agrícola")
        self.geometry("700x700")

        self.inputs = {}
        self.resultado_valor = 0

        variaveis = ['chuva', 'tempmin', 'tempmed', 'tempmax', 'umidrel', 'insolacao', 'evaporacao']

        frame = ttk.Frame(self)
        frame.pack(padx=20, pady=20, fill='x')

        ttk.Label(frame, text="Informe a média das variáveis climáticas de Setembro a Dezembro",
                  font=("Arial", 12)).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        for i, var in enumerate(variaveis):
            ttk.Label(frame, text=var.capitalize() + " média:").grid(row=i+1, column=0, sticky='e', pady=5)
            entry = ttk.Entry(frame, width=20)
            entry.grid(row=i+1, column=1, padx=10)
            self.inputs[var] = entry

        self.btn_calcular = ttk.Button(self, text="Calcular previsão", command=self.calcular)
        self.btn_calcular.pack(pady=20)

        self.resultado = ttk.Label(self, text="", font=("Arial", 12))
        self.resultado.pack(pady=10)

        self.grafico_frame = ttk.Frame(self)
        self.grafico_frame.pack(fill='both', expand=True)

    def calcular(self):
        dados = []
        for var in ['chuva', 'tempmin', 'tempmed', 'tempmax', 'umidrel', 'insolacao', 'evaporacao']:
            valor = self.inputs[var].get()
            if not valor:
                messagebox.showerror("Erro de validação", f"O campo '{var}' está vazio.")
                return
            try:
                valor_float = float(valor)
                if valor_float < 0:
                    messagebox.showerror("Erro de validação", f"O valor de '{var}' não pode ser negativo.")
                    return
                dados.append(valor_float)
            except ValueError:
                messagebox.showerror("Erro de validação", f"O valor de '{var}' deve ser numérico.")
                return

        try:
            modelo = joblib.load('modelo_produtividade.pkl')
            previsao = modelo.predict([dados])[0]
            self.resultado_valor = previsao
            self.resultado.config(text=f"Produtividade estimada: {previsao:.2f} kg/ha", foreground="green")
            self.plotar_grafico(previsao)
        except Exception as e:
            self.resultado.config(text=f"Erro ao calcular: {e}", foreground="red")

    def plotar_grafico(self, previsao):
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 3))
        categorias = ['Produtividade Prevista']
        valores = [previsao]

        ax.bar(categorias, valores, color='green')
        ax.set_ylabel('kg/ha')
        ax.set_title('Resultado da Previsão')

        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

if __name__ == '__main__':
    app = ClimaApp()
    app.mainloop()
