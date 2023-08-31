import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from custom_interfaces.srv import ComponentStatus


class PerceptionNode(Node):
  
  def __init__(self):
    super().__init__('perception_node')

    self.cameraSubscriber = self.create_subscription(
        String,
        'camera',
        self.camera_callback,
        10
    )

    self.trashDetectionPublisher = self.create_publisher(
        String,
        'trash_detection',
        10
    )

    self.componentStatusService = self.create_service(
        ComponentStatus,
        'component_status',
        self.handle_component_status
    )

  def camera_callback(self, message):
    msg = String()
    """
    In practical cases, we process images to understand if trash is present
    """
    if (message.data == "trash"):
      msg.data = "trash detected"
    else:
      msg.data = "nothing detected"
    self.trashDetectionPublisher.publish(msg)
    self.get_logger().info('Publishing: "%s"' % msg.data)

  def handle_component_status(self, request, response):
    self.get_logger().info("Server called!")
    if request.component == "camera":
      response.status = "Camera Battery is at 100%"
    else:
      response.status = "Error: Component unavailable"
    return response


def main(args=None):
  rclpy.init(args=args)
  perceptionNode = PerceptionNode()
  rclpy.spin(perceptionNode)
  perceptionNode.destroy_node()
  rclpy.shutdown()


if __name__ == '__main__':
  main()
