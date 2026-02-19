# import time
# import requests
# import json
#
# from base_worker import run_worker
#
# def save_to_file(data, recipe_id, api_name, output_dir):
#     print(f" [x] Saving data to {output_dir}")
#     filename = f"{api_name}_{recipe_id}_{int(time.time())}.json"
#     filepath = output_dir / filename
#     with open(filepath, 'w') as f:
#         json.dump(data, f, indent=2)
#     print(f" [✓] Saved to {filepath}")
#
# def callback(ch, method, properties, body, output_dir):
#     print(f" [x] Received a message with api")
#     try:
#         message = json.loads(body)
#         api = message.get('api')
#         recipe_id = message.get('recipe_id')
#
#
#         # if api != 'foodish':
#         #     print(f" [!] Ignoring message with api={api}")
#         #     ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
#         #     return
#
#         print(f" [x] Foodish: processing recipe {recipe_id}")
#
#         response = requests.get('https://foodish-api.com/api/', timeout=10)
#         response.raise_for_status()
#         data = response.json()
#
#         save_to_file(data, recipe_id, 'foodish', output_dir)
#
#         ch.basic_ack(delivery_tag=method.delivery_tag)
#     except Exception as e:
#         print(f" [!] Error: {e}")
#         ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
#
#
# if __name__ == '__main__':
#     run_worker(callback)
