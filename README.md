# Graph Visualizations in Prompts for Knowledge Graph Question Answering

This repository accompanies the paper:

> **Graph Visualizations in Prompts for Knowledge Graph Question Answering**

It contains the code required to reproduce the experiments comparing text-only
and graph-visualization-augmented prompting for knowledge graph question
answering (KGQA).


## Dataset

The evaluation dataset is hosted separately on Zenodo:

> **https://zenodo.org/records/21620848**

Download the dataset archive, extract it, and place the file below in the
repository root:

```text
df_kgqa.pkl
```

The resulting directory should have the following structure:

```text
.
├── df_kgqa.pkl
├── main.py
├── prompt_config.py
├── render_helper.py
├── graph_image_gen.py
└── requirements.txt
└── README.md
```

The dataset contains KGQA questions, answers, retrieved reasoning paths, and
their corresponding KG triples.

## Installation

The code requires Python 3.10+ and a local installation of
[Graphviz](https://graphviz.org/download/).

```bash
pip install -r requirements.txt
```

Install Graphviz separately, for example:

```bash
# Ubuntu / Debian
sudo apt-get install graphviz

# macOS
brew install graphviz
```

## Model API configuration

The experiments use an OpenAI-compatible API interface. To reproduce the
experiments, reviewers must provide their own API key, API base URL, and model
identifiers.

In `main.py`, configure the following values:

```python
api_key = "YOUR_API_KEY"
llm_base_url = "YOUR_API_BASE_URL"

client = OpenAI(
    api_key=api_key,
    base_url=llm_base_url,
)

models = [
    "MODEL_IDENTIFIER_1",
    "MODEL_IDENTIFIER_2",
]
```

For security, we recommend storing the key as an environment variable:

```bash
export LLM_API_KEY="your-api-key"
```

and loading it in `main.py`:

```python
api_key = os.environ["LLM_API_KEY"]
```

The original experiments were run with an OpenRouter-compatible API endpoint.
Reproduction with another provider is possible if it supports the OpenAI chat
completions API and image inputs.

## Running experiments

1. Download `df_kgqa.pkl` from the Zenodo record above and place it in the
   repository root.
2. Install Python dependencies and Graphviz.
3. Configure an API key, base URL, and one or more multimodal model identifiers
   in `main.py`.
4. Select the desired prompt conditions in `prompt_config.py`.
5. Run:

```bash
python main.py
```



## Experimental conditions

The prompt configurations are specified in `prompt_config.py`:

- **Text-only:** retrieved reasoning paths are provided as text.
- **Text-plus-image:** reasoning paths are provided together with a graph image
  generated from the same retrieved triples.
- **Image-only:** only the graph image is provided.
- **Non-hierarchical layout:** Graphviz force-directed rendering ablation.
- **NetworkX layout:** spring-layout rendering ablation.
- **Reasoning-path images:** each reasoning path is rendered as a separate
  graph image.

Uncomment the relevant entries in `prompt_configs` to enable a condition.

## Outputs

During execution, the code creates:

```text
pngs/              # Graph images for full retrieved contexts
pngs_rps/          # Graph images for individual reasoning paths
answers_pickles/   # Per-instance raw predictions
results/           # Aggregated predictions in Parquet format
```

## Main files

| File | Purpose |
|---|---|
| `main.py` | Loads data, executes prompt configurations, calls model APIs, and saves predictions |
| `prompt_config.py` | Defines prompt templates and experimental conditions |
| `render_helper.py` | Builds multimodal messages and encodes rendered images |
| `graph_image_gen.py` | Generates hierarchical, non-hierarchical, and NetworkX graph images |
| `requirements.txt` | Python dependencies |

## Reproducibility notes

Exact numerical replication may vary because experiments rely on externally
hosted models whose versions and behavior can change over time. For the closest
reproduction, use the same dataset, prompt configurations, graph-rendering
settings, model identifiers, and API provider. The provided code renders
hierarchical Graphviz diagrams by default and supports alternative visual
layouts through the ablation settings. 
## License

This repository is provided solely for double-blind review. A license and
long-term code release details will be added after the review process.