"""
    Code related to face detection and manipulation
"""

#pip install facenet_pytorch

from facenet_pytorch import MTCNN
mtcnn = MTCNN(image_size=256, margin=80)

# simplest ye olde trustworthy MTCNN for face detection with landmarks
def detect(img):
 
        # Detect faces
        batch_boxes, batch_probs, batch_points = mtcnn.detect(img, landmarks=True)
        # Select faces
        if not mtcnn.keep_all:
            batch_boxes, batch_probs, batch_points = mtcnn.select_boxes(
                batch_boxes, batch_probs, batch_points, img, method=mtcnn.selection_method
            )
 
        return batch_boxes, batch_points

# my version of isOdd, should make a separate repo for it :D
def makeEven(_x):
  return _x if (_x % 2 == 0) else _x+1

# the actual scaler function
def scale(boxes, _img, max_res=1_500_000, target_face=256, fixed_ratio=0, max_upscale=2, VERBOSE=False):
 
    x, y = _img.size
 
    ratio = 2 #initial ratio
 
    #scale to desired face size
    if (boxes is not None):
      if len(boxes)>0:
        ratio = target_face/max(boxes[0][2:]-boxes[0][:2]); 
        ratio = min(ratio, max_upscale)
        if VERBOSE: print('up by', ratio)

    if fixed_ratio>0:
      if VERBOSE: print('fixed ratio')
      ratio = fixed_ratio
 
    x*=ratio
    y*=ratio
 
    #downscale to fit into max res 
    res = x*y
    if res > max_res:
      ratio = pow(res/max_res,1/2); 
      if VERBOSE: print(ratio)
      x=int(x/ratio)
      y=int(y/ratio)
 
    #make dimensions even, because usually NNs fail on uneven dimensions due skip connection size mismatch
    x = makeEven(int(x))
    y = makeEven(int(y))
    
    size = (x, y)

    return _img.resize(size)

""" 
    A useful scaler algorithm, based on face detection.
    Takes PIL.Image, returns a uniformly scaled PIL.Image

    boxes: a list of detected bboxes
    _img: PIL.Image
    max_res: maximum pixel area to fit into. Use to stay below the VRAM limits of your GPU.
    target_face: desired face size. Upscale or downscale the whole image to fit the detected face into that dimension.
    fixed_ratio: fixed scale. Ignores the face size, but doesn't ignore the max_res limit.
    max_upscale: maximum upscale ratio. Prevents from scaling images with tiny faces to a blurry mess.
"""

def scale_by_face_size(_img, max_res=1_500_000, target_face=256, fix_ratio=0, max_upscale=2, VERBOSE=False):
    boxes = None
    boxes, _ = detect(_img)
    if VERBOSE: print('boxes',boxes)
    img_resized = scale(boxes, _img, max_res, target_face, fix_ratio, max_upscale, VERBOSE)
    return img_resized

