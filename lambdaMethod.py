import json
import boto3

def lambda_handler(event, context):
    text = event['text']
    client = boto3.client('bedrock-runtime')  # Assuming bedrock-runtime is the correct client name
    
    prompt = f"Your task is to retrieve the software requirements in this software specification file, ignore titles and table of contents. Don't mention them, just the requirements, one after another without restructuring. There is 87 requirements to find. {text}"

    response = client.invoke_model(
        modelId='chatgpt-3.5',  # Adjust this to the actual model ID for ChatGPT 3.5
        inputText=prompt,
        maxTokens=2048,
        temperature=0.7
    )
    
    generated_text = response['outputText']
    requirements = generated_text.split('\n')
    
    return {
        'statusCode': 200,
        'body': json.dumps([req.strip() for req in requirements if req.strip()])
    }
