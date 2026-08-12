# AdventureWorks Sales Analytics Platform

**SQL · Power BI · Python · Databricks · PySpark · AWS S3 · Apache Airflow**

## Descripción del Proyecto

**Adventure Works Cycles** es la empresa ficticia fabricante y comercializadora de bicicletas representada en el dataset AdventureWorks de Microsoft.

La compañía vende **bicicletas, componentes, ropa y accesorios** en múltiples territorios geográficos a través de una red de clientes y representantes de ventas.

### Problema de Negocio

Adventure Works contaba con información operativa detallada sobre **órdenes de venta, clientes, productos, vendedores y territorios**, pero estos datos se encontraban distribuidos entre múltiples tablas.

Esto dificultaba que la gerencia pudiera responder preguntas comerciales fundamentales:

- ¿Qué está impulsando los ingresos?
- ¿En qué períodos son más fuertes las ventas?
- ¿Qué productos generan mayor valor?
- ¿Quiénes son los clientes más valiosos de la empresa?
- ¿Qué clientes están en riesgo de volverse inactivos?
- ¿Qué territorios presentan el mejor desempeño?
- ¿Qué vendedores superan los resultados promedio de sus territorios?

### Solución

Construí una **plataforma de analítica end-to-end** que transforma los datos operativos en bruto en un Star Schema preparado para análisis, aplica análisis SQL orientado al negocio y presenta los resultados mediante seis dashboards en Power BI.

---

# Principales Hallazgos de Negocio

El análisis reveló varios patrones importantes en el desempeño comercial de Adventure Works:

- **La primavera fue la temporada con mayores ventas**, generando **$29.52M (26.87%)**, mientras que el invierno fue la más débil con **$25.22M (22.96%)**.
- **Las bicicletas generaron aproximadamente el 87.7% de los ingresos por categoría de producto**, convirtiéndose en el principal motor de ingresos de la compañía.
- **Southwest fue el territorio con mejor desempeño**, generando aproximadamente **$24M en ingresos**.
- **Linda C. Mitchell fue la vendedora con mayores ingresos**, generando aproximadamente **$10.3M**.
- **Potential Customers y Loyal Customers fueron los segmentos RFM más grandes**, mientras que At Risk y Lost Customers representan oportunidades claras de retención.
- La mayoría de los clientes fueron clasificados con **riesgo de abandono Bajo o Medio**, mientras que el grupo de Alto Riesgo fue considerablemente menor.
- Las ventas fueron más fuertes los **domingos y martes**, mientras que los jueves presentaron el menor volumen de ventas entre los días analizados.

---

# Recomendaciones de Negocio

A partir de estos hallazgos, Adventure Works debería:

- **Proteger y fortalecer el negocio principal de bicicletas**, ya que representa la gran mayoría de los ingresos.
- **Utilizar accesorios y ropa para aumentar el valor promedio de compra** mediante estrategias de venta cruzada y paquetes de productos.
- **Priorizar Southwest y otros territorios de alto crecimiento**, mientras se investigan las regiones con menor desempeño para identificar oportunidades de expansión.
- **Replicar las prácticas de los vendedores con mejor desempeño**, comparando sus resultados con los benchmarks de sus territorios.
- **Dirigir campañas de retención a los clientes At Risk y Lost Customers**, mientras se desarrollan estrategias de recompra para Potential Customers.
- **Alinear promociones e inventario con las temporadas y días de mayor demanda**.

---

# Arquitectura

```text
AdventureWorks Data
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
  Análisis SQL
        ↓
     Power BI
        ↓
Insights de Negocio
