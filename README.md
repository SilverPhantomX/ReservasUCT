# ReservasUCT — Sistema de Reservas de la Academia de Artes Musicales UCT

Aplicación móvil hecha con **Kivy + KivyMD** para reservar salas de práctica en la Academia de Artes Musicales de la Universidad Católica de Temuco. Reemplaza el registro en papel con el que hoy se gestionan las reservas y los préstamos.

> Proyecto del curso **Desarrollo Móvil (TINF1119V)**, Evaluación Integrada RA1.

---

## La problemática

La secretaria de la Academia de Artes Musicales de la UCT dedica mucho tiempo a **ordenar y gestionar a mano los papeles** de las reservas y de los préstamos de instrumentos y materiales.

Esto trae tres problemas concretos:

| # | Problema | Qué significa en la práctica |
|---|----------|------------------------------|
| 1 | **Pérdida de tiempo** | Ordenar y buscar registros a mano es lento e ineficiente. |
| 2 | **Riesgo de errores** | Los papeles se pueden traspapelar, dañar o perder. |
| 3 | **Falta de control** | Cuesta saber qué reservas o préstamos están vigentes, atrasados o devueltos. |

A quienes usan la academia también les afecta: no pueden saber si una sala está libre sin ir a preguntar en persona.

## Nuestra solución

Proponemos un **sistema digital de reservas y préstamos** con dos partes:

1. **App móvil para usuarios** (estudiantes y personas externas): reservan una sala desde el celular, ven solo los horarios libres y pueden anular sus reservas. **← Es el prototipo de este repositorio.**
2. **Panel administrativo para la secretaria**: un calendario semanal con todas las reservas ordenadas por día y horario, más un resumen general (total de reservas, clases, ensayos y estudios). *(Planificado. Ver [Hoja de ruta](#hoja-de-ruta).)*

### Beneficios esperados

- **Se deja de usar papel** y baja el tiempo de gestión manual.
- **Menos errores y menos pérdida de información**: el sistema valida los datos e impide que dos reservas choquen.
- **La secretaria ve de forma clara y ordenada** todas las reservas vigentes.

---

## Qué hace el prototipo actual

| Pantalla | Funcionalidad |
|----------|---------------|
| **Inicio** | Bienvenida, número de reservas próximas, lista de salas con su capacidad y horario de la academia. |
| **Reservas** | Formulario de reserva: nombres, apellidos, correo, motivo (Estudio / Ensayo / Clases), sala, fecha (calendario), hora de inicio, duración, acompañantes y afiliación. Antes de guardar, pide confirmación en un diálogo. |
| **Perfil** | Lista de las próximas reservas, con la opción de **anular** cada una (también pide confirmación). |

### Reglas que valida la app

- Nombres y apellidos solo con letras.
- Correo con formato válido. Los **estudiantes** deben usar su correo institucional (`@uct.cl` / `@alu.uct.cl`).
- Máximo **3 acompañantes**, y nunca más personas que la **capacidad de la sala**.
- No se aceptan **fechas pasadas** ni **domingos**.
- Horario de atención de **09:00 a 21:00**. La reserva tiene que terminar antes del cierre.
- **No puede haber dos reservas** de la misma sala con horarios que se crucen. El menú de horas muestra solo las horas libres.

### Salas configuradas

| Sala | Capacidad |
|------|-----------|
| Sala de Piano | 2 personas |
| Sala de Ensayo (Banda) | 4 personas |
| Cabina de Estudio Individual | 1 persona |
| Sala de Percusión | 4 personas |

*(Las salas se definen en `SALAS`, dentro de [modelos.py](modelos.py).)*

### Componentes de KivyMD que usa

| Requisito de la evaluación | Dónde se usa |
|----------------------------|--------------|
| Pantalla navegable con `BoxLayout` | Todas las pantallas se arman con `MDBoxLayout` y se navega con `MDScreenManager` y una barra inferior. |
| `MDDialog` en una acción real | Confirmar una reserva, anular una reserva y mostrar los errores del formulario. |
| `MDTextField` | Nombres, Apellidos y Correo. |
| `MDDropdownMenu` | Sala, Hora de inicio, Duración y Acompañantes. |
| Extra | `MDModalDatePicker` para elegir la fecha. |

---

## Diseño orientado a objetos

La lógica del negocio está en [modelos.py](modelos.py), **separada de la interfaz**. Así las reglas se pueden probar sin abrir la app, y la interfaz se puede cambiar sin tocar las reglas.

```
┌──────────────────────────────┐        ┌──────────────────────────────┐
│           Reserva            │        │        GestorReservas        │
├──────────────────────────────┤        ├──────────────────────────────┤
│ nombres, apellidos, correo   │  0..*  │ reservas: list[Reserva]      │
│ motivo, sala, fecha          │◄───────│ ruta_archivo                 │
│ hora_inicio, duracion        │        ├──────────────────────────────┤
│ acompanantes, afiliacion     │        │ agregar(reserva) -> errores  │
├──────────────────────────────┤        │ anular(id)                   │
│ hora_fin, horario (property) │        │ buscar_choque(reserva)       │
│ validar() -> list[str]       │        │ proximas()                   │
│ se_superpone_con(otra)       │        │ horas_ocupadas(sala, fecha)  │
│ resumen()                    │        │ guardar() / cargar()  (JSON) │
│ a_diccionario() / desde_...  │        └──────────────────────────────┘
└──────────────────────────────┘
```

- **`Reserva`** representa *una* reserva y **se valida a sí misma**: cada reserva conoce sus propias reglas (formato del correo, capacidad de la sala, horario, etc.).
- **`GestorReservas`** administra el **conjunto** de reservas. Las reglas que dependen de varias reservas, como evitar que dos se crucen, van aquí y no en `Reserva`. También se encarga de guardar los datos en JSON.
- La interfaz ([pantallas.py](pantallas.py)) solo arma un objeto `Reserva` con lo que escribió el usuario y se lo entrega al gestor.

---

## Estructura del proyecto

```
ReservasUCT/
├── App.py              # Punto de entrada: arma la ventana, las pantallas y la navegación
├── modelos.py          # Lógica de negocio (POO): Reserva y GestorReservas
├── pantallas.py        # Interfaz: componentes reutilizables y las 3 pantallas
├── requirements.txt    # Dependencias
├── archivos_generales/ # Presentación de la problemática
└── rubrica/            # Pauta de la evaluación
```

## Cómo ejecutarlo

Requiere **Python 3.10 o superior**.

```bash
# 1. Crear y activar un entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
python App.py
```

En el computador, la ventana se abre con tamaño de teléfono (400×780).

Las reservas se guardan en un archivo `reservas.json` dentro de la carpeta de datos de la app (en Linux, `~/.config/reservasuct/`). Así no se pierden al cerrar la app.

---

## Hoja de ruta

- [x] Formulario de reserva con validaciones
- [x] Detección de choques de horario y menú con solo las horas libres
- [x] Ver y anular reservas
- [x] Guardar los datos en un archivo local (JSON)
- [ ] **Panel administrativo** para la secretaria: calendario semanal y resumen (total de reservas, clases, ensayos y estudios)
- [ ] **Préstamos de instrumentos y materiales**: registro, fecha de devolución y estado (vigente / atrasado / devuelto)
- [ ] Inicio de sesión para separar las reservas de cada usuario
- [ ] Base de datos compartida, para que la app y el panel vean la misma información

---

## Equipo

- Christopher Córdova
- Felipe Velásquez
- Anthony García
- Franko Zambrano
