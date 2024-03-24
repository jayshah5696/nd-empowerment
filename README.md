# nd-empowerment
Supporting NeuroDiversity Month

# Inspiration
Dyslexia is extremely common, 1 in 10 people are affected by it across the world. The outcomes are very isolating. It affects learning, social interactions, mood and overall life. Leading what is considered a 'normal' life can be difficult. Dyslexic individuals often benefit from personalized tutoring and care. Unfortunately, such care is not available at an affordable price and is out of reach for a majority. On the eve of neurodiversity appreciation month, we wanted to do our part by leveraging AI to democratize this personalized learning approach to anyone who needs it.

# What it does
The NeuroBuddy platform helps dyslexic individuals by becoming their personalized 'translation layer' to the outside world. User onboarding It does so by first understanding its user, their likes, dislikes, triggers etc. It uses this understanding to create an ever evolving translation layer for them.

## Learning platform

Our learning platform deploys an AI agent to fetch relevant information about the topic. It is represented in an easy to understand format using simple, non triggering words, ample audio / visual representations of the users liking.

## Journal

Users may have difficulty typing in 'grammatically correct spellings'. They might have difficulty putting their thoughts together to form coherent arguments. The journaling page helps them convert it into 'formal spelling' based structured journal entries.

## Web Extension

The web extension accompanies the user outside of our platform on the web.. Bringing our unique, personalized learning to the entire web. When approached by a daunting wall of text, the user can simply highlight the text, right click our extension to explain or visualize. In the backend, we will then breakdown the text into simple, easy to understand chunks, convert them into personally tailored visual and audio representations (for example if user mentioned they like dinosaurs from their onboarding, we will use dinosaurs to explain it).

# How we built it
We built it using most of the resources provided in the hackathon. APIs from FireworksAI, MistralAI Platforms like Streamlit

# Challenges we ran into
It was difficult to pick and choose what to implement since there were a lot of avenues to innovate. We spent a majority of the time trying to understand what would make the MVP.

# Accomplishments that we're proud of
We are proud of the basic idea of being able to democratize education for folks who might find it the most challenging.

# What we learned
It's difficult to learn as it is, dyslexia is also a spectrum, so personalized learning is required at all levels. Making something that aids that is crucial to help the 10% of the world population which is affected by it.

# What's next for NeuroBuddy
We look to deploy it and get more feedback and evolve the platform! We also plan to integrate feedback mechanisms in the bot which would help users revise the topics they have read in the session on a timely manner and send the materials they learnt through chatbot as emails/pdf for their future reference so they can link how they actually learnt the topic whenever they refer to the pdf.

# Built With
- mistral
- groq
- fireworks
- streamlit
- fastapi
- python


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
