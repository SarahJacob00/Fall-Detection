import tensorflow as tf
import numpy as np
from PIL import Image
import pickle
import matplotlib.pyplot as plt
import cv2 as cv

def parse_output(heatmap_data,offset_data, threshold):

    joint_num = heatmap_data.shape[-1]
    pose_kps = np.zeros((joint_num,3), np.uint32)

    for i in range(heatmap_data.shape[-1]):

        joint_heatmap = heatmap_data[...,i]
        max_val_pos = np.squeeze(np.argwhere(joint_heatmap==np.max(joint_heatmap)))
        remap_pos = np.array(max_val_pos/8*257,dtype=np.int32)
        pose_kps[i,0] = int(remap_pos[0] + offset_data[max_val_pos[0],max_val_pos[1],i])
        pose_kps[i,1] = int(remap_pos[1] + offset_data[max_val_pos[0],max_val_pos[1],i+joint_num])
        max_prob = np.max(joint_heatmap)

        if max_prob > threshold:
            if pose_kps[i,0] < 257 and pose_kps[i,1] < 257:
                pose_kps[i,2] = 1

    return pose_kps

def draw_kps(show_img,kps, ratio=None):
    for i in range(5,kps.shape[0]):
      if kps[i,2]:
        if isinstance(ratio, tuple):
          cv.circle(show_img,(int(round(kps[i,1]*ratio[1])),int(round(kps[i,0]*ratio[0]))),2,(0,255,255),round(int(1*ratio[1])))
          continue
        cv.circle(show_img,(kps[i,1],kps[i,0]),2,(0,255,255),-1)
        #cv2_imshow(show_img)
    return show_img

def draw_deviations(img, keypoints, pairs):
  for i, pair in enumerate(pairs):
    color = (0,255,255)
    cv.line(img, (keypoints[pair[0]][1], keypoints[pair[0]][0]), (keypoints[pair[1]][1], keypoints[pair[1]][0]), color=color, lineType=cv.LINE_AA, thickness=1)
  return img


#DRAW_SKELETON
def draw_skeleton(img, keypoints):
  pairs = [(5,6),(5,7),(6,8),(7,9),(8,10),(11,12),(5,11),(6,12),(11,13),(12,14),(13,15),(14,16)]
  
  for i, pair in enumerate(pairs):
    color = (0,255,255)
    cv.line(img, (keypoints[pair[0]][1], keypoints[pair[0]][0]), (keypoints[pair[1]][1], keypoints[pair[1]][0]), color=color, lineType=cv.LINE_AA, thickness=1)

  max_x=max(keypoints[i][0] for i in range(0,len(keypoints)))
  max_y=max(keypoints[i][1]for i in range(0,len(keypoints)))
  min_x=min(keypoints[i][0]for i in range(0,len(keypoints)))
  #print(keypoints,keypoints[pair[0]][1])
  min_y=min(keypoints[i][1]for i in range(0,len(keypoints)))  

  #print('MIN_X =',min_x)
  #print('MIN_y =',min_y)
  #print('Max_X =',max_x)
  #print('Max_y =',max_y)

  w=max_x-min_x
  h=max_y-min_y
  #print('W,H RECTANGLE=',w,h)
  cv.rectangle(img, ( min_y,min_x),( min_y + h,min_x + w,),(0, 255, 0), 2)
  return img,w,h
