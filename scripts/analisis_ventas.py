# =============================================================
# Script: analisis_ventas.py
# Descripción: Análisis estadístico de ventas diarias 2024
#              basado en el dataset sales_sample_2024.csv
# Fuente del dataset: gist.github.com/khanusama20 (dominio público)
# Autor: Maira Aguirre Gusman - Rol P2 (Paco)
# Revisión: Maira Aguirre Gusman - Rol P3 (Luis)
# Issue Jira: SCRUM-10 / SCRUM-13
# =============================================================

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Se usa backend no interactivo para permitir guardar
                       # figuras sin necesidad de un entorno gráfico (Colab/servidor)
import matplotlib.pyplot as plt

# --- CARGA DE DATOS ---
# Se usa ruta relativa (no absoluta) para garantizar que el script funcione
# en cualquier entorno que respete la estructura de carpetas del repositorio
ruta_datos = 'datos/sales_sample_2024.csv'
df = pd.read_csv(ruta_datos)

# Se convierte la columna de fecha a tipo datetime porque el dataset la almacena
# como string. Sin esta conversión no es posible extraer el mes ni operar con fechas
df['sales_date'] = pd.to_datetime(df['sales_date'])

# --- INDICADOR 1: ESTADÍSTICAS GENERALES DEL PERÍODO ---
# Se calculan los indicadores básicos sobre el monto diario de ventas.
# idxmax() e idxmin() devuelven el índice de la fila con el valor más alto/bajo,
# lo que permite recuperar la fecha exacta del mejor y peor día de ventas
venta_total    = df['sales_amount'].sum()
venta_promedio = df['sales_amount'].mean()
venta_maxima   = df['sales_amount'].max()
venta_minima   = df['sales_amount'].min()
dia_max = df.loc[df['sales_amount'].idxmax(), 'sales_date'].date()
dia_min = df.loc[df['sales_amount'].idxmin(), 'sales_date'].date()

print(f'Venta total: $ {venta_total:,.2f}')
print(f'Promedio diario: $ {venta_promedio:,.2f}')
print(f'Máxima: $ {venta_maxima:,.2f} ({dia_max})')
print(f'Mínima: $ {venta_minima:,.2f} ({dia_min})')

# --- INDICADOR 2: VENTAS AGRUPADAS POR MES ---
# Se usa dt.to_period('M') en lugar de dt.month porque Period garantiza
# el orden cronológico correcto al agrupar. dt.month devuelve solo el número
# del mes (1-12) sin considerar el año, lo que podría causar errores
# si el dataset abarcara más de un año
nombres_meses = {
    1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril',
    5:'Mayo', 6:'Junio', 7:'Julio', 8:'Agosto',
    9:'Septiembre', 10:'Octubre', 11:'Noviembre', 12:'Diciembre'
}
df['mes'] = df['sales_date'].dt.to_period('M')
ventas_por_mes = df.groupby('mes')['sales_amount'].sum()
etiquetas = [nombres_meses[p.month] for p in ventas_por_mes.index]
valores   = ventas_por_mes.values

# idxmax() e idxmin() sobre la serie agrupada identifican directamente
# el período de mejor y peor desempeño comercial
mes_mayor = ventas_por_mes.idxmax()
mes_menor = ventas_por_mes.idxmin()
print(f'Mes mayor facturación: {nombres_meses[mes_mayor.month]} ($ {ventas_por_mes.max():,.2f})')
print(f'Mes menor facturación: {nombres_meses[mes_menor.month]} ($ {ventas_por_mes.min():,.2f})')

# --- GRÁFICO: EVOLUCIÓN MENSUAL DE VENTAS ---
# Se elige un gráfico de barras porque permite comparar valores discretos
# por período de forma clara. Se usa una paleta de azules degradados
# para representar visualmente la progresión temporal de enero a diciembre
fig, ax = plt.subplots(figsize=(12, 6))
colores = ['#1a3a5c','#1e4d7b','#215f97','#2771b3','#3a85c8',
           '#5099d4','#68adde','#82bee6','#9dceed','#b5dbf3','#cce6f7','#e0f1fb']
bars = ax.bar(etiquetas, valores, color=colores, edgecolor='white', linewidth=0.8, width=0.7)

# Se etiqueta cada barra con su valor para facilitar la lectura sin
# necesidad de consultar el eje Y. El offset de 800 evita superposición
# con el borde superior de la barra
for bar, val in zip(bars, valores):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+800,
            f'${val:,.0f}', ha='center', va='bottom', fontsize=8.5,
            fontweight='bold', color='#1a3a5c')

ax.set_title('Evolución Mensual de Ventas - Año 2024', fontsize=14, fontweight='bold')
ax.set_xlabel('Mes', fontsize=11)
ax.set_ylabel('Total Ventas ($)', fontsize=11)
# El límite superior se define como 1.18 veces el máximo para dejar
# espacio visual sobre las etiquetas de valor
ax.set_ylim(0, ventas_por_mes.max()*1.18)
ax.tick_params(axis='x', rotation=30)
# FuncFormatter permite mostrar los valores del eje Y con formato de moneda
# en lugar del formato científico o numérico por defecto de matplotlib
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f'${x:,.0f}'))
ax.grid(axis='y', linestyle='--', alpha=0.4)
# Se eliminan los bordes superior y derecho para una presentación más limpia
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('resultados/ventas_por_mes.png', dpi=150, bbox_inches='tight')

# --- EXPORTAR RESUMEN MENSUAL A CSV ---
# Se exporta un resumen con total y promedio diario por mes.
# Esto permite consultar los indicadores principales sin necesidad
# de volver a ejecutar el script completo
resumen = pd.DataFrame({
    'mes': etiquetas, 'total_ventas': valores,
    'promedio_diario': [df[df['mes']==p]['sales_amount'].mean() for p in ventas_por_mes.index]
}).round(2)
resumen.to_csv('resultados/resumen_mensual.csv', index=False)
print('Análisis completado.')
