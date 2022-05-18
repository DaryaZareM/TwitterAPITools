import json
import numoy as np
import pandas as np

normalizer= lambda x:x.replace('\"','\";"').replace('\'','\"').replace('\";"','\'').replace(' False',' \"False\"').replace(' True',' \"True\"').replace(' None',' \"None\"')

def extended_link_extract(data):
    """extract all expended links in a tweet; whether in retweet or quoted or in tweet

    Args:
        data (pandas.DataFrame ): crawled data which must have columns entity, retweet_status, and quoted_status

    Returns:
        list : list with input data lengh, has all links of each tweet in a list (list of lists)
    """
  links=[]
  quoted_status = data['quoted_status'].notna()
  retweeted_status = data['retweeted_status'].notna()
  
  for i in range(len(data)):
    try:
      if quoted_status[i]:
        links.append([j['expanded_url'] for j in json.loads(normalizer(data.iloc[i]['quoted_status']))['entities']['urls']]+[j['expanded_url'] for j in json.loads(normalizer(data.iloc[i]['entities']))['urls']])
      elif retweeted_status[i]:
        links.append([j['expanded_url'] for j in json.loads(normalizer(data.iloc[i]['retweeted_status']))['entities']['urls']])
      else:
        links.append([j['expanded_url'] for j in json.loads(normalizer(data.iloc[i]['entities']))['urls']])
    except:
      # print(i)
      links.append([])
      pass
    
  data['links']=np.array(links)
  return np.array(links)
