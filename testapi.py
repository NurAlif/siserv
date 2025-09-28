import gemini_api_client
import json

def run_example():
    """
    An example function to demonstrate how to use the gemini_api_client package.
    """
    print("--- Querying Local Gemini API ---")
    
    # 1. Define your prompt and choose a model.
    #    The model constants are conveniently available from the package.
    sample_prompt = (
        "Explain the theory of relativity in simple terms. "
        "Structure the response as a JSON object with two keys: 'summary' and 'key_concepts', "
        "where key_concepts is a list of strings."
    )
    model_to_use = gemini_api_client.MODEL_FLASH

    # 2. Call the main function from the package.
    #    This handles the request, parsing, and all retries.
    json_response = gemini_api_client.query_api_with_retries(
        prompt=sample_prompt, 
        model=model_to_use
    )
    print(json_response)

    # 3. Process the result.
    if json_response:
        print("\n✅ API Response Received Successfully:")
        # Use json.dumps to pretty-print the dictionary
        print(json.dumps(json_response, indent=2))
    else:
        print("\n❌ Failed to get a valid response from the API after multiple attempts.")


if __name__ == "__main__":
    run_example()
