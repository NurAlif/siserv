You will help me to create a application for me (front end part, i have done the backend part). It is a simple journaling app but enhanched with AI for english learning as foreign language. The application consist of 2 parts. The dashboard which holds list of previous journal records. And  journal writer which is a view to create or modify journal records.

analyze my request carefullly make sure it is complete, I can give you more information on the details of the app.

Plan in step by step to create the app, create the code in step by step, I will implement it also in step by step coppying the code. First create the code structure and setup the enviroment. 

Do it in step by step carefully slowly but surely


You will help me to create a fastapi application for me. It is a simple journaling app but enhanched with AI for english learning as foreign language. The application consist of 2 parts. The dashboard which holds list of previous journal records. And  journal writer which is a view to create or modify journal records.

analyze my request carefullly make sure it is complete, I can give you more information on the details of the app.

Plan in step by step to create the app, create the code in step by step, I will implement it also in step by step coppying the code. First create the code structure and setup the enviroment. 

ADD TRANSLATOR IN CASE THE USER FORGET THE ENGLISH WORD OR DO NOT KNOW.


Do it in step by step carefully slowly but surely

The journal writing is done in 2 step:
1. Scaffolding -> creating outlines on what to write.
2. Writing -> rough writing create the actual detailed writing but no need to be so perfect, just make sure the substansial is coherent, make sense, and include all the details and ideas of user.
3. Editing/Finishing -> perfecting the writing, grammar, word choice, etc.


The chat mode will be used to scaffold or find topics for actual journal writing.

We will mainly edit the journal creation window.
I need to make the editor/writer is like writing but guided by AI.

I will make the writing mechanism more comprehensive for journal writing.

The first time user open the writing view. There are some questions and a text field as a place holder. This will be a scaffolding for the writing, making the user easier. 
These questions are general like "what do you do today?" "what new or what unique today" to personalized based with previous journals (see user habits or activities). After some questions likely 2-3 questions, there is a button to chat with an AI to find and dig topics for journal writing (it will be switched to chat mode).

The user can choose to answer the questions or dirrectly chat to AI to dig some topics, or dirrectly write by their own based on their ideas or topic that they wanted in the writing field.


To implement this, there will be a phase buttons, phase 1-2-3, from scaffolding to finishing. There are specific AI behaviors at each phase to guide user for great journal writing. 


## Phase 1:
User can choose to write the outlines manualy, by answering questions, or by chatting with AI. THe behavior of the AI is to provide inspirations, find good and substantial topics for journal writing. help to dig or explore topics to write. User would need to answer it shortly no need too detail, or just the main points. 
User can choose to finish the first phase by asking the AI or AI can decide if the topics is enough.

## Phase 2:
The behavior of the AI is just standby until the user hit "get feedback" button or "Switch to chat mode to ask for something".  
For second phase user will decide if the writing is enough, (user may need to manualy switch to third phase). 

## Phase 3:
At the Third phase the AI will highlight all parts that are incorrect, like grammar, cohesion, etc. To make the writing finish and perfect. suggest word choice or suggest better sentence structure.
The third phase is finished when all errors are solved.





There are a bug: After writing something, then I chat to lingo, after that i got response from lingo AI my writing is gone. 

The user should be able to write at the writing field dirrectly or chat with lingo to find some topics to write. While writing, user can open chat mode to ask lingo. Lingo will assist to find topics to write, what else to write. etc. But lingo will be mindfull about users current writing. 
During chatting, lingo will automatically add topics to users writing field automatically.
User will update if lingo find something to write on or something that can give depth for writing. It will also look into users previous data to give personalization to the writing.

To achieve this, design a good prompt for the AI. or try design a good AI agent for this. I want this scaffolding feature advanced.







#########

I am making english learning app, but it is not done yet, the AI application is clunky, the chat the scaffolding, writing, and finishing activity is still very clunky. We need to redesign the mechanism, I found a langchain which i want to use ,I want to implement human in the loop using it, how it can improve. Lets try design a comprehensive AI agent for this application. It is a journal writing english learning app. The feature are guided journal writing to reduce blocks of user writing user making sure user got the fun parts, and most importantly focus on learning new things, ease cognitive load when writing. 


This is what I want:

Try not to modify the database, use the existing data structure ,but you can add field or table if it really needed.

The feature of this writing tool is an adaptive and highly personalized. The AI will try to know low level user informations like preferences, habit, small choices, to high level user cognition like motivation, goals, plan, how user solve problem, the decision making of user, and finally user thinking model. We might need new tables for this data. try conceptualize how to implement this using agentic or RAG or human in the loop thing. This data then used to create better more alligned and personalized AI to user interaction. 

The AI should try to direct the writing or interaction with the user towards:
What problem user encounter, what decision they took, why they took that decision, Ask why they did not decide the posible alternatives (think about user decision or choices alternative), How the user proceed the decision, The questions like How user solve the problem, etc. from lower level like habits preference or simple choices Towards higher level of thinking or cognition.

We will use low level to high level information about user to create meaningfull journal, and to build user thinking model.

make sure not to be too interogative, you can can ask simple think that is not too hard for user to answer, to ease user cognition.

The AI should align user not to talk about unmeaningfull things. Dont ask about sleep dream or something that are not going to something unmeaningfull.

The AI can align the user towards study topic since the users are students. anything related to study. But dont force them to talk in this topic.

