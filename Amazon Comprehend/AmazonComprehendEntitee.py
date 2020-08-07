import boto3
import json

comprehend = boto3.client(service_name='comprehend', region_name='eu-central-1')

text = "Amazon.com, Inc. is located in Seattle, WA and was founded July 5th, 1994 by Jeff Bezos, allowing customers to buy everything from books to blenders. Seattle is north of Portland and south of Vancouver, BC. Other notable Seattle - based companies are Starbucks and Boeing."

print('Calling DetectKeyPhrases')
print(json.dumps(comprehend.detect_entities(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
print('End of DetectKeyPhrases\n')