# Exam Robot

ROS 2 пакет для симуляции учебного робота с датчиками.

## Архитектура системы

Система состоит из четырёх узлов:

- **battery_node** – публикует уровень заряда батареи (1 Hz).
- **distance_sensor** – публикует показания дальномера (5 Hz), изменяющиеся в зависимости от скорости.
- **status_display** – анализирует батарею и расстояние, публикует статус (2 Hz).
- **robot_controller** – получает статус и выдаёт команды скорости (10 Hz).
- **robot_state_publisher** – публикует TF из URDF.

### Диаграмма узлов и топиков

```mermaid
graph LR
    A[battery_node] -->|/battery_level| C[status_display]
    B[distance_sensor] -->|/distance| C
    C -->|/robot_status| D[robot_controller]
    D -->|/cmd_vel| B
    D -->|/cmd_vel| E[Внешний мир]
    F[robot_state_publisher] -->|/tf, /robot_description| G[RViz]