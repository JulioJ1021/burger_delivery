# 🧭 Ruta de inicio desde cero: del computador nuevo al primer movimiento del Kinova

Esta guía es para quien llega al proyecto sin conocerlo. Sigue **diez etapas en orden**. Cada
una termina con una comprobación ✅: si no se cumple, no avances. Arréglala con la tabla
[Si algo falla](#si-algo-falla) o con la guía detallada que se enlaza en cada etapa.

Al final habrás compilado el proyecto, visto el robot en simulación y movido el Kinova Gen3
real con [`burger_kinova_reference`](../burger_kinova_reference/README.md), el package de
referencia que valida cada movimiento antes de enviarlo.

| Etapa | Qué haces | Necesitas el robot | Hito ✅ |
|:---:|---|:---:|---|
| 0 | Entender los términos y las reglas de seguridad | No | Sabes qué es la estación anfitriona |
| 1 | Crear el workspace y clonar el proyecto | No | `~/ros2_ws/src/burger_delivery` existe |
| 2 | Instalar ROS 2 Jazzy | No | `talker` y `listener` se comunican |
| 3 | Agregar el driver de Kinova y las dependencias | No | `rosdep` termina sin errores |
| 4 | Compilar | No | Aparecen los ejecutables de `burger_kinova_reference` |
| 5 | Ver la celda en RViz | No | Ves la mesa y el brazo de 6 GDL con pinza |
| 6 | Robot simulado y primer movimiento simulado | No | La muñeca gira en RViz y el cliente termina en `SUCCESSFUL` |
| 7 | Entrar a la red del laboratorio | Sí (red) | `ping 192.168.1.10` responde |
| 8 | Conectar el robot real sin movimiento | Sí | `[TRANSICIÓN] INICIO -> OK` con el robot real |
| 9 | Primer movimiento real | Sí | El brazo gira la muñeca y el cliente termina en `SUCCESSFUL` |
| 10 | Cerrar limpiamente | Sí | Ninguna sesión queda abierta con el robot |

Las etapas 1 a 6 se hacen en cualquier computador y en cualquier lugar. Las etapas 7 a 10 se
hacen en el laboratorio, con autorización del responsable.

---

## Etapa 0 — Cinco ideas antes de empezar

| Término | Qué significa aquí |
|---|---|
| **ROS 2 Jazzy** | El *middleware* con el que se comunican todos los programas del robot. La versión del curso es Jazzy, sobre **Ubuntu 24.04**. |
| **Workspace** (`~/ros2_ws`) | Carpeta donde viven los packages. El código va en `src/`; lo que compila `colcon` queda en `install/`, y es lo que ROS 2 usa. |
| **Driver** (`ros2_kortex`) | El programa oficial de Kinova que habla con el brazo y lo expone como tópicos y acciones de ROS 2. |
| **Estación anfitriona** | El **único** computador que ejecuta el driver. Va conectado por **cable**. Las demás estaciones se conectan a él por la red y nunca lanzan otro driver ([`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md) §2.0). |
| **`ROS_DOMAIN_ID`** | Número que separa grupos de computadores en la misma red. Con el robot, todo el laboratorio usa el **0**. Para practicar solo, usa otro número para no mezclarte con nadie. |

> [!WARNING]
> **Reglas de seguridad que no se negocian.** El robot solo se mueve con autorización del
> responsable del laboratorio, con un radio libre de 1.2 m alrededor del brazo y con una persona
> junto a la parada de emergencia. Toda prueba física empieza en **modo seco**, que valida el
> movimiento sin enviarlo. Nunca lances un segundo driver contra el mismo robot.

**Sistema operativo.** Ubuntu 24.04 nativo es lo recomendado. WSL2 sobre Windows también
funciona para las etapas 1 a 6, con dos advertencias: el daemon de la CLI de ROS 2 se bloquea
con frecuencia ([`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md) §1) y la estación anfitriona por
WSL2 muestra más retardos que una nativa. Si usas WSL, revisa también
[`ros2_setup/verificar_ros2.md`](../ros2_setup/verificar_ros2.md).

---

## Etapa 1 — Crear el workspace y clonar el proyecto

```bash
sudo apt update && sudo apt install -y git
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/roncanciovl/burger_delivery.git
```

> [!NOTE]
> Si eres estudiante del curso, clona el **repositorio privado de tu equipo** en lugar del
> público, y mantenlo al día con la [guía de sincronización](../education/proyectos_evaluables/ACTUALIZACIONES_BASE_CORTE_1.md).
> La carpeta debe seguir llamándose `burger_delivery`: todas las rutas de las guías la usan.

✅ **Listo cuando** `ls ~/ros2_ws/src/burger_delivery` muestra `burger_description`,
`burger_kinova_reference`, `scripts` y `README.md`.

---

## Etapa 2 — Instalar ROS 2 Jazzy

El repositorio trae el instalador. Necesita `sudo` porque usa `apt`:

```bash
sudo bash ~/ros2_ws/src/burger_delivery/install_ros2.sh
sudo apt install -y ros-jazzy-rmw-cyclonedds-cpp
```

El primero instala ROS 2 Jazzy de escritorio y las herramientas de desarrollo (`colcon`,
`rosdep`). El segundo instala CycloneDDS, el middleware de red que usa el laboratorio.

Comprueba que ROS 2 funciona con dos terminales:

```bash
# Terminal 1
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_cpp talker

# Terminal 2
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_py listener
```

✅ **Listo cuando** el `listener` imprime `I heard: [Hello World: N]`. Detén los dos con `Ctrl+C`.

---

## Etapa 3 — Agregar el driver de Kinova y las dependencias

```bash
cd ~/ros2_ws/src
git clone https://github.com/Kinovarobotics/ros2_kortex.git

# Ajustes obligatorios del laboratorio sobre ros2_kortex, ANTES de compilar
python3 ~/ros2_ws/src/burger_delivery/scripts/aplicar_compatibilidad_kortex.py
```

El script prepara `ros2_kortex` para Jazzy y para este robot: sin él, el modelo con pinza no se
genera y el driver no arranca. Es seguro repetirlo, y con `--check` solo comprueba. Qué cambia
y por qué está en [`ros2_setup/INSTALACION_KORTEX.md`](../ros2_setup/INSTALACION_KORTEX.md) §3.4.

Ahora instala las dependencias de todos los packages del workspace:

```bash
sudo rosdep init        # solo la primera vez en este computador; si dice que ya existe, sigue
rosdep update
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -y --skip-keys "kinova_vision"
```

`kinova_vision` (el driver de la cámara) se omite porque solo lo necesita la estación anfitriona
cuando usa la cámara, y no se instala con `apt`. Esa estación lo prepara con
`bash ~/ros2_ws/src/burger_delivery/scripts/aplicar_parche_kinova_vision.sh`
([Laboratorio 02](../education/guias_laboratorio/GUIA_LAB_02_PRUEBAS_CAMARA_KINOVA_VISION.md)).

✅ **Listo cuando** `rosdep` termina con `#All required rosdeps installed successfully`.

---

## Etapa 4 — Compilar

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

La primera compilación del driver tarda varios minutos. Si el computador tiene poca memoria y se
congela, repite con `colcon build --symlink-install --parallel-workers 2`.

Compila **siempre desde `~/ros2_ws`**, nunca desde una carpeta interna. Si cambias un URDF o un
launch, vuelve a compilar: ROS 2 lee lo que está en `install/`, no en `src/`.

```bash
ros2 pkg executables burger_kinova_reference
```

✅ **Listo cuando** aparecen `escena_moveit`, `kinova_monitor`, `moveit_safe_executor`,
`safe_sequence_client` y `safe_trajectory_client`.

> [!TIP]
> Para no repetir los `source` en cada terminal, agrega estas dos líneas al final de
> `~/.bashrc`:
>
> ```bash
> source /opt/ros/jazzy/setup.bash
> source ~/ros2_ws/install/setup.bash
> ```

---

## Etapa 5 — Ver la celda en RViz, sin robot

Usa un dominio propio para que tu visor no se mezcle con el de nadie:

```bash
export ROS_DOMAIN_ID=42          # cualquier número entre 1 y 101 distinto del 0
ros2 launch burger_description display.launch.py use_static_carts:=true
```

✅ **Listo cuando** RViz muestra la mesa, el Kinova Gen3 de **6 GDL** con la pinza Robotiq 2F-85
y los dos carritos, y los deslizadores de la ventana *Joint State Publisher* mueven el brazo.

Para entender lo que estás viendo (URDF, TF, el marco de la cámara), sigue el
[Taller URDF y TF2](../education/talleres/TALLER_URDF_TF.md). Cierra todo con `Ctrl+C` antes
de la etapa 6.

---

## Etapa 6 — Robot simulado y primer movimiento simulado

Aquí corres el **driver real de Kinova** con hardware simulado (`use_fake_hardware:=true`). Todo
el flujo es idéntico al del robot físico, así que esta etapa es el ensayo general de las
etapas 8 y 9.

**Terminal 1 — driver simulado, monitor y RViz:**

```bash
export ROS_DOMAIN_ID=42
ros2 launch burger_kinova_reference kinova_connection.launch.py \
  start_driver:=true robot_ip:=0.0.0.0 use_fake_hardware:=true \
  launch_rviz:=true enable_motion:=false
```

Espera en la consola `[TRANSICIÓN] INICIO -> OK` y `[CONTROLADORES] ... =active`. En modo
simulado el launch omite la pinza a propósito y lo avisa: es una incompatibilidad conocida de
`ros2_kortex` con Jazzy ([README del package](../burger_kinova_reference/README.md) §6.1).

**Terminal 2 — lee la pose actual del brazo:**

```bash
export ROS_DOMAIN_ID=42
ros2 topic echo /joint_states --once
```

Anota la posición de cada articulación **por su nombre** (`joint_1` … `joint_6`). El orden del
mensaje no tiene por qué ser 1, 2, 3…: guíate por el campo `name`.

**Terminal 2 — prepara la meta.** Copia las seis posiciones y cambia solo `joint_6` sumándole
`0.10` rad. `joint_6` gira la pinza sobre su eje: es el movimiento de menor riesgo. Por
ejemplo, si leíste `joint_1 … joint_6 = [0.0, 0.26, 3.14, -2.27, 0.0, 0.96]`, la meta es
`[0.0, 0.26, 3.14, -2.27, 0.0, 1.06]`. **Usa los números de tu lectura**, no los del ejemplo.

```bash
CFG=$(ros2 pkg prefix burger_kinova_reference)/share/burger_kinova_reference/config/kinova_connection.yaml

# 1) Modo seco: valida todo y NO envía nada
ros2 run burger_kinova_reference safe_trajectory_client --ros-args --params-file $CFG \
  -p use_fake_hardware:=true -p enable_motion:=true -p dry_run:=true \
  -p "safe_joint_positions_rad:=[<j1>, <j2>, <j3>, <j4>, <j5>, <j6 + 0.10>]"
echo $?
```

El cliente imprime una tabla con la posición actual, la meta y el cambio de cada articulación.
Debe terminar sin bloqueos y `echo $?` debe dar `0`. Si dice `META BLOQUEADA`, lee el motivo:
casi siempre es un número mal copiado, que supera `max_joint_delta_rad` (0.35 rad).

```bash
# 2) Envío al robot simulado: el mismo comando con dry_run:=false
ros2 run burger_kinova_reference safe_trajectory_client --ros-args --params-file $CFG \
  -p use_fake_hardware:=true -p enable_motion:=true -p dry_run:=false \
  -p "safe_joint_positions_rad:=[<j1>, <j2>, <j3>, <j4>, <j5>, <j6 + 0.10>]"
```

Responde `si` cuando pregunte `¿Enviar meta al servidor de acción? [si/no]`.

✅ **Listo cuando** la muñeca gira en RViz, el cliente informa `SUCCESSFUL` y `echo $?` da `0`.
Detén la terminal 1 con `Ctrl+C`.

---

## Etapa 7 — Entrar a la red del laboratorio

La red del laboratorio es una sola subred, `192.168.1.0/24`:

| Equipo | Dirección |
|---|---|
| Router TP-Link AX12 (SSID `ros2`) | `192.168.1.1` |
| Kinova Gen3 | `192.168.1.10` |
| Estación anfitriona (por cable) | `192.168.1.100` |
| Demás estaciones (Wi-Fi o cable) | `192.168.1.101` a `.254`, por DHCP |

```bash
ip -brief addr            # tu tarjeta de red debe tener una IP 192.168.1.x
ping -c 4 192.168.1.10    # el robot
```

Si tu IP no empieza por `192.168.1.`, estás en otra red (por ejemplo, la institucional):
conéctate al SSID `ros2`. Detalles en [`network_setup/ROS2_NETWORK_CONFIG.md`](../network_setup/ROS2_NETWORK_CONFIG.md).

Desde aquí, en **todas** las terminales de **todas** las estaciones, carga el entorno del curso
y reinicia el daemon de la CLI, que queda atado al dominio con el que arrancó:

```bash
export ROS_DOMAIN_ID=0
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI="file://$HOME/ros2_ws/src/burger_delivery/network_setup/cyclonedds.xml"
timeout 5s ros2 daemon stop; ros2 daemon start
```

✅ **Listo cuando** `ping` responde sin pérdidas y `echo $ROS_DOMAIN_ID` da `0`.

---

## Etapa 8 — Conectar el robot real, sin movimiento

**Antes de lanzar nada, averigua si alguien ya tiene el robot:**

```bash
timeout 15s ros2 node list | grep controller_manager
```

- **Si aparece**, ya hay un driver: tu estación es **cliente**. No lances otro. Conéctate así:

  ```bash
  ros2 launch burger_kinova_reference kinova_connection.launch.py start_driver:=false
  ```

- **Si no aparece y tú eres la estación anfitriona designada** (por cable), lanza el driver:

  ```bash
  ros2 launch burger_kinova_reference kinova_connection.launch.py \
    start_driver:=true robot_ip:=192.168.1.10 use_fake_hardware:=false \
    launch_rviz:=true enable_motion:=false
  ```

  El launch vuelve a comprobar si existe otro driver y, si lo encuentra, continúa como cliente.

En otra terminal, comprueba el enlace:

```bash
ros2 topic hz /joint_states
ros2 topic echo /burger/kinova/diagnostics --once | grep -A8 "identidad de la estación"
```

✅ **Listo cuando** la consola del launch muestra `[TRANSICIÓN] INICIO -> OK`, `/joint_states`
llega de forma estable (por encima de 20 Hz), el diagnóstico indica quién es la anfitriona y
RViz refleja la pose real del brazo.

---

## Etapa 9 — Primer movimiento real

Es el mismo procedimiento de la etapa 6, ahora sobre el robot físico. **Lo ejecuta una sola
persona** y el resto del laboratorio lo observa.

1. **Pide autorización** al responsable del laboratorio. Despeja 1.2 m alrededor del brazo y
   ubica a una persona junto a la parada de emergencia.
2. **Lee la pose real** con `ros2 topic echo /joint_states --once`. Con el robot real el mensaje
   trae también la articulación de la pinza (`robotiq_85_left_knuckle_joint`): **no la copies**.
   La meta lleva solo `joint_1` a `joint_6`.
3. **Prepara la meta** sumando `0.10` rad a `joint_6`, igual que en la etapa 6.
4. **Modo seco** sobre el hardware real:

   ```bash
   CFG=$(ros2 pkg prefix burger_kinova_reference)/share/burger_kinova_reference/config/kinova_connection.yaml
   ros2 run burger_kinova_reference safe_trajectory_client --ros-args --params-file $CFG \
     -p use_fake_hardware:=false -p enable_motion:=true -p dry_run:=true \
     -p "safe_joint_positions_rad:=[<j1>, <j2>, <j3>, <j4>, <j5>, <j6 + 0.10>]"
   echo $?
   ```

   Todas las filas deben verse `✓ OK` y `echo $?` debe dar `0`. Muestra el resultado al
   responsable.
5. **Con autorización en voz alta**, envía el **mismo** comando cambiando solo `dry_run:=false`.
   Recupéralo con la flecha ↑ en lugar de volver a escribir los números. Responde `si`.

✅ **Listo cuando** la pinza gira unos 6° sobre su eje, el cliente informa `SUCCESSFUL`, `echo $?`
da `0` y la nueva pose coincide con la meta en `ros2 topic echo /joint_states --once`.

**Si algo se ve mal, pulsa la parada de emergencia.** Para cancelar desde el teclado, usa
`Ctrl+C` en el cliente: el controlador detiene el brazo.

---

## Etapa 10 — Cerrar limpiamente

1. Detén el cliente y luego el launch del driver con `Ctrl+C`, en ese orden.
2. En la estación anfitriona, confirma que no quedó ninguna sesión abierta con el robot:

   ```bash
   ss -tanp | grep "192.168.1.10"      # no debe quedar ninguna línea ESTAB
   ```

3. Si vas a seguir practicando sin robot, vuelve a tu dominio propio
   (`export ROS_DOMAIN_ID=42`) y reinicia el daemon.

✅ **Listo cuando** `ss` no muestra conexiones con `192.168.1.10` y otra estación puede tomar
el robot.

---

## Si algo falla

Recorre las capas en orden: primero la red, después ROS 2, después el driver y al final tu
comando.

| Síntoma | Dónde está la respuesta |
|---|---|
| `ros2 node list` o `ros2 topic list` se quedan colgados o dan `TimeoutError` | [`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md) §1 (daemon de la CLI) |
| El driver no arranca, o aparece `/joint_states` duplicado | [`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md) §2 (robot ocupado) |
| `Invalid parameter "mock_sensor_commands"` o `invalid syntax (<expression>, line 0)` | Falta la etapa 3: [`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md) §3.2 y §3.3 |
| `/joint_states` con una séptima articulación del brazo (`joint_7`) | El driver corre con `dof:=7`: [`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md) §3.1 |
| `Overrun detected` o pérdidas de telemetría | La anfitriona está por Wi-Fi: pásala a cable ([README del package](../burger_kinova_reference/README.md) §10) |
| `META BLOQUEADA` en el cliente | Lee el motivo que imprime; tabla completa en el [README del package](../burger_kinova_reference/README.md) §8 y §10 |
| En RViz faltan mallas o salen en rojo | Vuelve a compilar `burger_description`: [`TROUBLESHOOTING.md`](../TROUBLESHOOTING.md) §4.5 |

---

## Siguientes pasos

| Para… | Sigue con |
|---|---|
| Entender la CLI de ROS 2 | [Taller CLI de ROS 2](../education/talleres/TALLER_ROS2_CLI.md) |
| Entender el modelo del robot y los marcos TF | [Taller URDF y TF2](../education/talleres/TALLER_URDF_TF.md) |
| Registrar y depurar lo que pasa | [Taller rosbag2, logging y depuración](../education/talleres/TALLER_ROSBAG_LOGGING_DEBUGGING.md) |
| Operar el robot por turnos entre varias estaciones | [Laboratorio 03](../education/guias_laboratorio/GUIA_LAB_03_OPERACION_DISTRIBUIDA_KINOVA_TURNOS.md), incluida la secuencia autónoma `safe_sequence_client` |
| Planificar movimientos con MoveIt 2 | [Laboratorio 04](../education/guias_laboratorio/GUIA_LAB_04_MOVEIT2_EJECUCION_SEGURA.md) y el [README del package](../burger_kinova_reference/README.md) §13 |
| Usar la cámara del robot | [Laboratorio 02](../education/guias_laboratorio/GUIA_LAB_02_PRUEBAS_CAMARA_KINOVA_VISION.md) |
| Razonamiento espacial con IA | [Laboratorio IA 01 — Embodied AI](../education/guias_laboratorio/GUIA_LAB_IA_01_EMBODIED_AI_GEMINI_ER2_KINOVA.md) |

Documentación completa del package usado en esta ruta:
[`burger_kinova_reference/README.md`](../burger_kinova_reference/README.md).
