# nd-empowerment
Support NeuroDiversity Month


# Installation Guide

create conda environemt
```
conda create -n nd python=3.11 -y
```

### install req.txt

```
pip install -r requierments.txt
```

### Copy .env_example as .env and fill the values
```
cp utils/.env_example utils/.env
```


##### list of LLMs available

- mistral/mistral-tiny-latest
- mistral/mistral-small-latest
- mistral/mistral-medium-latest
- mistral/mistral-large-latest
- groq/llama2-70b-4096
- groq/mixtral-8x7b-32768
- groq/gemma-7b-it