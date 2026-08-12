# Plataforma de Analítica de Ventas AdventureWorks

**SQL · Power BI · Python · Databricks · PySpark · AWS S3 · Apache Airflow**

## Descripción General del Proyecto

**Adventure Works Cycles** es el fabricante y minorista ficticio de bicicletas representado en el conjunto de datos AdventureWorks de Microsoft.

La empresa vende **bicicletas, componentes, ropa y accesorios** en múltiples territorios geográficos a través de una red de clientes y representantes de ventas.

### Problema de Negocio

Adventure Works contaba con datos operativos detallados sobre **órdenes de venta, clientes, productos, vendedores y territorios**, pero esta información estaba distribuida entre múltiples tablas.

Esto dificultaba que la gerencia pudiera responder preguntas comerciales fundamentales:

- ¿Qué está impulsando los ingresos?
- ¿Cuándo son más fuertes las ventas?
- ¿Qué productos generan mayor valor?
- ¿Quiénes son los clientes más valiosos de la empresa?
- ¿Qué clientes están en riesgo de volverse inactivos?
- ¿Qué territorios tienen el mejor desempeño?
- ¿Qué vendedores superan los benchmarks de sus regiones?

### Solución

Construí una **plataforma de analítica end-to-end** que transforma los datos operativos en bruto en un Star Schema preparado para análisis, aplica análisis SQL enfocado en el negocio y presenta los resultados mediante seis dashboards de Power BI.

---

# Principales Hallazgos de Negocio

El análisis reveló varios patrones claros en el desempeño comercial de Adventure Works:

- **La primavera fue la temporada con mayores ventas**, generando **$29.52M (26.87%)**, mientras que el invierno fue la más débil con **$25.22M (22.96%)**.
- **Las bicicletas generaron aproximadamente el 87.7% de los ingresos por categoría de producto**, convirtiéndose por amplio margen en el principal motor de ingresos de la empresa.
- **Southwest fue el territorio con mejor desempeño**, con aproximadamente **$24M en ingresos**.
- **Linda C. Mitchell fue la vendedora con mayores ingresos**, generando aproximadamente **$10.3M**.
- **Potential Customers y Loyal Customers fueron los segmentos RFM más grandes**, mientras que At-Risk y Lost Customers representaron claras oportunidades de retención.
- La mayoría de los clientes fueron clasificados con **riesgo de churn Bajo o Medio**, con un grupo de Alto Riesgo considerablemente menor.
- Las ventas fueron más fuertes los **domingos y martes**, mientras que los jueves presentaron el menor volumen de ventas entre los días de la semana analizados.

---

# Recomendaciones de Negocio

Con base en estos hallazgos, Adventure Works debería:

- **Proteger y hacer crecer el negocio principal de bicicletas**, ya que las bicicletas representan la gran mayoría de los ingresos.
- **Utilizar accesorios y ropa para aumentar el tamaño de la cesta de compra** mediante venta cruzada y paquetes de productos.
- **Priorizar Southwest y otros territorios de alto crecimiento**, mientras se investigan las regiones más débiles en busca de oportunidades de expansión.
- **Replicar las prácticas de los vendedores con mejor desempeño**, comparando a los mejores vendedores con los benchmarks de sus territorios.
- **Dirigir campañas de retención a los clientes At-Risk y Lost Customers**, mientras se utilizan los Potential Customers para estrategias de compra recurrente.
- **Alinear las promociones y la planificación de inventario con las temporadas y días de ventas más fuertes**.

---

# Arquitectura

```text
Datos de AdventureWorks
        ↓
      AWS S3
        ↓
 Ingesta con Python
        ↓
    Databricks
Bronze → Silver → Gold
        ↓
    Star Schema
        ↓
  Analítica SQL
        ↓
     Power BI
        ↓
Insights de Negocio
```

El flujo de trabajo completo es orquestado con **Apache Airflow**.

![Diagrama de Arquitectura](docs/architecture/architecture_diagram.png)

---

# Hallazgos de Negocio Detallados

## 1. Las ventas muestran patrones estacionales y semanales claros

![Dashboard Ejecutivo de Ventas](docs/dashboards/executive_sales_dashboard.png)

### Hallazgos

- **La primavera fue la temporada con mayores ventas**, generando **$29.52M (26.87%)** de las ventas.
- El verano generó **$28.04M (25.53%)**.
- El otoño generó **$27.07M (24.64%)**.
- **El invierno fue la temporada más débil**, con **$25.22M (22.96%)**.
- **Los domingos y martes fueron los días con mayores ventas**.
- **Los jueves presentaron el menor volumen de ventas** entre los días de la semana analizados.
- El análisis mensual también reveló períodos tanto de aceleración como de disminución de las ventas.

