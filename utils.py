import os
from PIL import Image
import numpy as np
import torch
from model import Net

def tensor_load_rgbimage(filename, size=None, scale=None, keep_asp=False):
    img = Image.open(filename).convert('RGB')
    if size is not None:
        if keep_asp:
            size2 = int(size * 1.0 / img.size[0] * img.size[1])
            img = img.resize((size, size2), Image.ANTIALIAS)
        else:
            img = img.resize((size, size), Image.ANTIALIAS)

    elif scale is not None:
        img = img.resize((int(img.size[0] / scale), int(img.size[1] / scale)), Image.ANTIALIAS)
    img = np.array(img).transpose(2, 0, 1)
    img = torch.from_numpy(img).float()
    return img

def tensor_save_rgbimage(tensor, filename, cuda=False):
    if cuda:
        img = tensor.clone().cpu().clamp(0, 255).numpy()
    else:
        img = tensor.clone().clamp(0, 255).numpy()
    img = img.transpose(1, 2, 0).astype('uint8')
    img = Image.fromarray(img)
    img.save(filename)


def tensor_save_bgrimage(tensor, filename, cuda=False):
    (b, g, r) = torch.chunk(tensor, 3)
    tensor = torch.cat((r, g, b))
    tensor_save_rgbimage(tensor, filename, cuda)
    
def preprocess_batch(batch):
    batch = batch.transpose(0, 1)
    (r, g, b) = torch.chunk(batch, 3)
    batch = torch.cat((b, g, r))
    batch = batch.transpose(0, 1)
    return batch

def transfer_style(path_content, path_style, style_model, user_id):
    content_image = tensor_load_rgbimage(path_content, size=400, keep_asp=True).unsqueeze(0)
    style = tensor_load_rgbimage(path_style, size=400).unsqueeze(0)    
    style = preprocess_batch(style)

    model_dict = torch.load('21styles.model')
    model_dict_clone = model_dict.copy() # We can't mutate while iterating

    for key, value in model_dict_clone.items():
        if key.endswith(('running_mean', 'running_var')):
            del model_dict[key]

    style_model.load_state_dict(model_dict, False)

    content_image = preprocess_batch(content_image)
    style_model.setTarget(style)
    output = style_model(content_image)
    tensor_save_bgrimage(output.data[0], f'img/output_{user_id}.jpg', False)
    return f'img/output_{user_id}.jpg'