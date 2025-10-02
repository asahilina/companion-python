#!/bin/bash

# --- Function for error handling ---
handle_error() {
  echo "Error: $1"
  exit 1
}

# --- Part 1: Set Google Cloud Project ID ---
API_KEY_FILE="$HOME/api_key.txt"
echo "--- Setting AI Studio API Key File ---"

read -p "Please enter your AI Studio API Key: " user_api_key

if [[ -z "$user_api_key" ]]; then
  handle_error "No API KEY was entered."
fi

echo "You entered: $user_api_key"
echo "$user_api_key" > "$API_KEY_FILE"

if [[ $? -ne 0 ]]; then
  handle_error "Failed saving your API KEY: $user_api_key."
fi
echo "Successfully saved API KEY."



echo "--- Setup complete ---"
exit 0