If the user answer is vague you can ask apropriate details to clarify.

Each of writing stages (scaffolding, writing, and finishing) has different speciallized AI behavior. 

Scaffolding:

AI can be a thesaurus, sugesting fitting word of what user trying to say, or translating them if user dont know the english yet.

Chat on scaffolding will open a chat window where user can find topics orjournal writing outline for user. 
Guiding user towards knowing low level like preferences and habits, to ultimatelly thinking model of user. 

Writing:
AI is periodically checking user writing after "period" or "enter" Ai will check user writing for suggestion or just say carry on if user had something unfinished or if user is doing well.

User can chat while writing and ask something like translations or something if user encountered blocks.

No need to be so perfect in this stage

finishing: AI checks for grammar and ask user to fix it, Ai will guide them sentence by sentence.

i also want the AI can be tuned or is try find what are parametecallendarrs that can be ajusted like the strictness of writing evaluations, metrics for evaluations to aware of, and anything that can be ajusted to build a better system.


We will build this in step by step. in this step we are going to conceptualize how we do it how the AI agent mechanism, how it is can make it different new and meaningfull for the user.



we also need to consider writing and chat experience better. Conceptualize to fix the problem. I tried single shot prompt to make the chat better but the llm did not do a good job for it. These are the problem that we are going to fix:
- cant give suggestion or being a thesaurus while chatting, ussually the AI just output the answer back to english, without a phrase "to say teduh in english is shade" like that.

sometime, the AI 
















what sentiment analysis used for? 



The data design for user thinking model is not comprehensive enough. 

.The UTM (user thinking model) contains both low level to high level thinking model, including medium, not just limited high-level trait and low level patterns. we dont know how big this is. You can leave this blank I have comprehensive model and machanism for this model. The point is how to interface the model. So we need an abstraction or interface definition  to connect with the thinking model. The interface of this thinking model is ingestion and retrieval. Ingestions will be from mainly user writing but not limiited. Retrieval can be based on similarity or from specific topics or a query question that the model can answer. I will take care of the thinking model part. This model will be only responsible for personal thinking model only. To store the personal english learning data it  will be different and comprehensive. You will be responsible for that part. Make sure it is comprehensive. 

Now these are the things that you should also consider for english learning related part:




I am mmaking an english learning app using journaling, it is not complete yet, there is some bugs that we need to fix. 








Selamat siang mas, mohon dibantu saya sudah impor insentif untuk perusahaan ini. untuk status berhasil parsial. tetapi saya cek di payroll untuk nominal tidak muncul. Berikut data perusahaannya: 
Nama Perusahaan : PT Datanesia Multi Perkasa
Hostname : ptdatanesiamultiperkasa.api.kledo.com
Website UUID : 7cyi9z_api_kledo_com
Website ID : 165226
DB Server : tenant12
Last Login : 23-01-2025
Email Perusahaan : info@datanesiamp.co.id















I am creating an english learning application as journaling app. however the current system is still clunky. I want a better AI system for this app. better and most importantly not clunky. I need to design a comprehensive AI agent for this. I provided the current source code and a documentation on what I am going to improve. the documentation will be optimized for prompting since I relying on AI to build the app. it must be clear, complete, and accurate. Now, analyze the current documentation that will be the future changes. what do you thing about the agent design, i think it whould be still clunky, I want you to make the design better and make sure it is not clunky. there is some abiguity in the agent architecture. how the mechanism or the prompt flow of each agent. Is there more agent that are needed, or are there uneccessary agent that are unneeded? what agent does what, is it actually matter?



Lets anayze this is step by step no need to rust, granuraly, slowly but surely



I created a rollable shoping bag for me to go for shoping.

I am us




- Created a rollable shopping bag.
- Used a wheel, cardboard, and a luggage handle.
- Challenged by limited resources.
- Overcame resource limitations by buying wheels and using readily available cardboard and tape.
- Final product functioned well; able to roll and carry heavy items.
- Proud of resourceful use of leftover materials.



I created a rollable shoping bag for me to go for shoping.

Fantastic! What materials did you use, and how did the process go?

I use a wheel and a cardboard and a luggage handle from a broken suitcase

Wonderful! I've added that. What was the most challenging part of the construction?

it is using the only available resources. limited reseources.

That's insightful. How did you overcome the challenge of limited resources?

i bough a 2 wheels and used a easy to find card board and wrap it using tape to make it strong

Excellent! How well did the final shopping bag function?

it function very well it can roll and can carry many heavy items

That's impressive! What are you most proud of in this project?

i can use leftover materials and turn it into something usefull. it can became very hard to carry a lot of items without this. now i can go to the market for groceries for ease

That's a great point! What other creative solutions did you consider before settling on the wheel design?


Necessity, as they say, is the mother of invention, and today, I proved that adage true by building a reusable shopping bag from virtually nothing. My materials were surprisingly simple: two wheels I purchased inexpensively, some sturdy cardboard I found around the house, and an old luggage handle I had lying around. Using tape, I carefully reinforced the cardboard to ensure its strength and durability.

The process involves collecting materials. there are limited budged and there are many left over materials lying around. so why not turn it into something usefull?

I am creating an english learning companion as a journaling activity. However it is not complete yet.
I need to improve it as follow:
1. I want to add audio feature. All 
