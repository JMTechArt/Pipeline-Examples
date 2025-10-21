import asyncio
from dis import dis
import os
import json

import hashlib
from PIL import Image
from typing import Union
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def colorize_depth(depth_data):
    print(np.min(depth_data),np.max(depth_data))
    near = .6
    far = 40
    
    depth_data[depth_data == 0.0] = far
    depth_data = np.clip(depth_data, near, far)
    depth_data = (np.log(depth_data) - np.log(near)) / (np.log(far) - np.log(near))
    depth_data = 1.0 - depth_data
     
    color_map_name = "plasma"
    depth_data_colored = plt.colormaps[color_map_name](depth_data)[:, :, :3]
    depth_data_colored_uint8 = (depth_data_colored * 255).astype(np.uint8)

    return Image.fromarray(depth_data_colored_uint8)

   
def create_segmentation_legend(segmentation_img, color_to_labels, file_path):
    fig, ax = plt.subplots(figsize=(10, 10), frameon=False)
    ax.imshow(segmentation_img)
    ax.axis('off')

    color_patch_list = []
    for color, labels in color_to_labels.items():
        color_val = eval(color)
        color_patch = patches.Patch(color=[i / 255 for i in color_val], label=labels)
        color_patch_list.append(color_patch)

    legend = ax.legend(handles=color_patch_list)
    legend.get_frame().set_edgecolor('b')
    legend.get_frame().set_linewidth(0.0)

    plt.savefig(file_path, bbox_inches='tight', pad_inches=0)

def process_distance_to_camera_files(out_dir, vis_out_dir):
    for file_name in os.listdir(out_dir):
        if file_name.startswith("distance_to_camera") and file_name.endswith(".npy"):
            distance_to_camera_data = np.load(os.path.join(out_dir, file_name))
            distance_to_camera_data = np.nan_to_num(distance_to_camera_data, posinf=0)

            distance_to_camera_image = colorize_depth(distance_to_camera_data)
            output_file_name = file_name.replace(".npy", ".png")
            distance_to_camera_image.save(os.path.join(vis_out_dir, output_file_name))


def process_semantic_segmentation_files(out_dir, vis_out_dir):
    for file_name in os.listdir(out_dir):
        if file_name.startswith("semantic_segmentation_") and file_name.endswith(".png"):
            segmentation_img = Image.open(os.path.join(out_dir, file_name))

            # Construct the corresponding labels file name
            base_name = file_name.replace(".png", "")
            number_part = base_name.split("_")[-1]
            labels_file_name = f"semantic_segmentation_labels_{number_part}.json"
            
            if os.path.exists(os.path.join(out_dir, labels_file_name)):
                with open(os.path.join(out_dir, labels_file_name), "r") as json_data:
                    color_to_labels = json.load(json_data)

                create_segmentation_legend(
                    segmentation_img, color_to_labels, os.path.join(vis_out_dir, base_name + "_legend.png"))
            else:
                print(f"Labels file {labels_file_name} not found for {file_name}.")

#test training output for depth map and semantic segementation
depth_out = "C:/Omni_depth_dir"
depth_vis_out = "C:/Processed_depth_dir"
seg_out = "C:/Omni_segmentation_dir"
seg_vis_out = "C:/Processed_segmentation_dir"
process_distance_to_camera_files(depth_out, depth_vis_out)
process_semantic_segmentation_files(seg_out, seg_vis_out)

