import aylien_news_api
from aylien_news_api.rest import ApiException
import os
import sys

AYLIEN_ID = os.environ.get('AYLIEN_NEWSAPI_ID')
AYLIEN_KEY = os.environ.get('AYLIEN_NEWSAPI_KEY')
MAX_PAGECOUNT = 1

# Configure API key authorization: app_id
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = AYLIEN_ID
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = AYLIEN_KEY
# create an instance of the API class
aylien = aylien_news_api.DefaultApi()

filename = sys.argv[1]
f = open(filename, 'r')

for line in f:
    term = '\"' + line.rstrip() + '\"'
    sort_by = 'relevance'
    language = ['en']
    since = 'NOW-1DAY'
    until = 'NOW'
    # entities = [
    #   'http://dbpedia.org/resource/Donald_Trump',
    #   'http://dbpedia.org/resource/Hillary_Rodham_Clinton'
    # ]
    per_page = 10
    cursor = '*'
    pagecount = 0

    while pagecount < MAX_PAGECOUNT:
        try:
            # List stories
            api_response = aylien.list_stories(
                    text=term,
                    language=language,
                    published_at_start=since,
                    published_at_end=until,
                    per_page=per_page,
                    cursor=cursor
                    # entities_body_links_dbpedia=entities,
                    # sort_by=sort_by
                    )
            for story in api_response.stories:
                print('TITLE: ' + story.title)
                # print(story.body)
                print('SUMMARY: ')
                for sentence in story.summary.sentences:
                    print(sentence)
                print('SOURCE: ' + story.source.domain)
                print('AUTHOR: ' + story.author.name)
                entities = [entity.text for entity in story.entities.body]
                print('ENTITIES: ')
                print(entities)
                print(story.links.permalink)
                print(' ')
                print(' ')
            cursor = api_response.next_page_cursor
            if len(api_response.stories) < per_page:
                break
            print(cursor)
            pagecount += 1
        except ApiException as e:
            print("Exception when calling DefaultApi->list_stories: %s\n" % e)

