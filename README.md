## Astrogate 
### i5 Space Chatbot 
C/Pung 10 Mar 2024

### Overview 
Project Goal: Turn the information on the [air force handbook](https://static.e-publishing.af.mil/production/1/af_a1/publication/afh1/afh1.pdf) and [publication page](https://www.e-publishing.af.mil/Product-Index/#/?view=cat&catID=1) into a chatbot.


### Mission 
The longterm mission of this project is to create a web API hosted on Amazon EC2, with a Rust backend which will be queried by Wix. Short-term, the mission of this project is to create a working chatbot for air force documents, published online, accessible by all Air Force and Space Force cadets. 

This will allows users to search for information in lengthy Air Force PDFs, specifically the SOP, 2024 FTM, Drill and Ceremonies, and the Tounge and Quill extracted from PDFs using natural language queries, and HTML from the i5 website.

### Execution

This mission will be executed by writing a simple frontend in typescript, storing local chats. The logic for connecting Qdrant open source vector storage, with the OpenAI embedding model, and GPT-4.  

### Project Requirements 
Ability to achieve PDF text extraction, text embedding, vector storage and querying, and displaying results on a Wix site.