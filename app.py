import json

import streamlit as st
from cloudflare import Cloudflare

"# Comically Bad Art Generation"

# Set Cloudflare API key from Streamlit secrets
client = Cloudflare(api_token=st.secrets["CLOUDFLARE_API_TOKEN"])


art_style = st.text_input("Art style", placeholder="Oil painting")
description = st.text_input("Description", placeholder="A sunset over a mountain")

if art_style and description:
    st.write(f"Generating prompt for {description} in the style of {art_style}...")
    with st.chat_message("assistant"):
        with client.workers.ai.with_streaming_response.run(
            account_id=st.secrets["CLOUDFLARE_ACCOUNT_ID"],
            model_name="@cf/meta/llama-3-8b-instruct",
            messages=[
                {
                    "role": "system",
                    "content": """
                 You are generator of Stable Diffusion prompts.
                 
                 The user is going to provide you with an art style and a description.
                 
                 You task is to create an SD prompt that will make the most comically bad version of what they asked for.
                 
                 Be creative with your prompt and try to make the art look as bad or strange as you can.
                 
                 Incorporate common adjectives from reviews of what makes art bad in the prompt.
                 
                 Keep it succinct and follow the stable diffusion pattern of being separated by commas.
                 
                 Ensure to include the art style and description in the beginning of the prompt.
                 
                 Return only the Stable Diffusion prompt. 
                 """,
                },
                {"role": "user", "content": f"A {art_style} of {description}"},
            ],
            stream=True,
        ) as response:
            # The response is an EventSource object that looks like so
            # data: {"response": "Hello "}
            # data: {"response": ", "}
            # data: {"response": "World!"}
            # data: [DONE]
            # Create a token iterator
            def iter_tokens(r):
                for line in r.iter_lines():
                    if line.startswith("data: ") and not line.endswith("[DONE]"):
                        entry = json.loads(line.replace("data: ", ""))
                        yield entry["response"]

            completion = st.write_stream(iter_tokens(response))
    with st.chat_message("assistant"):
        st.write("Generating image...")
        response = client.workers.ai.with_raw_response.run(
            "@cf/bytedance/stable-diffusion-xl-lightning",
            account_id=st.secrets["CLOUDFLARE_ACCOUNT_ID"],
            prompt=completion,
        )
        st.image(response.read(), caption=completion)
