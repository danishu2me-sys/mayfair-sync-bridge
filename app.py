import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

OFFICIAL_SERVER = "https://mayfair.sndpro.app:1132"
captured_orders = []


@app.route(
    "/ConfigAPI/api/Configuration/GetConfiguration", methods=["GET", "POST"]
)
def relay_config():
  target = f"{OFFICIAL_SERVER}/ConfigAPI/api/Configuration/GetConfiguration"
  headers = {k: v for k, v in request.headers if k.lower() != "host"}
  resp = requests.request(
      method=request.method,
      url=target,
      headers=headers,
      data=request.get_data(),
      verify=False,
  )
  return (resp.content, resp.status_code, resp.headers.items())


@app.route("/Mayfair/<path:subpath>", methods=["GET", "POST", "PUT"])
def relay_sync(subpath):
  target = f"{OFFICIAL_SERVER}/Mayfair/{subpath}"

  if request.method == "POST":
    try:
      raw_body = request.get_data().decode("utf-8", errors="ignore")
      captured_orders.append({"path": subpath, "payload": raw_body})
    except Exception as e:
      print("Error:", e)

  headers = {k: v for k, v in request.headers if k.lower() != "host"}
  resp = requests.request(
      method=request.method,
      url=target,
      headers=headers,
      data=request.get_data(),
      verify=False,
  )
  return (resp.content, resp.status_code, resp.headers.items())


@app.route("/api/get-all-orders", methods=["GET"])
def get_orders():
  return jsonify({"success": True, "orders": captured_orders})


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
