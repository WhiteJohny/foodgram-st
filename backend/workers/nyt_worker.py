# import time
# import requests
# import json
# import os
#
# from base_worker import run_worker
#
# NYT_API_KEY = os.environ.get('NYT_API_KEY')
# if not NYT_API_KEY:
#     raise ValueError("NYT_API_KEY environment variable is required")
#
#
# def save_to_file(data, recipe_id, api_name, output_dir):
#     print(f" [x] Saving data to {output_dir}")
#     filename = f"{api_name}_{recipe_id}_{int(time.time())}.json"
#     filepath = output_dir / filename
#     with open(filepath, 'w') as f:
#         json.dump(data, f, indent=2)
#     print(f" [✓] Saved to {filepath}")
#
#
# def callback(ch, method, properties, body, output_dir):
#     print(f" [x] Received a message with api")
#     try:
#         message = json.loads(body)
#         api = message.get('api')
#         recipe_id = message.get('recipe_id')
#
#         # if api != 'nyt':
#         #     print(f" [!] Ignoring message with api={api}")
#         #     ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
#         #     return
#
#         print(f" [x] NYT: processing recipe {recipe_id}")
#
#         url = f"https://api.nytimes.com/svc/mostpopular/v2/shared/1/facebook.json?api-key={NYT_API_KEY}"
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         data = response.json()
#
#         save_to_file(data, recipe_id, 'nyt', output_dir)
#
#         ch.basic_ack(delivery_tag=method.delivery_tag)
#     except Exception as e:
#         print(f" [!] Error: {e}")
#         ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
#
#
# if __name__ == '__main__':
#     run_worker(callback)
