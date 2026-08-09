import argparse
import json
from pathlib import Path
from bs4 import BeautifulSoup
from jsonschema import validate, ValidationError

# Define the schema for the configuration file
CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "selectors": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the data field"},
                    "selector": {"type": "string", "description": "CSS or XPath selector"},
                    "type": {"type": "string", "enum": ["text", "html", "attribute"], "default": "text"},
                    "attribute": {"type": "string", "description": "Attribute name if type is 'attribute'"},
                    "multiple": {"type": "boolean", "default": False, "description": "Whether to extract multiple elements"},
                    "strip_whitespace": {"type": "boolean", "default": True, "description": "Strip leading/trailing whitespace"},
                    "default": {"description": "Default value if selector finds nothing"}
                },
                "required": ["name", "selector"],
                "additionalProperties": False
            }
        },
        "remove_selectors": {
            "type": "array",
            "items": {"type": "string"},
            "description": "CSS or XPath selectors for elements to remove before extraction"
        }
    },
    "additionalProperties": False
}

def load_config(config_path: Path) -> dict:
    """Loads and validates the configuration from a JSON file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    try:
        validate(instance=config, schema=CONFIG_SCHEMA)
    except ValidationError as e:
        raise ValueError(f"Configuration validation error: {e.message} at path {e.path}") from e
    return config

def extract_data(html_content: str, config: dict) -> dict:
    """
    Extracts structured data from HTML content based on the provided configuration.
    """
    soup = BeautifulSoup(html_content, 'lxml') # Use lxml for better XPath support

    # 1. Remove unwanted elements first
    for selector in config.get('remove_selectors', []):
        for tag in soup.select(selector):
            tag.decompose()

    # 2. Extract data based on selectors
    extracted_data = {}
    for item_config in config.get('selectors', []):
        name = item_config['name']
        selector = item_config['selector']
        extract_type = item_config.get('type', 'text')
        attribute = item_config.get('attribute')
        multiple = item_config.get('multiple', False)
        strip_whitespace = item_config.get('strip_whitespace', True)
        default_value = item_config.get('default')

        try:
            elements = soup.select(selector)

            if multiple:
                values = []
                for el in elements:
                    if extract_type == 'text':
                        val = el.get_text()
                    elif extract_type == 'html':
                        val = str(el)
                    elif extract_type == 'attribute' and attribute:
                        val = el.get(attribute)
                    else:
                        val = None # Should not happen with schema validation

                    if val is not None and strip_whitespace:
                        val = val.strip()
                    if val is not None:
                        values.append(val)
                extracted_data[name] = values if values else default_value
            else:
                if elements:
                    el = elements[0]
                    if extract_type == 'text':
                        val = el.get_text()
                    elif extract_type == 'html':
                        val = str(el)
                    elif extract_type == 'attribute' and attribute:
                        val = el.get(attribute)
                    else:
                        val = None

                    if val is not None and strip_whitespace:
                        val = val.strip()
                    extracted_data[name] = val if val is not None else default_value
                else:
                    extracted_data[name] = default_value
        except Exception as e:
            print(f"Warning: Could not extract '{name}' with selector '{selector}': {e}")
            extracted_data[name] = default_value # Assign default on error too

    return extracted_data

def main():
    parser = argparse.ArgumentParser(
        description="Clean and extract structured data from web pages using CSS/XPath selectors."
    )
    parser.add_argument(
        "-u", "--url",
        help="Path to the HTML file to process (local file only for this prototype).",
        required=True
    )
    parser.add_argument(
        "-c", "--config",
        help="Path to the JSON configuration file with selectors.",
        required=True
    )
    args = parser.parse_args()

    html_path = Path(args.url)
    config_path = Path(args.config)

    if not html_path.exists():
        print(f"Error: HTML file not found at {html_path}")
        exit(1)
    if not config_path.exists():
        print(f"Error: Config file not found at {config_path}")
        exit(1)

    try:
        config = load_config(config_path)
    except ValueError as e:
        print(f"Error loading configuration: {e}")
        exit(1)

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    extracted_data = extract_data(html_content, config)
    print(json.dumps(extracted_data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
