#!/usr/bin/env python

from eval import *
from yolact_edge.utils.logging_helper import setup_logger

# from google.colab.patches import cv2_imshow

parse_args(["--config=yolact_edge_config", "--calib_images=../calib_images"])


from eval import args
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
import datetime

setup_logger(logging_level=logging.INFO)
logger = logging.getLogger("yolact.eval")

args.trained_model = "/home/autoware/catkin_ws/src/beginner_tutorials/scripts/weights/yolact_edge_54_800000.pth"
args.yolact_transfer = True

torch.set_default_tensor_type('torch.cuda.FloatTensor')

logger.info('Loading model...')
net = Yolact(training=False)
net.load_weights(args.trained_model, args=args)
net.eval()
logger.info('Model loaded.')

net.detect.use_fast_nms = args.fast_nms
cfg.mask_proto_debug = args.mask_proto_debug

args.score_threshold = 0.3
args.top_k = 15

def callback(data):
    # image_pubulish=rospy.Publisher('/camera/image_changes',Image,queue_size=1)
    bridge = CvBridge()
    try:
      cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    im_padding = cv2.copyMakeBorder(cv_image,200,200,0,0,cv2.BORDER_CONSTANT,value=[0,0,0])
    frame = torch.from_numpy(im_padding).cuda().float()
    batch = FastBaseTransform()(frame.unsqueeze(0))

    extras = {"backbone": "full", "interrupt": False, "keep_statistics": False,
          "moving_statistics": None}

    with torch.no_grad():
      preds = net(batch, extras=extras)["pred_outs"]

    dets = preds[0]

    img_numpy = prep_display(preds, frame, None, None, undo_transform=False)
    cv2.imshow("test", img_numpy)
    cv2.waitKey(3)

def saveimg(data):
    bridge = CvBridge()
    try:
      cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    name = "/home/autoware/shared_dir/img/out"+ str(datetime.datetime.now())[-5:]+ ".png"
    cv2.imwrite(name , cv_image)

    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/d400/color/image_raw", Image, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()

