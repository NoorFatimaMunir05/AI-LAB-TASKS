# Lab 6: NLP fundamentals, chunking and evidence retrieval

Student: Noor Fatima Munir, Roll No 034, Section BSAI 3A

These are synthetic teaching documents, not actual university regulations. Use Python 3.10 or newer. No paid API or GPU is needed. The pretrained `sentence-transformers/all-MiniLM-L6-v2` encoder must be downloaded over the internet on its first run. Do not upload the model cache, virtual environment, secrets or private data.

## Installation

`python -m venv .venv`

Activate the environment, then run `python -m pip install -r requirements.txt`.

## Instructor scenario and guided scripts

Run these from this folder:

- `python lab6_search.py` (shared helper; no output by itself)
- `python scenario1_handbook.py`
- `python scenario2_support.py`
- `python scenario3_docs.py`
- `python scenario4_workplace.py`
- `python scenario5_equipment.py`
- `python guided_tokens.py`
- `python guided_embeddings.py`
- `python guided_chunks.py`
- `python guided_limits.py`
- `python guided_metrics.py`
- `python guided_chatbot.py --backend tfidf`
- `python guided_chatbot.py --backend embedding`
- `python guided_suggestions.py --backend embedding --query "forgot login"`

## Task 1

`python task1_tokens.py`

`python task1_chatbot_check.py`

For the interactive chatbot, test the exact question, a paraphrase, an empty input and an unrelated question using `guided_chatbot.py`.

## Task 2

`python create_dataset.py`

`python task2_chunks.py`

`python task2_semantic_check.py`

## Task 3

`python task3_retrieval.py --backend both`

This exports `retrieval_log.csv` and `retrieval_summary.json`. Development queries are used to choose the method; held-out labels are not consulted for selection. Both sparse TF-IDF and real sentence embeddings are compared for all three chunk strategies when the encoder is installed.

`python document_chatbot.py`

This assistant displays source offsets and only presents confirmed evidence. An unrelated query must not cause an automatic asserted policy answer.

## Recorded limitations

If model download or package installation fails, lexical exercises can still run using `--backend tfidf`. Missing embedding results must be reported as not run. The CSV shipped with this package comes from an actually executed TF-IDF run in the current environment; it does not pretend to contain embedding scores. After installing the model, rerun the full experiment and update the Word report with the genuine six-configuration numbers before final submission.

The corpus and queries are synthetic and stored in `corpus.json` and `queries.json`. This package does not contain private student or university data.
