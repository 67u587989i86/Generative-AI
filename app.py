import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load .env
load_dotenv()
api_key = os.getenv("PERPLEXITY_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

def generate_answer(prompt, model="sonar-pro", temperature=0.7, max_tokens=500):
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a factual assistant with citations."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        answer = resp.choices[0].message.content
        # Optionally capture citations info
        return answer
    except Exception as e:
        st.error(f"API error: {e}")
        return None

def main():
    st.title("📚 Hello Ajay , I am your AI assistant")
    st.write("Generate real-time, citation-backed answers with Sonar Pro.")

    if "prompt" not in st.session_state:
        st.session_state.prompt = ""

    examples = ["What’s the capital of France?", "Latest news on AI regulation", "Explain quantum entanglement"]
    st.sidebar.title("💡 Examples")
    for ex in examples:
        if st.sidebar.button(ex):
            st.session_state.prompt = ex

    prompt = st.text_area("Your question:", key="prompt", height=150)
    temp = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.5)

    if st.button("Ask Perplexity"):
        if not prompt:
            st.warning("Please enter a prompt.")
            return
        if not api_key:
            st.error("Missing PERPLEXITY_API_KEY in .env")
            return

        with st.spinner("Fetching answer..."):
            answer = generate_answer(prompt, temperature=temp)
            if answer:
                st.subheader("Answer")
                st.markdown(answer)

if __name__ == "__main__":
    main()
