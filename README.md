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
10. [Flujo de trabajo y estrategia de versionamiento](#flujo-de-trabajo-y-estrategia-de-versionamiento)


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
![image](https://github.com/user-attachments/assets/ff7b2ab1-b150-48b8-8dc2-21a70f126f9c)


### Diagrama de Dominio
![image](https://github.com/user-attachments/assets/e7ac8a6c-ebf1-40a1-92eb-a1f5e811ddc5)


### Diagrama de Contenedores 

![image](https://github.com/user-attachments/assets/bc61b8fa-6195-4c03-b312-3406fe083d95)


### Diagrama de Componentes
![image](https://github.com/user-attachments/assets/7c8d93d1-2c1a-4462-a055-afc04ddb252e)


### Diagrama de Despliegue
![image](https://github.com/user-attachments/assets/f780531a-c86e-44fc-a316-90c705ff3407)


### Diagrama de Concurrencia
![image](https://github.com/user-attachments/assets/ca71a92c-1950-4aa6-865f-02de1363727d)


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


⚠️ Los documentos asociados a la entrega de cada semana los puede encontrar en la carpeta /docs de este repositorio ⚠️

## Flujo de trabajo y estrategia de versionamiento

Para gestionar el desarrollo de la plataforma, utilizamos **GitHub** con el modelo de ramificación basado similar a **Git Flow**. Este flujo permite un desarrollo estructurado y organizado, asegurando estabilidad en el código base.

### Estructura de ramas
- **`main`**: Contiene las versiones estables y listas para producción. Solo se actualiza con versiones etiquetadas.
- **`feature/*`**: Ramas dedicadas a nuevas funcionalidades. Se crean desde `develop` y se fusionan nuevamente en `develop` cuando están completas.
- **`hotfix/*`**: Para corregir errores críticos en `main`. Se crean desde `main`, se corrigen y luego se fusionan tanto en `main` como en `develop`.
- **`release/*`**: Preparación de una nueva versión estable. Se crean desde `develop`, se prueban y se fusionan en `main` cuando están listas.
- **`docs/*`**: Preparación de una rama con documentación.

### Proceso de desarrollo
1. Un desarrollador crea una rama `feature/nueva-funcionalidad` desde `main`.
2. Se desarrolla la funcionalidad y se crean pull requests (PR) para revisión de código. Esta revisión se hace de forma automática (por CodeRabbit) como por el companero que aprueba.
3. Tras aprobarse, se fusiona en `main` y se somete a consideración la eliminación de las ramas temporales.
4. Al completar un conjunto de funcionalidades, se crea una rama `release/x.y.z` para pruebas finales.
5. Si es aprobada, la `release/x.y.z` se fusiona en `main`, se etiqueta y se lanza la versión.
6. Si surgen errores críticos en producción, se crean ramas `hotfix/x.y.z+1` desde `main` y se aplican las correcciones.


## Estrategia de Versionamiento
Utilizamos **Semantic Versioning (SemVer)** para numerar versiones:
```bash
MAJOR.MINOR.PATCH
```
- **MAJOR**: Cambios incompatibles con versiones anteriores.
- **MINOR**: Nuevas funcionalidades sin romper compatibilidad.
- **PATCH**: Correcciones de errores y mejoras menores.

### Ejemplo de versiones
- `1.0.0`: Primera versión estable del producto.
- `1.1.0`: Se agrega una nueva funcionalidad sin romper compatibilidad.
- `1.1.1`: Se corrige un bug sin modificar funcionalidades.
- `2.0.0`: Cambios importantes que hacen incompatible la nueva versión con la anterior.

### Manejo de versiones en Git
Cada versión estable se etiqueta en Git con el formato:
```bash
git tag -a vMAJOR.MINOR.PATCH -m "Descripción de la versión"
git push origin vMAJOR.MINOR.PATCH
```
Ejemplo:
```bash
git tag -a v1.0.0 -m "Primera versión estable"
git push origin v1.0.0
```
