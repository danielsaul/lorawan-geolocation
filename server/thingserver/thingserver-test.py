import requests
import json


def main():
    url = "http://localhost:4000/jsonrpc"
    headers = {'content-type': 'application/json'}

    # Example echo method
    payload = {
            "method": "downlink",
            "params": {
              "dev_eui": "0123456789abcdef",
              "dev_addr": "0a1b2c3d",
              "rx_time": 1435923301.123542,
              "counter_up": 10,
              "port": 2,
              "encrypted_payload": "DS4CGaDCdG+48eJNM3Vai-zDpsR71Pn9CPA9uCON84",
              "radio": {
                "gw_addr": "70b3d54b10080100",
                "gw_gps": {
                  "lat": 59.936009,
                  "lon": 30.065817,
                  "alt": 145
                },
                "stat": 1,
                "modu": "LORA",
                "chan": 2,
                "datr": "SF12BW125",
                "tmst": 2362035980,
                "codr": "4/5",
                "rfch": 0,
                "lsnr": 8.8,
                "rssi": -103,
                "freq": 868.5,
                "size": 29
              }
            },
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    print response
    #assert response["result"] == "echome!"
    #assert response["jsonrpc"]
    #assert response["id"] == 0

if __name__ == "__main__":
    main()
