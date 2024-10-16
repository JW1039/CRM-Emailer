from openai import OpenAI
import time
import random
from dotenv import load_dotenv
import os

load_dotenv()

class ChatGPT():
    def __init__(self):
      API_KEY = os.getenv("OPENAI_KEY")
      self.client = OpenAI(api_key=API_KEY)
      self.retrieved = []

    def get(self, ownerName, busName, perMsg, userName):

      prompt = """Below is an example of our top performing email for generating leads for chiropractors and physiotherapists. Please create an email for a lead called {ownerName} from {busName} - the unique thing I would like to tie into the personal message is that {perMsg}. we don’t need a subject line, just the email body. Please make the personal message 2 sentences maximum and keep the email short, conversational and casual like the below email template. My name is {userName}.

      Hey {{firstName}}, 

      {{Personal Message}} 

      We've worked with chiropractic practices across Australia like Chiropractic life, healthplex, spinal studio and perth wellness and currently generate over 722 new patient appointments per month.

      This was all done with our tailored digital strategies.

      Are you free for a call this week? 

      Cheers,

      {{My Name}}""".format(ownerName=ownerName, busName=busName, perMsg=perMsg, userName=userName)


      completion = self.client.chat.completions.create(
          model="gpt-3.5-turbo-1106",
          messages=[
            {"role": "user", "content": prompt}
          ]
        )
      

      self.retrieved.append(completion.choices[0].message.content)
      return completion.choices[0].message.content

    # mock get a result
    def t_get(self, ownerName, busName, perMsg, userName):
       time.sleep(random.randint(1,3))
       return random.choice(["Hey Mark,\n\nI couldn't help but notice we both have a soft spot for Holden Commodores – they’re classics! Driving one has been an amazing ride for me, much like what I aim to provide in terms of service.\n\nWe've partnered with chiropractic practices across Australia such as Chiropractic Life, Healthplex, Spinal Studio, and Perth Wellness, and we're proud to say we're currently generating over 722 new patient appointments monthly.\n\nThis success is a result of our custom digital marketing strategies designed specifically for the chiropractic industry.\n\nGot some time for a quick chat this week?\n\nCheers,\n\nIsaac", "Hey Jeffrey,\n\nIt's always nice to meet another dog lover; I bet our four-legged friends could swap some great chase stories!\n\nWe've aided chiropractic operations across Australia, including Chiropractic Life, Healthplex, Spinal Studio, and Perth Wellness, bolstering their client base by over 722 new patient appointments each month thanks to our custom digital strategies.\n\nHow about taking some time for a quick chat this week?\n\nCheers,\n\nIsaac", "Hey Greg,\n\nI see you're serious about gym training. Which muscle group is your favourite to work out? I'm all about chest day.\n\nWe've partnered with chiropractic clinics nationwide - Chiropractic Life, Healthplex, Spinal Studio, and Perth Wellness, to name a few, driving over 722 new patient appointments every month through customized digital marketing strategies.\n\nFancy a chat this week to see how we can help Sydney Spine & Sports Clinic do the same?\n\nCheers,\n\nIsaac"])


    def end(self):
       self.client.close()



if __name__ == "__main__":

  chat = ChatGPT()
  results = [chat.get(ownerName="Mark Smith", busName="Marks Chiropracters", perMsg="we both drive Holden Commodores", userName="Steve"),
  chat.get(ownerName="Jeffrey Leonard", busName="Jeff the Chiropracter", perMsg="we both own dogs", userName="Steve"),
  chat.get(ownerName="Greg Sher", busName="Sydney Spine & Sports Clinic ", perMsg="likes 'training at the gym' whats your favorite muscle group to work, mines chest", userName="Steve")]

  print(results)