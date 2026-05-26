# =============================================================
# Script: analisis_ventas.py
# Descripción: Análisis estadístico de ventas diarias 2024
#              basado en el dataset sales_sample_2024.csv
# Fuente del dataset: gist.github.com/khanusama20 (dominio público)
# Autor: Maira Aguirre Gusman - Rol P2 (Paco)
# Issue Jira: SCRUM-10
# =============================================================

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- CARGA DE DATOS ---
# Se usa ruta relativa para garantizar reproducibilidad en cualquier entorno
ruta_datos = "datos/sales_sample_2024.csv"
df = pd.read_csv(ruta_datos)

# Convertir la columna de fecha a tipo datetime para operar con períodos
df["sales_date"] = pd.to_datetime(df["sales_date"])

# --- INDICADOR 1: VENTA TOTAL DEL PERÍODO ---
# Suma acumulada de todos los montos diarios del año
venta_total    = df["sales_amount"].sum()
venta_promedio = df["sales_amount"].mean()
venta_maxima   = df["sales_amount"].max()
venta_minima   = df["sales_amount"].min()
dia_max = df.loc[df["sales_amount"].idxmax(), "sales_date"].date()
dia_min = df.loc[df["sales_amount"].idxmin(), "sales_date"].date()

print(f"Venta total: $ {venta_total:,.2f}")
print(f"Promedio diario: $ {venta_promedio:,.2f}")
print(f"Máxima: $ {venta_maxima:,.2f} ({dia_max})")
print(f"Mínima: $ {venta_minima:,.2f} ({dia_min})")

# --- INDICADOR 2: VENTAS POR MES ---
# dt.to_period("M") garantiza orden cronológico automático
nombres_meses = {
    1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril",
    5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto",
    9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"
}
df["mes"] = df["sales_date"].dt.to_period("M")
ventas_por_mes = df.groupby("mes")["sales_amount"].sum()
etiquetas = [nombres_meses[p.month] for p in ventas_por_mes.index]
valores   = ventas_por_mes.values

mes_mayor = ventas_por_mes.idxmax()
mes_menor = ventas_por_mes.idxmin()
print(f"Mes mayor facturación: {nombres_meses[mes_mayor.month]} ($ {ventas_por_mes.max():,.2f})")
print(f"Mes menor facturación: {nombres_meses[mes_menor.month]} ($ {ventas_por_mes.min():,.2f})")

# --- GRÁFICO: EVOLUCIÓN MENSUAL DE VENTAS ---
# Gráfico de barras con valor etiquetado sobre cada barra
fig, ax = plt.subplots(figsize=(12, 6))
colores = ["#1a3a5c","#1e4d7b","#215f97","#2771b3","#3a85c8",
           "#5099d4","#68adde","#82bee6","#9dceed","#b5dbf3","#cce6f7","#e0f1fb"]
bars = ax.bar(etiquetas, valores, color=colores, edgecolor="white", linewidth=0.8, width=0.7)
for bar, val in zip(bars, valores):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+800,
            f"${val:,.0f}", ha="center", va="bottom", fontsize=8.5,
            fontweight="bold", color="#1a3a5c")
ax.set_title("Evolución Mensual de Ventas - Año 2024", fontsize=14, fontweight="bold")
ax.set_xlabel("Mes", fontsize=11)
ax.set_ylabel("Total Ventas ($)", fontsize=11)
ax.set_ylim(0, ventas_por_mes.max()*1.18)
ax.tick_params(axis="x", rotation=30)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f"${x:,.0f}"))
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("resultados/ventas_por_mes.png", dpi=150, bbox_inches="tight")

# --- EXPORTAR RESUMEN MENSUAL ---
# Permite consultar los indicadores sin ejecutar el script completo
resumen = pd.DataFrame({
    "mes": etiquetas, "total_ventas": valores,
    "promedio_diario": [df[df["mes"]==p]["sales_amount"].mean() for p in ventas_por_mes.index]
}).round(2)
resumen.to_csv("resultados/resumen_mensual.csv", index=False)
print("Análisis completado.")
