# OE - TP2 - Análisis de Ventas

## Descripción

Trabajo Práctico N.º 2 de la materia Organización Empresarial
(Tecnicatura Universitaria en Programación – UTN).

Implementa un análisis estadístico de ventas diarias utilizando Python,
con gestión de versiones en Git/GitHub y planificación en Jira.

## Integrante

| Nombre | Roles simulados |
|---|---|
| Maira Aguirre Gusman | P1 – Líder y Organizador / P2 – Desarrollador Técnico / P3 – Revisor y QA |

## Escenario

**Escenario B – Análisis de Ventas de una Pequeña Empresa**

## Dataset

**Nombre:** sales_sample_2024.csv  
**Fuente:** https://gist.github.com/khanusama20/ee33c2869dd5cf3cebdf020be1ca43f6  
**Licencia:** Dominio público (GitHub Gist)  
**Registros:** 366 registros de ventas diarias – año completo 2024  
**Columnas:** id, sales_date, sales_amount

## Estructura del repositorio

```
OE-tp2-analisis-ventas/
├── datos/
│   └── sales_sample_2024.csv
├── scripts/
│   └── analisis_ventas.py
├── resultados/
│   ├── ventas_por_mes.png
│   └── resumen_mensual.csv
├── README.md
└── .gitignore
```

## Ejecución en Google Colab

```bash
git clone https://github.com/mairaguirre/OE-tp2-analisis-ventas.git
cd OE-tp2-analisis-ventas
python scripts/analisis_ventas.py
```

Los resultados se generan automáticamente en /resultados.

## Herramientas

- Python 3 · pandas · matplotlib
- Git y GitHub para control de versiones
- Google Colab como entorno de desarrollo y bitácora
- Jira para gestión de tareas y trazabilidad

## Trazabilidad Jira

| Issue | Descripción | Rol |
|---|---|---|
| SCRUM-8 | Crear estructura de carpetas y clonar en Colab | P1 – SM |
| SCRUM-10 | Desarrollar y ejecutar el script de análisis | P2 – DEV |
| SCRUM-13 | Mejorar documentación interna y configurar .gitignore | P3 – REVISOR/QA |

## Indicadores generados

- Venta total del período anual: $ 1,812,114.00
- Venta diaria promedio: $ 4,951.13
- Venta diaria máxima: $ 8,960.00 (2024-03-20)
- Venta diaria mínima: $ 1,003.00 (2024-04-21)
- Mes de mayor facturación: Septiembre ($ 173,024.00)
- Mes de menor facturación: Octubre ($ 127,380.00)
