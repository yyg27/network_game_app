import requests

def get_wiki(topic):
    try:
        formatted_topic = topic.replace(" ", "_");
        
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_topic}"

        ##for introducing our script to wikipedia api to bypass 403 forbidden status code
        headers = {
            'User-Agent': 'wiki_fetcher/1.0'
        }

        print(f"Searching for '{topic}'...");
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:

            data = response.json();
            
            title = data.get('title');
            summary = data.get('extract'); ##to get summary
            
            print(f"\n### {title} ###\n");
            print(summary);
        else:
            print("Topic not found!!!");

    except Exception as e:
        print(f"Error: {e}");

if __name__ == "__main__":
    topic_input = input("Would you kindly enter a topic: ");
    if topic_input:
        get_wiki(topic_input);
    else:
        print("Please enter a topic.");