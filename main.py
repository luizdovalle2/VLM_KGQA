import pandas as pd
import pickle
import os
from tqdm import tqdm
from openai import OpenAI

from render_helper import *
from prompt_config import *
    
dataset = "all"
df_merged = pd.read_pickle(f"df_kgqa.pkl")
df_merged["triples"] = df_merged["reasoning_paths"].apply(lambda x: list(set(paths_to_triples(x.split("\n")))))
df_merged["rps"] = df_merged["reasoning_paths"].apply(lambda x: list(x.split("\n")))
df_merged["rps_triples"] = df_merged["rps"].apply(
    lambda x: [list(set(paths_to_triples([y]))) for y in x]
)



api_key = "[PLACHOLDER]"
llm_base_url = "[PLACHOLDER]"




client = OpenAI(api_key=api_key, base_url=llm_base_url)

models =[
    
        'qwen/qwen3.5-35b-a3b',
        'qwen/qwen3.5-122b-a10b', 
        'mistralai/mistral-small-3.1-24b-instruct',
       'mistralai/mistral-medium-3.1',
       'google/gemini-3.1-flash-lite',
       
         'google/gemini-3-flash-preview'
         ]


save_dir = "answers_pickles"
os.makedirs(save_dir, exist_ok=True)
df_top = df_merged
for model in models:
    
    for cfg in prompt_configs:
        answers = []
        prompt_type = cfg["prompt_type"]
        config_type = cfg["prompt_type"] if cfg.get("image_ablation") is None else f'{cfg["prompt_type"]}_{cfg.get("image_ablation")}'


        print(f"Processing now for model {model}, config {config_type}")

        for i, row in tqdm(df_top.iterrows(), total=len(df_top), desc="Processing rows"):
            reasoning_paths = row.reasoning_paths
            question = row.question

            try:
                if cfg["use_reasoning_paths"]:
                    prompt = cfg["template"].format(
                        reasoning_paths=reasoning_paths,
                        question=question
                    )
                else:
                    prompt = cfg["template"].format(
                        question=question
                    )

                content = build_content_for_row(i, row, prompt, cfg, dataset)

                completion = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": content
                        },
                    
                    ],
                    extra_body={
                        "reasoning": {
                            "effort": "none",
                            "exclude": True
                        }
                    }
                )

                answer = completion.choices[0].message.content
            except Exception as e:
                print(f"API error on row {i}, prompt_type={config_type}, model={model}: {e}")
                answer = None

            row_result = {
                "row_id": i,
                "prompt_type": config_type,
                "question": question,
                "reasoning_paths": reasoning_paths if cfg["use_reasoning_paths"] else None,
                "predicted": answer,
                "model": model,
                "dataset" : dataset
            }

            answers.append(row_result)

            pickle_path = os.path.join(
                save_dir,
                f"answer_row_{i}_{dataset}_{config_type}_{model.replace('/', '_')}.pkl"
            )
            os.makedirs(os.path.dirname(pickle_path), exist_ok=True)

            with open(pickle_path, "wb") as f:
                pickle.dump(row_result, f)

        os.makedirs("results", exist_ok=True)
        pd.DataFrame(answers).to_parquet(
            f"results/answers_{dataset}_{config_type}_{model.replace('/', '_')}.parquet"
        )

print(f"Processed {len(answers)} prompt runs and saved pickles in '{save_dir}'.")