import chromadb
import fastapi
import uvicorn
from pydantic import BaseModel


chroma_client = chromadb.HttpClient(host='localhost', port=8000)
client = chromadb.PersistentClient(path="D:\chroma_database_aibeecara")


def create_user_colection_by_name(name):
    collection = chroma_client.create_collection(name=f"{name}")

def find_collection(name):
    collection = chroma_client.get_collection(name= f"{name}")
    return collection

def add_collection_convo(response,username,user_counter):
    coll = find_collection(username)
    coll.add(
        documents=response,ids=user_counter
    )

def get_coll_related_to_input(username, input,n):
    coll = find_collection(username)
    return coll.query(query_texts= input,n_results= n)

app = fastapi.FastAPI()

class submit_history(BaseModel):
    response : str
    username : str
    user_counter : str

class submit_querry(BaseModel):
    username : str
    input : str
    n : int

@app.get("/database/create/{username}")
async def create_collection(username):
    try: 
        create_user_colection_by_name(username)
        return {"status" :"collection succesfully added" }
    except :
        return {"status" :"something wrong duh" }
    
@app.post("/database/history")
async def post_history(post : submit_history):
    try: 
        add_collection_convo(post.response, post.username,post.user_counter)
        return {"status" :"success" }
    except :
        return {"status" :"something wrong duh" }
    

@app.post("/database/querry")
async def querry (input : submit_querry):
    try: 
        response = get_coll_related_to_input(input.username,input.input,input.n)
        list_context=response["documents"][0]
        return {"status" :"success","context":f"{list_context}" }
    except :
        return {"status" :"something wrong duh" }
    
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=30000)
