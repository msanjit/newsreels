
# coding: utf-8

# In[1]:


import os
import sys
from flask import request
from flask import Flask
from flask import jsonify


# In[2]:


scriptpath = "../refinitiv.py"
# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))
# Do the import
import refinitiv


# In[3]:


app=Flask(__name__)


# In[4]:


@app.route('/tagger_service_endpoint', methods=['POST']) 
def tagger_service_endpoint(url="https://api.thomsonreuters.com/permid/calais",api_key="1tuJRbkEEOJ5SyERevb9pk5oDDVjQ4AQ"):
    req_data=request.data
    return jsonify(refinitiv.tag(url,api_key,req_data,headType="text/raw"))


# In[5]:


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

