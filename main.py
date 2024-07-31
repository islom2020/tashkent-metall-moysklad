from flask import Flask, request, jsonify

import webhook_moysklad.moysklad_api

app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        order_id = data['events'][0]['meta']['href'].split('/')[-1]

        # Process the webhook data here
        print("Received webhook data:", data)

        size = webhook_moysklad.moysklad_api.get_customer_orders_size()
        print(size)

        webhook_moysklad.moysklad_api.update_customer_order_check_number_by_id(order_id, size)

        # Respond with a success message
        return jsonify({"message": "Webhook received successfully"}), 200
    else:
        return jsonify({"message": "Method not allowed"}), 405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    #test comment