### Implicación para el Negocio

Adventure Works puede utilizar estos patrones para alinear mejor el **inventario, las promociones, los objetivos de ventas y la actividad comercial** con períodos de demanda históricamente más fuerte o más débil.

---

## 2. Los ingresos están altamente concentrados en bicicletas

![Analítica de Productos](docs/dashboards/product_analytics.png)

### Hallazgos

- **Las bicicletas generan aproximadamente el 87.7% de los ingresos por categoría de producto.**
- **Los componentes contribuyen aproximadamente con el 9.5%.**
- La ropa y los accesorios representan únicamente una pequeña proporción de los ingresos totales por productos.
- El análisis identifica los productos con mejor desempeño por mes.
- Varias combinaciones de productos aparecen repetidamente en el análisis de **Comprados Frecuentemente Juntos**.
- El análisis de ingresos frente a ganancias identifica productos que generan ingresos sustanciales sin producir márgenes igualmente sólidos.

### Implicación para el Negocio

Las bicicletas son claramente el principal motor de ingresos de la empresa.

Al mismo tiempo, la menor contribución de los accesorios y la ropa sugiere oportunidades para aumentar la **venta cruzada y el tamaño promedio de la cesta de compra**, mientras que los productos con altos ingresos y bajos márgenes requieren un análisis adicional de precios y rentabilidad.

---

## 3. Southwest es el territorio de ventas más fuerte

![Territorio de Ventas](docs/dashboards/sales_territory.png)

### Hallazgos

- **Southwest es el territorio más grande**, generando aproximadamente **$24M en ingresos**.
- **Canada y Northwest** forman el siguiente grupo más fuerte con aproximadamente **$16M cada uno**.
- Australia les sigue con aproximadamente **$11M**.
- Alemania es el territorio con menores ingresos entre los analizados.
- Los ingresos actuales son superiores a los del año anterior en los territorios mostrados.
- El análisis interanual revela diferencias sustanciales en las trayectorias de crecimiento entre mercados.

### Implicación para el Negocio

Adventure Works no debería gestionar todos los mercados de manera idéntica.

Southwest representa un mercado crítico en términos de ingresos, mientras que los territorios de menor volumen pueden investigarse para identificar **oportunidades de crecimiento, limitaciones comerciales o diferencias en la demanda de los clientes**.

---

## 4. El desempeño de ventas se concentra entre varios representantes destacados

![Desempeño de Vendedores](docs/dashboards/salesperson_performance.png)

### Hallazgos

- **Linda C. Mitchell es la vendedora con mayores ingresos**, generando aproximadamente **$10.3M**.
- **Jae B. Pak** le sigue con aproximadamente **$8.5M**.
- **Tsvi Michael Reiter** generó aproximadamente **$7.2M**.
- **Jillian Carson** también se encuentra entre los vendedores con mejor desempeño, con aproximadamente **$6.8M**.
- Varios de los principales vendedores superan sustancialmente los promedios de sus territorios.

### Implicación para el Negocio

Comparar a los representantes con el **benchmark de su territorio** proporciona una medida de desempeño más justa que utilizar únicamente los ingresos totales.

Los representantes con mejores resultados pueden estudiarse para identificar prácticas de ventas exitosas que potencialmente puedan replicarse en toda la organización.

---

## 5. El valor de los clientes está distribuido de manera desigual

![Analítica de Clientes](docs/dashboards/customer_analytics.png)

### Hallazgos

- El cliente individual de mayor valor generó **cerca de $0.9M en ingresos durante su ciclo de vida**.
- Varios de los principales clientes generaron más de **$0.7M cada uno**.
- El análisis de Pareto muestra que la contribución de ingresos de los clientes no está distribuida de manera uniforme.
- La mayoría de los clientes se encuentran en categorías de **Riesgo Bajo o Riesgo Medio** de churn.
- El grupo de **Alto Riesgo** es considerablemente menor.
- El análisis también identifica clientes que se han vuelto inactivos y que podrían requerir estrategias de reactivación.

### Implicación para el Negocio

Adventure Works puede priorizar los esfuerzos de retención basándose tanto en el **valor del cliente como en el riesgo de churn**, en lugar de tratar a todos los clientes de la misma manera.

Los clientes de alto valor que muestran una disminución en su nivel de actividad deberían recibir especial atención.

---

## 6. La segmentación RFM crea grupos de clientes accionables

![Segmentación de Clientes](docs/dashboards/customer_segmentation.png)

Utilicé **Análisis RFM — Recencia, Frecuencia y Valor Monetario —** para segmentar a los clientes según su comportamiento de compra.

