class ddb_bot:
  # Global class variables
  EXCEPTIONS={}
  EXCEPTIONS['NO_BOT_TOKEN']='No Slack Bot Token'
  EXCEPTIONS['CONNECTION_FAILED']='Connection to slack failed'
  
  # delay between polling action
  RTM_READ_DELAY=.03 
  RTM_FAIL_TIMEOUT=1
  RTM_MAX_FAILS=10

  def __init__(self):
    #check for BOT API token
    try:
      SLACK_BOT_TOKEN= os.environ["SLACK_BOT_TOKEN"]
    except:
      raise Exception(ddb_bot.EXCEPTIONS['NO_BOT_TOKEN'])
    
    try:
      self.DDB_CONFIG=os.environ["DDB_CONFIG"]
    except:
      self.DDB_CONFIG=None
      pass
    
    #Chgeck for proxies
    SLACK_PROXIES=None
    try:
      SLACK_HTTP_PROXY=os.environ["SLACK_HTTP_PROXY"]
      SLACK_HTTPS_PROXY=os.environ["SLACK_HTTPS_PROXY"]
      SLACK_PROXIES={'http':SLACK_HTTP_PROXY,'https':SLACK_HTTPS_PROXY}
    except:
      pass
    # init connection with RTM
    self.slack_client= SlackClient(SLACK_BOT_TOKEN,proxies=SLACK_PROXIES)

  def is_direct_message(self,msg):
    if 'channel' in msg:
      if msg['channel']:
        # its a direct message with the bot
        if msg['channel'][0]=='D':
          return True
    return None

  def is_mesage_to(self,msg):
    if 'text' in msg:
      if msg['text']!=None:
        if msg['text'].find("<@{0}>".format(self.bot_id))>-1:
          return True
    return None
  
  def return_my_message(self,msg):
      pre,post=msg['text'].split("<@{0}>".format(self.bot_id))
      return post

  def ddb_query(self,msg):
    print("Preforming query:{0}".format(msg))
    # declare engine    
    e=engine(config=self.DDB_CONFIG)
    # run query
    results=e.query(msg)
    # format results
    output_factory(results,output=e.system['OUTPUT_MODULE'],output_style=e.system['OUTPUT_STYLE'],output_file=None)

  def go(self):
    fails=0
    while True:
      if self.slack_client.rtm_connect(with_team_state=False):
        # clear out the fail counter
        fails=0
        self.bot_id = self.slack_client.api_call("auth.test")["user_id"]
        logging.log(20,"ddb-bot-id: {0}".format(self.bot_id))
        while True:
          rtm_res=self.slack_client.rtm_read()
          for msg in rtm_res:
            if 'type' in msg:
              if self.is_mesage_to(msg):
                self.ddb_query(msg)
              elif self.is_direct_message(msg):
                self.ddb_query(msg)
              
              if msg['type']=='message':
                if 'text' in msg:
                  print(msg['text'])
            #print msg
            
          # out of for loop
          time.sleep(ddb_bot.RTM_READ_DELAY)
      else:
         time.sleep(ddb_bot.RTM_FAIL_TIMEOUT)
         fails+=1
         if fails>=ddb_bot.RTM_MAX_FAILS:
            raise Exception(ddb_bot.EXCEPTIONS['CONNECTION_FAILED'])

