from graphviz import Digraph, Graph
import os
import base64
import pandas as pd
import io
from PIL import Image
from graph_image_gen import *



def resize_max768_pil(image_path):
    img = Image.open(image_path)

    w, h = img.size
    max_dim = max(w, h)

    if max_dim > 768:
        scale = 768 / max_dim
        new_size = (int(w * scale), int(h * scale))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    return img

def encode_image_pil(img):
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return base64.b64encode(buffer.read()).decode("utf-8")


def triples_to_diagram(i, row, dataset, out_dir="pngs", cfg={}, rankdir="LR"):
    ablation = cfg.get("image_ablation")
    # print("here"*100)
    os.makedirs(out_dir, exist_ok=True)
    # create special subfolders if ablation
    if ablation is not None:
        os.makedirs(os.path.join(out_dir, ablation),  exist_ok=True)
        out_base = os.path.join(out_dir, ablation, dataset)
    else:
        out_base = os.path.join(out_dir, dataset)
    os.makedirs(out_base, exist_ok=True)
    out_base = os.path.join(out_base, f"{i}")\
    # ablation renders differntly
    if ablation == 'chaos':
        return triples_group_to_diagram_chaos(row["triples"], out_base)
    if ablation == 'nx':
        return triples_group_to_diagram_nx(row["triples"], out_base)
    else:
        return triples_group_to_diagram(row["triples"], out_base, rankdir=rankdir)
     


def render_rps_triple_images(row_id, rps_triples, dataset, out_dir="pngs_rps", rankdir="LR"):
    os.makedirs(out_dir, exist_ok=True)
    image_paths = []

    for j, triple_group in enumerate(rps_triples):
        os.makedirs(out_dir, exist_ok=True)
        out_base = os.path.join(out_dir, dataset)
        os.makedirs(out_base, exist_ok=True)
        out_base = os.path.join(out_base, f"{row_id}_{j}")
        rendered_path = triples_group_to_diagram(triple_group, out_base, rankdir=rankdir)
        image_paths.append(rendered_path)

    return image_paths


# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")

def encode_image(image_path, max_size=(512, 512), quality=85, fmt="jpeg"):
    with Image.open(image_path) as img:
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img.thumbnail(max_size)

        buffer = io.BytesIO()
        img.save(buffer, format=fmt, quality=quality, optimize=True)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

def build_content_for_row(i, row, prompt, cfg, dataset):
    content = [{"type": "text", "text": prompt}]

    if not cfg["use_image"]:
        return content

    if cfg["image_mode"] == "single_triples":
        image_path = triples_to_diagram(i, row, dataset, cfg=cfg)
        base64_image = encode_image(image_path)
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}"
            }
        })

    elif cfg["image_mode"] == "rps_multi":
        image_paths = render_rps_triple_images(i, row["rps_triples"], dataset)

        for image_path in image_paths:
            img = resize_max768_pil(image_path)
            base64_image = encode_image_pil(img)

            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"
                }
            })

    else:
        raise ValueError(f"Unsupported image_mode: {cfg['image_mode']}")

    return content


def paths_to_triples(paths, return_df=False):
    """
    Convert a list of '->' paths into triples (subject, predicate, object).

    Args:
        paths (list of str): Each string is a path like
            'A -> p1 -> B -> p2 -> C'
        return_df (bool): If True, returns a pandas DataFrame instead of list of tuples.

    Returns:
        list of tuples [(subject, predicate, object), ...] or DataFrame
    """
    triples = []
    for path in paths:
        parts = [p.strip() for p in path.split("->")]
        for i in range(0, len(parts)-2, 2):
            subj = parts[i]
            pred = parts[i+1]
            obj = parts[i+2]
            triples.append((subj, pred, obj))
    
    if return_df:
        return pd.DataFrame(triples, columns=["subject", "predicate", "object"])
    return triples