Los clientes fueron clasificados en:

- Campeones
- Clientes Leales
- Clientes Potenciales
- Clientes Nuevos
- En Riesgo
- Clientes Perdidos

### Hallazgos

- **Los Clientes Potenciales representan el segmento de clientes más grande.**
- **Los Clientes Leales constituyen otra parte importante de la base de clientes.**
- Los Campeones representan un grupo de clientes más pequeño pero estratégicamente valioso.
- Los clientes En Riesgo y Clientes Perdidos proporcionan grupos claramente identificables para esfuerzos de retención y reactivación.
- Los ingresos varían sustancialmente entre los segmentos de clientes.

### Implicación para el Negocio

Adventure Works puede utilizar diferentes estrategias para cada segmento:

**Campeones →** programas de fidelización y VIP  
**Clientes Leales →** venta cruzada y retención  
**Clientes Potenciales →** incentivar compras recurrentes  
**Clientes Nuevos →** onboarding y campañas para una segunda compra  
**En Riesgo →** campañas de retención dirigidas  
**Clientes Perdidos →** campañas de reactivación

---

# Análisis SQL

La capa analítica incluye modelos SQL para:

- Tendencias mensuales de ingresos
- Crecimiento mes a mes
- Análisis estacional de ventas
- Valor de vida del cliente
- Riesgo de churn de clientes
- Clientes inactivos
- Segmentación RFM
- Evolución de segmentos de clientes
- Contribución por categoría de producto
- Productos principales por mes
- Productos comprados frecuentemente
- Productos con altos ingresos / bajos márgenes
- Crecimiento interanual por territorio
- Desempeño de vendedores vs. territorio

### Técnicas SQL

`CTEs` · `Funciones de Ventana` · `LAG()` · `LEAD()` · `DENSE_RANK()` · `NTILE()` · `CASE` · `Self Joins` · `Subconsultas` · `Agregaciones` · `Funciones de Fecha`

---

# Modelo de Datos

La capa Gold utiliza un **Star Schema** preparado para análisis y diseñado para análisis SQL y reportes en Power BI.

![Star Schema](docs/architecture/star_schema.png)

El modelo dimensional proporciona dimensiones consistentes de clientes, productos, territorios, vendedores y fechas para el análisis de negocio.

---

# Stack Tecnológico

| Área | Tecnologías |
|---|---|
| Análisis de Datos | SQL, Power BI |
| Visualización de Datos | Power BI |
| Modelado de Datos | Star Schema, Modelado Dimensional |
| Programación | Python |
| Procesamiento de Datos | PySpark |
| Almacenamiento en la Nube | AWS S3 |
| Plataforma de Datos | Databricks |
| Almacenamiento | Delta Lake |
| Orquestación | Apache Airflow |
| Control de Versiones | Git, GitHub |

---

# Estructura del Repositorio

```text
AdventureWorks/
│
├── airflow/
│   └── dags/
│       └── adventureworks_pipeline.py
│
├── config/
│
├── data/
│   └── raw/
│
├── databricks/
│   ├── 01_bronze.py
│   ├── 02_silver.py
│   ├── 03_gold.py
│   └── 04_sql_analytics.py
│
├── docs/
│   ├── architecture/
│   └── dashboards/
│
├── ingestion/
│   ├── run_pipeline.py
│   └── scripts/
│
├── powerbi/
│   └── AdventureWorksDashboard.pbix
│
├── scripts/
├── .gitignore
├── README.md
├── README_ES.md
└── requirements.txt
```

---

# Habilidades Demostradas

### Analítica de Datos & BI

- Análisis de negocio con SQL
- Desarrollo de dashboards en Power BI
- Análisis de KPIs
- Análisis de tendencias y crecimiento
- Valor de vida del cliente
- Análisis de churn
- Segmentación RFM
- Análisis de desempeño de productos
- Análisis territorial
- Benchmarking de vendedores
- Visualización de datos y storytelling

### Ingeniería de Datos

- ETL con Python
- AWS S3
- Databricks
- PySpark
- Delta Lake
- Arquitectura Medallion
- Apache Airflow
- Modelado Star Schema

---

# Resultado del Proyecto

Los datos operativos fragmentados de Adventure Works fueron transformados en una **plataforma de analítica centralizada con seis dashboards de Power BI orientados a la toma de decisiones**.

La solución final permite analizar el desempeño comercial a través de:

**Ventas → Clientes → Segmentos → Productos → Territorios → Vendedores**

Este proyecto demuestra cómo **SQL y Power BI pueden transformar datos operativos en recomendaciones de negocio accionables**, respaldados por un pipeline de datos automatizado en la nube.
