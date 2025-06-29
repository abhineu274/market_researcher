from crewai.llm import LLM
import os
import requests
import time

class AzureOpenAILLM(LLM):
    def __init__(self, api_key=None, api_base=None, api_version=None, deployment_name=None, model=None):
        self.api_key = api_key or os.getenv("AZURE_API_KEY")
        self.api_base = api_base or os.getenv("AZURE_API_BASE")
        self.api_version = api_version or os.getenv("AZURE_API_VERSION")
        self.deployment_name = deployment_name or os.getenv("AZURE_DEPLOYMENT_NAME")
        self.model = model or os.getenv("AZURE_MODEL")

    def call(self, prompt, **kwargs):
        url = f"{self.api_base}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }
        data = {
            "messages": prompt,
            "max_tokens": kwargs.get("max_tokens", 512),
            "temperature": kwargs.get("temperature", 0.7),
        }
        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    wait_time = 2 ** attempt
                    print(f"[RateLimit] 429 Too Many Requests. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise
        raise Exception("Failed after multiple retries due to rate limiting.")
