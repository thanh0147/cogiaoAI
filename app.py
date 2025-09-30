from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# Import Gemini SDK
import google.generativeai as genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # cho phép tất cả origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StudentData(BaseModel):
    name: str
    grade: str
    gender: str
    mood: int
    bestPart: str
    notGood: str
    learned: str
    selfNote: str
    shareWithTeacher: bool
    wantSuggestion: bool

# Khởi client Gemini, SDK sẽ lấy API key từ biến môi trường nếu không truyền trực tiếp
#client = genai.Client(api_key="AIzaSyCvOEzoZy4I5hJooz5bpayWI-nY9XLdo_k")  # SDK tự đọc GEMINI_API_KEY hoặc GOOGLE_API_KEY nếu đã set :contentReference[oaicite:4]{index=4}
genai.configure(api_key=os.getenv("AIzaSyCvOEzoZy4I5hJooz5bpayWI-nY9XLdo_k"))

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return FileResponse("index.html")

@app.post("/submit")
async def submit_data(data: StudentData):
    # Tạo prompt để gửi cho Gemini
    prompt = f"""
    Đây là thông tin học sinh:
    - Tên: {data.name}
    - Lớp: {data.grade}
    - Giới tính: {data.gender}
    - Tâm trạng (1-5): {data.mood}
    - Điều thích nhất: {data.bestPart}
    - Điều chưa vui: {data.notGood}
    - Bài học rút ra: {data.learned}
    - Lời nhắn cho bản thân: {data.selfNote}

    Bạn là một cô giáo và là chuyên gia trong ngành Tâm lí học đường. 
    Từ những thông tin trên của HS đưa ra, hãy viết một đoạn phân tích ngắn, thân thiện (3-5 câu), giúp học sinh cảm thấy tích cực hơn.
    """

    if data.wantSuggestion:
        prompt += "Hãy thêm một gợi ý tích cực nhỏ để ngày mai tốt hơn."

    # Gọi Gemini để phân tích
    model = genai.GenerativeModel("gemini-2.5-flash")
    resp = model.generate_content(prompt)

    result_text = resp.text  # SDK trả về nội dung dưới thuộc tính `text`
    return {"analysis": result_text}


