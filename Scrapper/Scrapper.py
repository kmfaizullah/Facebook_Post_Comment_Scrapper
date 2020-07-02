import requests
from bs4 import BeautifulSoup
from LoginSecret import username, password
import pandas as pd

class Scrapper: 
  
    """
        This is peramiterized constructor.
        It will take content url while creating object.
        args: url
    """ 
    def __init__(self, url): 
        self.url = url
        
    def parse_data(self, post_url):
        
        """
            This method is for creating session providing facebook credentials.
            This method will take a post url by ushich url html data will be persed and returned.
            args: post_url
            return: parsed html data.
        """
        login_basic_url = 'https://mbasic.facebook.com/login'
        login_details = {
                'email': username,
                'pass': password
            }
        with requests.Session() as session:
            post = session.post(login_basic_url, data=login_details)
            parsed_data = session.get(post_url)
        return parsed_data 
  
    def find_comment(self, content_url): 
        """
            This method is for finding scrapping person name and comment from a facebook page.
            Beautiful Soup library has been used to searched the desired person and comment from the bunch of parsed data.
            The class name, by which this method will find the dised item has been selected by inspecting facebook page.
            The searching properties may very from one page to another page.
            args: content_url
            return: Person name and their corresponsind comment as python list.
        """
        comment=[]
        person=[]
        soup = BeautifulSoup(self.parse_data(content_url).content, "html.parser")
        r=soup.select(".cr.y")
        for y in r:
            person.append(y.text)

        result=soup.select(".cs")
        for res in result:
            comment.append(res.text)
        return person, comment 

    def data_Csv_save(self):
        
        """
            This method is for preparing and exportinf data.
            Data will be saved as a CSV file.
        """
        Person, Comment = self.find_comment(self.url)
        Person_df = pd.DataFrame(Person,columns= ['Person'])
        Comment_df = pd.DataFrame(Comment,columns= ['Comments'])
        format_data=pd.concat([Person_df, Comment_df], axis=1)
        format_data.to_csv('Facebook_post_comment.csv',index=False)
        
#facebook post url        
URL = f'https://mbasic.facebook.com/story.php?story_fbid=3109006692521637&id=1030915846997409&refid=17&_ft_=mf_story_key.3109006692521637%3Atop_level_post_id.3109006692521637%3Atl_objid.3109006692521637%3Acontent_owner_id_new.1030915846997409%3Athrowback_story_fbid.3109006692521637%3Apage_id.1030915846997409%3Astory_location.4%3Atds_flgs.3%3Apage_insights.%7B%221030915846997409%22%3A%7B%22page_id%22%3A1030915846997409%2C%22page_id_type%22%3A%22page%22%2C%22actor_id%22%3A1030915846997409%2C%22dm%22%3A%7B%22isShare%22%3A0%2C%22originalPostOwnerID%22%3A0%7D%2C%22psn%22%3A%22EntStatusCreationStory%22%2C%22post_context%22%3A%7B%22object_fbtype%22%3A266%2C%22publish_time%22%3A1593674858%2C%22story_name%22%3A%22EntStatusCreationStory%22%2C%22story_fbid%22%3A%5B3109006692521637%5D%7D%2C%22role%22%3A1%2C%22sl%22%3A4%2C%22targets%22%3A%5B%7B%22actor_id%22%3A1030915846997409%2C%22page_id%22%3A1030915846997409%2C%22post_id%22%3A3109006692521637%2C%22role%22%3A1%2C%22share_id%22%3A0%7D%5D%7D%7D%3Athid.1030915846997409%3A306061129499414%3A2%3A0%3A1596265199%3A4197325281738412762&__tn__=%2AW-R'

Scrap = Scrapper(URL) # creating Scrapper object
Scrap.data_Csv_save() #calling method using object to scrap and save data.