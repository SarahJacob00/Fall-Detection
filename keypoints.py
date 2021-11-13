import tensorflow as tf
import numpy as np
from PIL import Image
import pickle
import matplotlib.pyplot as plt
import cv2 as cv
from parseout import parse_output,draw_kps,draw_deviations,draw_skeleton
import math
model_path = "posenet_mobilenet_v1_100_257x257_multi_kpt_stripped.tflite"



def get_keypoints(template_path,i):


  interpreter = tf.lite.Interpreter(model_path=model_path)
  interpreter.allocate_tensors()

  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()

  height = input_details[0]['shape'][1]
  width = input_details[0]['shape'][2]

  im = Image.fromarray(template_path)
  #dst ="Hostel" + str(i) + ".jpg"
  im.save("filename"+str(i)+".jpeg")

  template_path="filename"+str(i)+".jpeg"
  template_image_src =cv.imread(template_path) 

  template_image = cv.resize(template_image_src, (width, height))
  template_input = np.expand_dims(template_image.copy(), axis=0)
  
  floating_model = input_details[0]['dtype'] == np.float32
 
  if floating_model:
    template_input = (np.float32(template_input) - 127.5) / 127.5

  interpreter.set_tensor(input_details[0]['index'], template_input)

  interpreter.invoke()
 
  template_output_data = interpreter.get_tensor(output_details[0]['index'])
  template_offset_data = interpreter.get_tensor(output_details[1]['index'])
 
  template_heatmaps = np.squeeze(template_output_data)
  template_offsets = np.squeeze(template_offset_data)

  template_show = np.squeeze((template_input.copy()*127.5+127.5)/255.0)
  template_show = np.array(template_show*255,np.uint8)
  keypoints = parse_output(template_heatmaps,template_offsets,0.3)
  #print(keypoints)
  

  return template_show,keypoints,height,width