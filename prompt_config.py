
prompt_template_text = """Use the reasoning paths to answer the question.

Output format:
["answer1", "answer2", ...]

Rules:
- Return ONLY a Python list of answers.
- No explanations, reasoning, or extra text.
- Do not restate the question.
- Include all possible correct answers.


Reasoning Paths:
{reasoning_paths}

Question:
{question}

Answer:"""

prompt_template_image = """Use the reasoning paths and the image to answer the question.

Output format:
["answer1", "answer2", ...]

Rules:
- Return ONLY a Python list of answers.
- No explanations, reasoning, or extra text.
- Do not restate the question.
- Include all possible correct answers.

Reasoning Paths:
{reasoning_paths}

Question:
{question}

Answer:"""

prompt_template_image_only = """Use the image to answer the question.

Output format:
["answer1", "answer2", ...]

Rules:
- Return ONLY a Python list of answers.
- No explanations or additional text.
- Do not restate the question.
- Include all possible correct answers.

Question:
{question}

Answer:"""


prompt_configs = [
    {
        "prompt_type": "text_only",
        "template": prompt_template_text,
        "use_image": False,
        "use_reasoning_paths": True,
        "image_mode": None,              # no images
    },
    {
        "prompt_type": "text_plus_image",
        "template": prompt_template_image,
        "use_image": True,
        "use_reasoning_paths": True,
        "image_mode": "single_triples",  # one image from row["triples"]
    },
    {
        "prompt_type": "image_only",
        "template": prompt_template_image_only,
        "use_image": True,
        "use_reasoning_paths": False,
        "image_mode": "single_triples",  # one image from row["triples"]
    },
    {
        # Chaos
        "prompt_type": "text_plus_image",
        "template": prompt_template_image,
        "use_image": True,
        "use_reasoning_paths": True,
        "image_mode": "single_triples",  # one image from row["triples"]
        "image_ablation": "chaos"
    },
       {
        # NX
        "prompt_type": "text_plus_image",
        "template": prompt_template_image,
        "use_image": True,
        "use_reasoning_paths": True,
        "image_mode": "single_triples",  # one image from row["triples"]
        "image_ablation": "nx"
    },
    {
        "prompt_type": "text_plus_rps_images",
        "template": prompt_template_image,
        "use_image": True,
        "use_reasoning_paths": True,
        "image_mode": "rps_multi",       # one image per item in row["rps_triples"]
    }

]