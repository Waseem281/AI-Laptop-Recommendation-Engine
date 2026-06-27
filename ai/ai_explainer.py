from ai.groq_client import client
from config import MODEL_NAME


def explain_recommendation(product, user_query):

    prompt = f"""
You are an AI Laptop Recommendation Assistant.

User searched:

{user_query}

Laptop Details

Brand: {product['brand']}
Model: {product['name']}
Processor: {product['processor_brand']} {product['processor']}
RAM: {product['ram']} GB
Storage: {product['memory_size']} GB
GPU: {product['gpu_brand']} {product['gpu_type']}
Price: ₹{product['price']}
Rating: {product['rating']}

Explain in 2-3 simple sentences why this laptop is recommended.

Do not use bullet points.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.3,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content