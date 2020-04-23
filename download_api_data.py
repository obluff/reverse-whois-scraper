import requests
import pandas as pd

### CHANGEME
api_key = None
pages_to_parse = 10
output_filename = "reverse_whois_output.csv"
keyword="lockdown"

link = "http://api.whoxy.com/?key={}reverse=whois&keyword={}&mode=mini&format=json&page={}"


json_objects = []
for i in range(pages_to_parse):

    request_link = link.format(api_key, keyword, str(i))
    reverse_whois = requests.get(request_link)

    #handling edge case where request fails
    if not reverse_whois.ok:
        print("Request to ", request_link, "Failed")
        print("Shutting down")
        break

    downloaded_json = reverse_whois.json()

    #checking if request was successful, but we have an issue with our parameters
    if downloaded_json['status'] == 0:
        print("Request was successful, but failed because of the following status reason")
        print(downloaded_json["status_reason"])
        break
    json_objects += downloaded_json['search_result']

    print("Request to page", i, "was successful")
    print("Current number of records downloaded", len(json_objects))


print("Writing to", output_filename)

pd.DataFrame \
  .from_dict(json_objects) \
  .to_csv(output_filename)



