from mongoengine import *
import os
import datetime


# DB_URI = os.environ.get("Database_string")
# DB_URI = "mongodb+srv://stack:stackCoredevs.21@cluster0.qsmsc.mongodb.net/stack"
connect(host=DB_URI)
try:
    class Records(Document):
        owner = ObjectIdField(required=True)
        size = StringField(required=True)
        climateControl = BooleanField(default=False, required=True)
        price = FloatField(required=True)
        date = DateTimeField(default=datetime.datetime.utcnow)


    def push_records(_id, size, climate_control, price, ):

        all_records = Records(owner=_id,
                              size=size,
                              climateControl=climate_control,
                              price=price

                              )

        all_records.save()


    class Links(Document):
        link = StringField(required=True)
        websiteName = StringField()
        location = StringField()
        createdAt = DateTimeField(default=datetime.datetime.utcnow)


    def push_links(link, website_name):

        all_links = Links(link=link,
                          websiteName=website_name
                          )

        all_links.save()
    # push_links("https://www.publicstorage.com/self-storage-fl-miami/478?sp=478|13|miami|25.76168|-80.19179|0|0|0",
    #            "www.publicstorage.com")

except Exception as e:
    print(e)
