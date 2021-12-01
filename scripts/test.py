from eval import *
from yolact_edge.utils.logging_helper import setup_logger

# from google.colab.patches import cv2_imshow

parse_args(["--config=yolact_edge_youtubevis_config", "--calib_images=../calib_images"])


from eval import args

setup_logger(logging_level=logging.INFO)
logger = logging.getLogger("yolact.eval")

args.trained_model = "/home/autoware/catkin_ws/src/beginner_tutorials/scripts/weights/yolact_edge_youtubevis_847_50000.pth"
args.yolact_transfer = True

torch.set_default_tensor_type('torch.cuda.FloatTensor')

logger.info('Loading model...')
net = Yolact(training=False)
net.load_weights(args.trained_model, args=args)
net.eval()
logger.info('Model loaded.')

net.detect.use_fast_nms = args.fast_nms
cfg.mask_proto_debug = args.mask_proto_debug

args.score_threshold = 0.5
args.top_k = 15

im = cv2.imread("/home/autoware/catkin_ws/src/yolact/yolact_edge/test.png")

frame = torch.from_numpy(im).cuda().float()
batch = FastBaseTransform()(frame.unsqueeze(0))

extras = {"backbone": "full", "interrupt": False, "keep_statistics": False,
          "moving_statistics": None}

with torch.no_grad():
    preds = net(batch, extras=extras)["pred_outs"]

dets = preds[0]

img_numpy = prep_display(preds, frame, None, None, undo_transform=False)
# cv2.imshow("test", img_numpy)
# cv2.waitKey()
cv2.imwrite("out.png", img_numpy)

