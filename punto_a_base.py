import rclpy
from geometry_msgs.msg import PointStamped
from tf2_ros import Buffer, TransformListener
import tf2_geometry_msgs  # Registra la transformación de PointStamped


def main():
    rclpy.init()
    nodo = rclpy.create_node('punto_a_base')

    buffer = Buffer()
    listener = TransformListener(buffer, nodo)

    p = PointStamped()
    p.header.frame_id = 'gen3_camera_color_frame'
    p.header.stamp = rclpy.time.Time().to_msg()
    p.point.x = 0.10
    p.point.y = 0.05
    p.point.z = 0.60

    try:
        for _ in range(100):
            rclpy.spin_once(nodo, timeout_sec=0.1)

            if buffer.can_transform(
                'gen3_base_link',
                p.header.frame_id,
                rclpy.time.Time()
            ):
                resultado = buffer.transform(p, 'gen3_base_link')
                print('Punto expresado en gen3_base_link:')
                print(resultado.point)
                return

        print('No se encontró la transformación. Revisa los frames y el dominio ROS.')

    finally:
        nodo.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

