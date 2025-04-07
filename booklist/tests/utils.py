def validate_response_keys(response, keys):
    for key in keys:
        assert key in response.data, f"Missing key: {key}"
