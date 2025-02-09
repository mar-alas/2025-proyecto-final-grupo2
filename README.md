# 2025-proyecto-final-grupo2

## Integrantes del equipo

* Maria del Mar Alas Escalante
* Jhon Puentes
* Robert Castro
* Daniel Gamez

## Índice

1. [Integrantes del equipo](#integrantes-del-equipo)
2. [Documento Visión de Arquitectura](#documento-visión-de-arquitectura)
3. [Hoja de trabajo arquitectura](#hoja-de-trabajo-arquitectura)
   - [Objetivos](#objetivos)
   - [Restricciones de negocio](#restricciones-de-negocio)
   - [Restricciones de tecnología](#restricciones-de-tecnología)
4. [EDT](#edt)
   - [EDT Formato Árbol](#edt-formato-árbol)
   - [EDT Formato Lista](#edt-formato-lista)
5. [Diagramas](#diagramas)
   - [Diagrama de Contexto](#diagrama-de-contexto)
   - [Diagrama de Dominio](#diagrama-de-dominio)
   - [Diagrama de Contenedores](#diagrama-de-contenedores)
   - [Diagrama de Componentes](#diagrama-de-componentes)
   - [Diagrama de Despliegue](#diagrama-de-despliegue)
6. [Estrategia de Pruebas](#estrategia-de-pruebas)
7. [Definición de Frameworks](#definición-de-frameworks)
8. [Priorización](#priorización)
9. [Estimación de velocidad y capacidad](#estimación-de-velocidad-y-capacidad)


## Documento Visión de Arquitectura
[Visión de Arquitectura Doc.pdf](https://github.com/user-attachments/files/18634986/Vision.de.Arquitectura.Doc.pdf)

## Hoja de trabajo arquitectura

### Objetivos

| Descripción del Objetivo                                                             | Tiempo de cumplimiento | Mejora esperada al negocio                                       |
|---------------------------------------------------------------------------------------|------------------------|-------------------------------------------------------------------|
| Aumentar la posición en el mercado ofreciendo el mejor servicio de venta y distribución de productos a los clientes | 4 años                 | Crecer 3% anual                                                    |
| Entregar los pedidos solicitados con el menor número de inconformidades posible       | 2 años                 | Reducirlo en 10%                                                   |
| Reducir las pérdidas por perecederos vencidos                                           | 1 año                  | Reducirlo en 60%                                                   |

### Restricciones de negocio

| **#Restriccion de Negocio** | 1 |
|--------------------------------|-----------------------------------------------------------|
| **Descripción de la restricción** | La arquitectura debe estar lista en 8 semanas |
| **Usuario que expresa esta restricción** | Patrocinador del Proyecto – Presidente CCP |
| **Justificación para esta restricción** | El recaudo del dinero de capital de riesgo depende de que todo el proyecto termine en 16 semanas y para ello la arquitectura se debe plantear de forma rápida sin comprometer su calidad. |
| **Cómo considera que pueda afectar la arquitectura del sistema esta restricción** | Enfocarse en los requerimientos de alta prioridad primero dejando decisiones de diseño menos importantes para otras etapas.|

| **#Restriccion de Negocio** | 2 |
|--------------------------------|-----------------------------------------------------------|
| **Descripción de la restricción** | La arquitectura debe realizarse por un equipo de 4 personas |
| **Usuario que expresa esta restricción** | Patrocinador del Proyecto – presidente CCP.  |
| **Justificación para esta restricción** | Es el presupuesto en horas hombre que el presidente/patrocinador considera apropiados para proyectos de este tipo.|
| **Cómo considera que pueda afectar la arquitectura del sistema esta restricción** | Se prioriza las funcionalidades más importantes para los stakeholders cumpliendo con los objetivos primordiales de los mismos. La arquitectura va a ser producto de la experiencia y horas de trabajo de estas 4 personas.|

### Restricciones de tecnología

| **#Restriccion de Tecnología** | 1 |
|--------------------------------|-----------------------------------------------------------|
| **Descripción de la restricción** | La aplicación debe tener una interfaz Web para las funcionalidades del área de compras, área logística y algunas funciones relacionadas con el análisis del desempeño comercial. |
| **Usuario que expresa esta restricción** | Gerente de tecnología.  |
| **Justificación para esta restricción** | El proyecto necesita tener disponibles ciertas funcionalidades por interfaz web según el tipo de usuario que va a hacer uso de estas. Esto con base a estudios y análisis realizados a los procesos de las áreas administrativas que laboran en computadores principalmente.|
| **Cómo considera que pueda afectar la arquitectura del sistema esta restricción** | La arquitectura tendrá que tener en cuenta los retos y ventajas de las interfaces web versus otro tipo de interfaces como las de escritorio.|

| **#Restriccion de Tecnología** | 2 |
|--------------------------------|-----------------------------------------------------------|
| **Descripción de la restricción** | La aplicación debe tener una interfaz Móvil para funcionalidades especificas. |
| **Usuario que expresa esta restricción** | Gerente de tecnología.  |
| **Justificación para esta restricción** | El proyecto necesita una interfaz Móvil para los usuarios que no tienen acceso a computadores. Esto son los vendedores y clientes. |
| **Cómo considera que pueda afectar la arquitectura del sistema esta restricción** | La programación en móvil tiene retos y ventajas adicionales a la programación web. Seguramente en  la arquitectura se tendrán que ver tácticas tipo caché u otro tipo para poder cumplir con requisitos funcionales y no funcionales.|

| **#Restriccion de Tecnología** | 3 |
|--------------------------------|-----------------------------------------------------------|
| **Descripción de la restricción** | El lenguaje de programación para el backend debe ser Python. |
| **Usuario que expresa esta restricción** | Gerente de tecnología.  |
| **Justificación para esta restricción** | Es el lenguaje de mayor experiencia en el equipo de trabajo y el que la compañía ha definido como estándar para todos sus proyectos. |
| **Cómo considera que pueda afectar la arquitectura del sistema esta restricción** | Puede haber impacto en el desempeño del sistema dado que Python es mas lento que otros lenguajes y por ello sea necesario implementar tácticas de arquitectura adicionales a si se usará C++ por ejemplo. |

| **#Restriccion de Tecnología** | 4 |
|--------------------------------|-----------------------------------------------------------|
| **Descripción de la restricción** | El framework de programación para el frontend web debe ser Angular |
| **Usuario que expresa esta restricción** | Gerente de tecnología.  |
| **Justificación para esta restricción** | Es el framework de mayor experiencia en el equipo de trabajo y el que la compañía ha definido como estándar para todos sus proyectos web. |
| **Cómo considera que pueda afectar la arquitectura del sistema esta restricción** | Por el momento no se ve mayor impacto por la escogencia de este framework. |

| **#Restriccion de Tecnología** | 5 |
|--------------------------------|-----------------------------------------------------------|
| **Descripción de la restricción** | El framework de programación para el frontend móvil debe ser Android con Kotlin y Jetpack Compose |
| **Usuario que expresa esta restricción** | Gerente de tecnología.  |
| **Justificación para esta restricción** | Es el framework de mayor experiencia en el equipo de trabajo y el que la compañía ha definido como estándar para todos sus proyectos móviles. |
| **Cómo considera que pueda afectar la arquitectura del sistema esta restricción** | Por el momento no se ve mayor impacto por la escogencia de este framework. |






## EDT

### EDT Formato Árbol

[EDTFormatoArbol.pdf](https://github.com/user-attachments/files/18634956/EDTFormatoArbol.pdf)

### EDT Formato Lista

[EDT.docx](https://github.com/user-attachments/files/18634958/EDT.docx)


## Diagramas

### Diagrama de Contexto 


![Diagramas de Contexto, Domino, Componentes-Contexto drawio](https://github.com/user-attachments/assets/0c5fdee1-28c6-4a4b-aa13-432eb2d6896f)

### Diagrama de Dominio
![Diagramas de Contexto, Domino, Componentes-Dominio drawio](https://github.com/user-attachments/assets/9b5b49ea-89e8-48cb-a53f-9ed32003ae52)

### Diagrama de Contenedores 

![Diagramas de Contexto, Domino, Componentes-Contenedores drawio](https://github.com/user-attachments/assets/110ebf96-ead2-4b26-a173-8683846450b7)

### Diagrama de Componentes

![Diagramas de Contexto, Domino, Componentes-Componentes drawio](https://github.com/user-attachments/assets/2e202896-f9e7-4da6-bcde-41c95d3a9189)

### Diagrama de Despliegue

![Diagramas de Contexto, Domino, Componentes-Despliegue drawio](https://github.com/user-attachments/assets/85d69c4e-9765-4011-bb4d-84287fac0dd2)

## Estrategia de Pruebas
[Estrategia de Pruebas.pdf](https://uniandes-my.sharepoint.com/:b:/g/personal/da_gamez96_uniandes_edu_co/EbZzM6CqlmdKlgiMTvM5HXEBPkdHDj0VyJ9hKycMoFG3bA?e=wnXi3x)

## Definición de Frameworks

### Frameworks Componente web

* Desarrollo: Angular
* Unit testing: TestBed
* Integración: Jasmine 
* E2E: Cypress
### Frameworks Componente móvil

* Desarrollo: Jetpack Compose + Kotlin
* Unit testing: JUnit
* Integracion: Espresso
* E2E: Espresso

### Backend
* Desarrollo API: Flask en Python
* Ambiente cloud para backend: GCP
* Unit testing: Pytest

### Herramientas de Testing Adicionales

* JMeter
* Postman
  
## Priorización
[Árbol de utilidad.pdf](https://uniandes-my.sharepoint.com/:b:/g/personal/da_gamez96_uniandes_edu_co/EaNzMLwzX2VOgVnjvLuYFEQBY59vx4ts_YTxHu1Z7O2ANA?e=ZqKNek)

## Estimación de velocidad y capacidad
[Estimación Puntos Historia de Usuario.xslx](https://uniandes-my.sharepoint.com/:x:/g/personal/da_gamez96_uniandes_edu_co/EckiTsWHsd5HrplPOmdfgSsBVXJc38TcgI-3KxOAL5CEhg?e=8GutRG)

[Calculo de Velocidad Proyecto Final 1.xslx](https://uniandes-my.sharepoint.com/:x:/g/personal/da_gamez96_uniandes_edu_co/EajH4Cir-kZCnJ2ok08Wy_AB3Nhi3XJ2-qicAe75BXELug?e=nLXxUB)






